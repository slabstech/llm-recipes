import React, { Component, createRef } from 'react';
import axios from 'axios';
import { AxiosError } from 'axios';
import './App.css'

const ollamaBaseUrl = 'http://localhost:11434/api';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      base64StringImage: null,
      response: null,
      prompt: '',
      uploadedImage: null,
    };
    this.promptRef = createRef();
  }

  componentDidMount() {
    this.getOrPullModel('moondream:latest');
  }

  checkModelExists = async (modelName) => {
    try {
      await axios.post(`${ollamaBaseUrl}/show`, { name: modelName });
      return true; // Model exists
    } catch (error) {
      if (error instanceof AxiosError && error.response && error.response.status === 404) {
        return false; // Model doesn't exist
      }
      throw error; // Rethrow other errors
    }
  };

  pullModel = async (modelName) => {
    const requestBody = {
      name: modelName,
      stream: false
    };

    try {
      const response = await axios.post(`${ollamaBaseUrl}/pull`, requestBody);
      console.log('Model pulled successfully:', response.data);
    } catch (error) {
      console.error('Error pulling model:', (error as AxiosError).message);
    }
  };
  getOrPullModel = async (modelName) => {
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

  handleImageUpload = (event) => {
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

  sendImageToOllama = async () => {
    if (!this.state.base64StringImage) return;
    this.setState({ prompt: this.promptRef.current?.value || '' });

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

    const ollamaEndpoint = 'http://localhost:11434/api/chat';

    try {
      const response = await axios.post(ollamaEndpoint, requestBody);
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
      <p className="read-the-docs">
        Warehouse UI
      </p>
          <input type="text" ref={this.promptRef} placeholder="Enter your prompt here..." />
          <input type="file" onChange={this.handleImageUpload} />
          <button onClick={this.sendImageToOllama}>Upload</button>        

      {this.state.response && (
        <div>
          <h4>Response:</h4>
          <pre>{JSON.stringify(this.state.response, null, 2)}</pre>
          {this.state.uploadedImage && (
              <img src={this.state.uploadedImage} alt="Uploaded" width="100" height="100" />
            )}
        </div>
      )}
      
    </>
  )
}
}

export default App;
