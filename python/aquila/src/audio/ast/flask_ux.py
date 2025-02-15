from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file:
            try:
                url = "http://localhost:8000/predict"
                #url = "http://138.246.17.57:8000/predict"
                files = {'file': (file.filename, file.stream, file.content_type)}
                response = requests.post(url, files=files)
                
                if response.status_code == 200:
                    return jsonify({'result': response.text})
                else:
                    return jsonify({'error': f"Error: {response.status_code} - {response.text}"})
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
