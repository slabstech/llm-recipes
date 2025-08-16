import cv2


def take_picture(filename):
    # Initialize the webcam (0 is usually the default camera)
    cam = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cam.isOpened():
        print("Cannot open camera")
        exit()

    # Read one frame from the camera
    ret, frame = cam.read()

    # If a frame is successfully returned, save it as an image
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Photo captured and saved as  {filename}")
    
    else:
        print("Failed to capture image")

    # Release the camera
    cam.release()

    return ret


def describe_image(filename):
    image_bytes = await file.read()
    image = BytesIO(image_bytes)
    img_base64 = encode_image(image)
    text = ocr_page_with_rolm(img_base64, model="gemma3")


filename = "photo.jpg"
take_picture(filename=filename)


describe_image(filename)