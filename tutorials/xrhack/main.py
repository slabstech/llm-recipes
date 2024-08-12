import cv2
import time
import requests 
import json 
import requests
import base64
import json 
import time
import os


def explain_image(image_path, model, prompt, ollama_url):
        
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    url = ollama_url + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image.decode("utf-8")]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    response_data = ""
    if response.status_code == 200:
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode('utf-8')
                data_list = json.loads(data)
                content = data_list['message']['content']
                response_data += content
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return response_data



def processVideoStream():
    # Replace '0' with the appropriate device index for your capture card
    cap = cv2.VideoCapture(0)

    start_time = time.time()
    if not cap.isOpened():
        print("Error: Could not open video device.")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the resulting frame
        cv2.imshow('Read video', frame)

        elapsed_time = time.time() - start_time
        if elapsed_time > 3:
            # Save the current frame
            cv2.imwrite('saved_frame.jpg', frame)
            print("Frame saved as 'saved_frame.jpg'")
            '''
                    # Send a GET request for the next command
            response = requests.get('http://your-server.com/next-command')

            # Check the status code for the response
            if response.status_code == 200:
                print("Next command received successfully")
                # You can process the response data here
            else:
                print("Failed to get next command")
            '''
            break

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def getCommand():
        # Load the prompt from a JSON file
    with open('prompt.json', 'r') as f:
        prompt_data = json.load(f)

    model = prompt_data['model']
    prompt = prompt_data['prompt']
    url = prompt_data['url']
        
    image_inference = explain_image("saved_frame.jpg", model, prompt, url)    
    print(image_inference)

def main():
    processVideoStream()
    getCommand()


if __name__ == "__main__":
    main()

