import cv2
import time
import requests 
import base64
import json 
import os
import threading
import asyncio
import aiohttp

async def explain_image(image_path, model, prompt, ollama_url):
        
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
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:

            response_data = ""
            if response.status_code == 200:
                async for chunk in response.iter_lines():
                    if chunk:
                        data = chunk.decode('utf-8')
                        data_list = json.loads(data)
                        content = data_list['message']['content']
                        response_data += content
            else:
                print(f"Error: {response.status_code} - {await response.text()}")
            return response_data


async def processVideoStream():
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

        cv2.imwrite('saved_frame.jpg', frame)
        print("Frame saved as 'saved_frame.jpg'")

        asyncio.create_task(getCommand())

        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            # Save the current frame
            break

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


async def getCommand():
        # Load the prompt from a JSON file
    with open('prompt.json', 'r') as f:
        prompt_data = json.load(f)

    model = prompt_data['model']
    prompt = prompt_data['prompt']
    url = prompt_data['url']
        
    image_inference = await explain_image("saved_frame.jpg", model, prompt, url)    
    print(image_inference)

async def main():
    await asyncio.create_task(getCommand())
    await processVideoStream()


if __name__ == "__main__":
    asyncio.run(main())