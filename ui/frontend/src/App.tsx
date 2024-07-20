import { Component, ChangeEvent } from 'react';
import axios from 'axios';
import { AxiosError } from 'axios';
import './App.css'
import TextField from '@mui/material/TextField';

interface AppState {
  base64StringImage: string | null;
  response: any;
  prompt: string;
  uploadedImage: string | null;
  isLoading: boolean;
  models: string[]; 
  selectedModel: string; 
}

class App extends Component<{}, AppState> {
  ollamaBaseUrl = import.meta.env.VITE_OLLAMA_BASE_URL;
  constructor(props:{}) {
    super(props);
    this.state = {
      base64StringImage: null,
      response: null,
      prompt: '',
      uploadedImage: null,
      isLoading: false,
      models: ['moondream', 'llava'], 
      selectedModel: 'moondream', 
    };
  }

  componentDidMount() {
    this.getOrPullModel(this.state.selectedModel);
  }

  checkModelExists = async (modelName:string) => {
    try {
      await axios.post(`${this.ollamaBaseUrl}/show`, { name: modelName });
      return true; // Model exists
    } catch (error) {
      if (error instanceof AxiosError && error.response && error.response.status === 404) {
        return false; // Model doesn't exist
      }
      throw error; // Rethrow other errors
    }
  };

  pullModel = async (modelName:string) => {
    const requestBody = {
      name: modelName,
      stream: false
    };

    try {
      const response = await axios.post(`${this.ollamaBaseUrl}/pull`, requestBody);
      console.log('Model pulled successfully:', response.data);
    } catch (error) {
      console.error('Error pulling model:', (error as AxiosError).message);
    }
  };
  getOrPullModel = async (modelName:string) => {
    try {
      const modelExists = await this.checkModelExists(modelName);
      if (modelExists) {
        console.log(`Model '${modelName}' already exists.`);
      } else {
        console.log(`Model '${modelName}' not found. Pulling...`);
        await this.pullModel(modelName);
      }
    } catch (error) {
      console.error('Error:', (error as AxiosError).message);
    }
  };

  handleImageUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const reader = new FileReader();

      reader.onloadend = () => {
        if (typeof reader.result === 'string') {
          this.setState({ 
            base64StringImage: reader.result.split(',')[1],
            uploadedImage: reader.result, 
          });
        }
      }
      reader.readAsDataURL(file);
    } else {
      // handle the case where no file was selected
    }
  };

  handlePromptChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ prompt: event.target.value });
  };

  handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    this.setState({ selectedModel: event.target.value }, () => {
      this.getOrPullModel(this.state.selectedModel);
    });
  };

  sendImageToOllama = async () => {
    if (!this.state.base64StringImage) return;
    
    const requestBody = {
      model: 'moondream',
      messages: [
        {
          role: 'user',
          content: this.state.prompt,
          images: [this.state.base64StringImage]
        }
      ],
      stream: false
    };

    const ollamaEndpoint = this.ollamaBaseUrl + '/chat';

    try {
      const response = await axios.post(ollamaEndpoint, requestBody);
      console.log("Prompt - ", this.state.prompt);
      console.log('Image processing result:', response.data.message.content);
      this.setState({ response: response.data.message.content });
      return response.data.message.content;
    } catch (error) {
      console.error('Error processing image:', (error as AxiosError).message);
      throw error;
    }
  };

  render(){
  return (
    <>
    <div className="app-container">
      <p className="read-the-docs">
        Warehouse UI
      </p>
      <div className="input-container">
          <TextField
            value={this.state.prompt}
            onChange={this.handlePromptChange}
            placeholder="Enter your prompt here..."
            fullWidth
          />
            <input 
              type="file" 
              onChange={this.handleImageUpload} 
          />
          <button 
            onClick={this.sendImageToOllama} 
            disabled={this.state.isLoading}>
            {this.state.isLoading ? 'Processing...' : 'Upload'}
          </button>
          <select 
            value={this.state.selectedModel} 
            onChange={this.handleModelChange}>
            {this.state.models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>        
      </div>    
      {this.state.response && (
        <div className="response-container">
          <h4>Response:</h4>
          <pre>{JSON.stringify(this.state.response, null, 2)}</pre>
          {this.state.uploadedImage && (
              <img 
              src={this.state.uploadedImage} 
              alt="Uploaded" 
              width="100" height="100" />
            )}
        </div>
      )}
      </div>  
    </>
  )
}
}

export default App;
