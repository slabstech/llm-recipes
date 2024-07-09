Navigation Algo 


Start Program

Stream on

Take photo

Function IsEnvironmentSuitableForNavigation 
Check for light condition 
Check if it can understand the location from Images via VLM

Return true if suitable - light available,  enough free space for forward movement. 

False if unsuitable,  night/dark/cluttered /obstacles 


If function returned false 
Stream off 
End program 

If function returned true 

Takeoff 

Function 360Map creation 
Take photo 
Verify navigation 

Take 30 deg turns x 12 times 
Take photo 
Verify navigation 
Build a map around the drone.  


Function expand map (path, global map)
Move in + plus path to extend the map, based on previous path created.  
Always return to starting based on vision odometry  


360 classification - work plan 

Part 1 

Take 12 photos as 1 sec interval

Send images to image processors 

Image processor will write description


Make this code work.

Part 2 

Take photos from dronr without launch .
Move drone with uand 30ndeg every second 
Save images to file.

Merge 1 - Connect part 1 and part 2


Part 3

Launch drone.
Make 12 turn and take photos.


Merge 2 - connect part 3 with merge 1


Part 4 - advanced 
Trial with ros2 nodes, drone as a node, image processors as a node , report generator as a mode.

--

mock drone camera for Recon Algo 

Mock drone video capture as webcam cv2 capture.
Improve the algorithm and then use drone fit testing. 
Turn function,  move laptop manual to simluate use case

Camera should be mocked by Webcam to reduce dependency issue. 







