from djitellopy import Tello
import time
import cv2
import numpy as np

from vision_query import VisionQuery  # Assuming vision_query.py is in the same directory

class ImageProcessor:
    def __init__(self, threshold=127):
        self.threshold = threshold
        self.vision_query = VisionQuery()

    def check_light_condition(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average_intensity = np.mean(gray)

        if average_intensity > self.threshold:
            return True  # Light condition
        else:
            return False  # Dark condition

    def process_image(self, frame):
        light_condition = self.check_light_condition(frame)
        # Add your image processing code here
        # For example, you can use self.vision_query to query the image
        result = self.vision_query.query(frame)
        return result, light_condition


class DroneNavigation:
    def __init__(self, drone):
        self.drone = drone
        self.global_map = {}
        self.frame_read = None

    def is_environment_suitable_for_navigation(self):

        frame = self.frame_read.frame
        light_condition = self.drone.check_light_condition(frame)
        vlm_understanding = True  # Replace with actual VLM understanding check
        return light_condition and vlm_understanding

    def take_photo(self, file_name_for_image):
        # This is a placeholder. You'll need to implement the actual photo taking.
        cv2.imwrite(file_name_for_image, self.frame_read.frame)

    def verify_navigation(self):
        # This is a placeholder. You'll need to implement the actual navigation verification.
        return True

    def create_360_map(self):
        self.frame_read = self.drone.get_frame_read()
        #tello.rotate_clockwise(360)
        current_epoch = int(time.time())

        for counter in range(12):
            time.sleep(1)
            file_name_for_image = f'image_{current_epoch}_b_{counter}.jpg'
            self.take_photo(file_name_for_image)

#            if not self.verify_navigation():
#                return False
             # TODO - enable turn after photo capture   
#            self.drone.turn(30)
#            if not self.verify_navigation():
#                return False
        return True

    def expand_map(self, path):
        self.drone.move(path)
        if not self.verify_navigation():
            return False
        self.drone.return_to_start()
        return True

    def navigate(self):
        if not self.is_environment_suitable_for_navigation():
            self.drone.land()
            return

        self.drone.stream_on()
        current_epoch = int(time.time())
        file_name_for_image = f'image_{current_epoch}_b_1.jpg'
        self.take_photo(file_name_for_image)

        # TODO - enable takeoff after processing check
#        self.drone.takeoff()

        if not self.create_360_map():
            self.drone.land()
            return

        # This is a placeholder. You'll need to implement the actual path planning.
        path = "some_path"  # Replace with actual path planning
        if not self.expand_map(path):
            self.drone.land()
            return

        self.drone.land()

class Drone(Tello):
    def __init__(self):
        super().__init__()
        self.connect()
        self.streamon()

    def takeoff(self):
        self.streamon()
        self.takeoff()

    def turn(self, degrees):
        self.rotate_clockwise(degrees)

    def move(self, path):
        # This is a placeholder. You'll need to implement the actual move.
        pass

    def land(self):
        self.streamoff()
        self.land()
    
    def return_to_start(self):
        # This is a placeholder. You'll need to implement the actual return to start.
        pass

    def check_light_condition(self,frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the average pixel intensity
        average_intensity = np.mean(gray)

        # Define a threshold to determine light or dark condition
        # This value can be adjusted based on your specific use case
        threshold = 127

        if average_intensity > threshold:
            return True  # Light condition
        else:
            return False  # Dark condition

def main():
    drone = Drone()
    drone_navigation = DroneNavigation(drone)
    drone_navigation.navigate()

if __name__ == "__main__":
    main()
