
# Ghost Vision 

The project utilises advanced image processing tasks, leveraging state-of-the-art machine learning models for image generation, editing, inpainting, object detection, and segmentation. It uses models like Stable Diffusion, InstructPix2Pix, Grounding DINO, and SAM 2, with lazy loading to optimize memory usage and startup time.

## Features
- **Image Generation**: Generate images from text prompts using Stable Diffusion XL.
- **Image Editing**: Edit images based on text instructions with InstructPix2Pix.
- **Inpainting**: Fill masked areas of an image with generated content, optionally using a reference image.
- **Object Detection**: Detect objects in images using Grounding DINO and return bounding box information.
- **Segmentation**: Segment objects from images and remove backgrounds or mask objects using SAM 2.
- **Custom Tank Camouflage**: Apply camouflage to tank images and blend them into scenes.

## Prerequisites
- Python 3.10+
- CUDA-enabled GPU (optional, but recommended for faster processing)
- Git (for cloning the repository)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```
3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```
Sample requirements.txt
Create a requirements.txt file with the following content:
```
fastapi==0.115.0
uvicorn==0.30.6
torch==2.4.1
diffusers==0.30.3
transformers==4.44.2
safetensors==0.4.5
huggingface-hub==0.25.1
Pillow==10.4.0
numpy==1.26.4
opencv-python==4.10.0.84
```

Note: You may need to install sam2 separately if it's not available via PyPI. Follow the official SAM 2 repository instructions.
4. Set Environment Variables (Optional)
If you have a Hugging Face token for model access, set it as an environment variable:
bash
```bash
export HF_TOKEN="your-hugging-face-token"  # On Windows: set HF_TOKEN=your-hugging-face-token
```
5. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```
The API will be available at http://localhost:7860.
Usage
API Endpoints
1. Health Check

    Endpoint: GET /health
    Description: Check if the API is running.
    Response: {"status": "healthy"}

2. Generate Image

    Endpoint: GET /generate?prompt=<text>
    Description: Generate an image from a text prompt using Stable Diffusion XL.
    Example:
    ``` bash
    curl "http://localhost:7860/generate?prompt=A futuristic city at night" -o generated_image.png
    ```
3. Edit Image

    Endpoint: POST /edit-image/
    Description: Edit an image based on a text instruction using InstructPix2Pix.
    Parameters:
        file: Image file (multipart/form-data)
        instruction: Text instruction (e.g., "Make it sunny")
        steps: Inference steps (default: 50)
        text_cfg_scale: Text guidance scale (default: 7.5)
        image_cfg_scale: Image guidance scale (default: 1.5)
        seed: Random seed (default: 1371)
    Example:
    ```bash
    curl -X POST -F "file=@input.jpg" -F "instruction=Make it sunny" "http://localhost:7860/edit-image/" -o edited_image.png
    ```
4. Inpaint Image (Coordinates)

    Endpoint: POST /inpaint/
    Description: Inpaint a rectangular area of an image based on a prompt.
    Parameters:
        file: Image file
        prompt: Text prompt for inpainting
        mask_coordinates: Rectangle coordinates (format: "x1,y1,x2,y2")
        steps: Inference steps (default: 50)
        guidance_scale: Guidance scale (default: 7.5)
        seed: Random seed (default: 1371)
    Example:
    ```bash
    curl -X POST -F "file=@input.jpg" -F "prompt=Add a tree" -F "mask_coordinates=100,100,200,200" "http://localhost:7860/inpaint/" -o inpainted_image.png
    ```
5. Inpaint with Mask

    Endpoint: POST /inpaint-with-mask/
    Description: Inpaint an image using a provided mask image.
    Parameters:
        image: Image file
        mask: Mask image file (white areas indicate inpainting regions)
        prompt: Text prompt (default: "Fill the masked area with appropriate content.")
    Example:
    ```bash
    curl -X POST -F "image=@input.jpg" -F "mask=@mask.png" -F "prompt=Add a river" "http://localhost:7860/inpaint-with-mask/" -o inpainted_image.png
    ```
6. Inpaint with Reference

    Endpoint: POST /inpaint-with-reference/
    Description: Inpaint an image using a reference image and rectangular mask.
    Parameters:
        image: Target image file
        reference_image: Reference image file
        prompt: Text prompt (default: "Integrate the reference content naturally...")
        mask_x1, mask_y1, mask_x2, mask_y2: Mask coordinates (defaults: 100,100,200,200)
    Example:
    ```bash
    curl -X POST -F "image=@background.jpg" -F "reference_image=@ref.jpg" -F "mask_x1=100" -F "mask_y1=100" -F "mask_x2=200" -F "mask_y2=200" "http://localhost:7860/inpaint-with-reference/" -o result.png
    ```
7. Fit Image to Mask

    Endpoint: POST /fit-image-to-mask/
    Description: Fit a camouflaged tank into a specified mask area in an image.
    Parameters:
        image: Background image file
        reference_image: Tank image file
        mask_x1, mask_y1, mask_x2, mask_y2: Mask coordinates (defaults: 200,200,500,500)
    Example:
    ```bash
    curl -X POST -F "image=@field.jpg" -F "reference_image=@tank.jpg" "http://localhost:7860/fit-image-to-mask/" -o fitted_image.png
    ```
8. Detect Objects (JSON)

    Endpoint: POST /detect-json/
    Description: Detect objects in an image and return bounding box data in JSON.
    Parameters:
        file: Image file
        text_query: Object to detect (default: "a tank.")
    Example:
    ```bash
    curl -X POST -F "file=@image.jpg" "http://localhost:7860/detect-json/" -o detections.json
    ```
9. Segment Image

    Endpoint: POST /segment-image/
    Description: Segment objects and remove the background.
    Parameters:
        file: Image file
        text_query: Object to segment (default: "a tank.")
    Example:
    ```bash
    curl -X POST -F "file=@image.jpg" "http://localhost:7860/segment-image/" -o segmented_image.png
    ```
10. Mask Object

    Endpoint: POST /mask-object/
    Description: Mask detected objects, removing them from the image.
    Parameters:
        file: Image file
        text_query: Object to mask (default: "a tank.")
    Example:
    ```bash
    curl -X POST -F "file=@image.jpg" "http://localhost:7860/mask-object/" -o masked_image.png
    ```

- Notes
    - Lazy Loading: Models are loaded on-demand when their endpoints are first called, reducing startup time but adding latency to the initial request.
    GPU Support: For optimal performance, run on a CUDA-enabled GPU. CPU fallback is supported but slower.
    File Naming: Replace main:app in the uvicorn command with your actual Python filename (e.g., app:app if the file is named app.py).

- Troubleshooting
    - Model Loading Errors: Ensure you have internet access and correct Hugging Face credentials if required.
    Memory Issues: If running out of GPU memory, reduce batch sizes or use a CPU by setting device = "cpu" in the code.
    Dependencies: Verify all packages are installed correctly. Use pip install --upgrade <package> for any version conflicts.

- Contributing
    - Feel free to submit issues or pull requests to improve this project. Contributions are welcome!
- License
-   This project is licensed under the MIT License. See the LICENSE file for details.


### How to Use
1. Copy the above content into a file named `README.md` in your project directory.
2. Replace `https://github.com/yourusername/your-repo-name.git` with your actual GitHub repository URL.
3. Ensure you have a `requirements.txt` file with the dependencies listed, and adjust versions as needed based on your environment.
4. If you include a `LICENSE` file in your project, update the link in the "License" section accordingly.
