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





