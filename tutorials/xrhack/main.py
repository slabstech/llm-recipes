import cv2
import time
# Replace '0' with the appropriate device index for your capture card
cap = cv2.VideoCapture(0)

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
        break

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
