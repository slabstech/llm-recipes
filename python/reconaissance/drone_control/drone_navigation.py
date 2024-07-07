from djitellopy import Tello
import time
import cv2
class DroneNavigation:
    def __init__(self, drone):
        self.drone = drone
        self.global_map = {}

    def is_environment_suitable_for_navigation(self):
        # This is a placeholder. You'll need to implement the actual checks.
        light_condition = True  # Replace with actual light condition check
        vlm_understanding = True  # Replace with actual VLM understanding check
        return light_condition and vlm_understanding

    def take_photo(self, file_name_for_image, frame_read):
        # This is a placeholder. You'll need to implement the actual photo taking.
        cv2.imwrite(file_name_for_image, frame_read.frame)

    def verify_navigation(self):
        # This is a placeholder. You'll need to implement the actual navigation verification.
        return True

    def create_360_map(self):
        frame_read = self.drone.get_frame_read()
        #tello.rotate_clockwise(360)
        current_epoch = int(time.time())

        for counter in range(12):
            time.sleep(1)
            file_name_for_image = f'image_{current_epoch}_b_{counter}.jpg'
            self.take_photo(frame_read, file_name_for_image)

#            if not self.verify_navigation():
#                return False
            self.drone.turn(30)
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
            self.drone.stream_off()
            return

        self.drone.stream_on()
        self.take_photo()
        self.drone.takeoff()

        if not self.create_360_map():
            self.drone.stream_off()
            return

        # This is a placeholder. You'll need to implement the actual path planning.
        path = "some_path"  # Replace with actual path planning
        if not self.expand_map(path):
            self.drone.stream_off()
            return

        self.drone.stream_off()

class Drone(Tello):
    def __init__(self):
        super().__init__()
        self.connect()
        self.streamon()

    def stream_on(self):
        self.streamon()

    def stream_off(self):
        self.streamoff()

    def takeoff(self):
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


def main():
    drone = Drone()
    drone_navigation = DroneNavigation(drone)
    drone_navigation.navigate()

if __name__ == "__main__":
    main()
