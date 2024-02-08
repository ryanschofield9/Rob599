#!/usr/bin/env python

import rospy 
import sys 
import time 
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from rob599_hw1.srv import StoppingDistance, StoppingDistanceRequest


def callback(request):
    rospy.loginfo(f"the request was: {request.data}")
    msg = Float64()
    val = Bool()
    print(StoppingDistanceRequest(4.0).data)
    if request.data > StoppingDistanceRequest(4.0).data:
        rospy.loginfo(f"the request was greater than 4 and a default value of 1 will be published")
        msg.data = 1.0
        val = False
    elif request.data < StoppingDistanceRequest(0.5).data:
        rospy.loginfo(f"the request was less than 0.5 and a default value of 1 will be published")
        msg.data = 1.0 
        val = False
    else: 
        rospy.loginfo("the request was good and will be published")
        msg.data = request.data 
        val = True 
    
    #start_time = time.time
    #while (time.time - start_time < 3): 
    publisher.publish(msg)
    return val 



#used example code in github (server.py) and example page on ros wiki to help write this
if __name__ == '__main__':
    rospy.init_node('stopping_distance')
    service = rospy.Service('stopping_distance', StoppingDistance, callback)
    rospy.loginfo('Service started. No number greater than 4 will be accepted and no number less than 0.5 will be accepted')
    #value greater than 4 and the robot will not move anywhere, value less than 0.5 and it will be getting to close 
    
    publisher = rospy.Publisher('distance',Float64, queue_size=10)
    
    rospy.spin()
