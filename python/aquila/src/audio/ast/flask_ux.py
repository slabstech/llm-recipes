from flask import Flask, render_template, request, jsonify
import requests
import time

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

                # Measure the start time
                start_time = time.time()

                response = requests.post(url, files=files)

                # Measure the end time
                end_time = time.time()

                # Calculate the time taken in milliseconds
                time_taken_ms = (end_time - start_time) * 1000

                if response.status_code == 200:
                    return jsonify({
                        'result': response.text,
                        'time_taken_ms': time_taken_ms,
                        'label': 'Time taken in milliseconds'
                    })
                else:
                    return jsonify({
                        'error': f"Error: {response.status_code} - {response.text}",
                        'time_taken_ms': time_taken_ms,
                        'label': 'Time taken in milliseconds'
                    })
            except Exception as e:
                return jsonify({
                    'error': str(e),
                    'time_taken_ms': time_taken_ms,
                    'label': 'Time taken in milliseconds'
                })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)