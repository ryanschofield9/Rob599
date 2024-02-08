# How to Run the Code
# Launch File
launch file is normal and can just run roslaunch rob599_hw1 wall_stare.launch (assumes that the fetch_world.launch is already running

Make sure that service code and action code is commented out (there are notes in stop_fetch.py on what needs to be commented out and when 

Also make sure that the subscriber is uncommented (gets commented out when running action call) 


# Service Call 
Make sure to run the code in the following order to get best results: service.py, stop_fetch.py, filter.py.

Make sure to uncomment out the correct code in stop_fetch.py (commented in the code on where) and make sure all action code is commented  

The service call has a spot when you can put in a value, if the value is not possible it will tell you that is not viable and set 1.0 as the distance 

# Action Call 
Make sure to run the code in the following order to get best results: actrion_server.py, filter.py, stop_fetch.py 

Make sure to uncomment out the correct code in the stop_fetch.py (commented in the code on where) and maek sure all service code is commented 

Make sure to comment out the subscriber noted in the code 

The action call has a spot where you can put in a value 

# Markers 
Make sure to run the marker.py file and can run with the launch file or the filter.py and stop_fetch.py file seperately 

# Wall Angles
Make sure to run the wall_angle.py file and can run with the launch file or the filter.py and stop_fetch.py file seperately

Doesn't work great, but I thought I would include it anyways as there is visuals on rviz for it 

# Videos 
5 videos have been included 

launch_file_to shows filter node, launch file, basic stopping control of the fetch 

service_call_to shows the service call functionality 

action_call_to shows the action call functionality

marker_to shows the marking of the shortest distance to the wall 

wall_angle_to shows the wall_angle marking and solving functionality 
