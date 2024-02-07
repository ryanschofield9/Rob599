#!/usr/bin/env python

import rospy 
import sys 
from std_msgs.msg import Float64
from std_msgs.msg import Bool


def callback(request):
    rospy.loginfo(f"the request was: {request.data}")
    msg = Float64()
    val = Bool()
    if request > 4:
        rospy.loginfo(f"the request was greater than 4 and a default value of 1 will be published")
        msg.data = 1.0
        val = False
    elif request < 0.5:
        rospy.loginfo(f"the request was less than 0.5 and a default value of 1 will be published")
        msg.data = 1.0 
        val = False
    else: 
        rospy.loginfo("the request was good and will be published")
        msg.data = request.data 
        val = True 
    
    publisher.publish(msg)
    return val 



#used example code in github (server.py) and example page on ros wiki to help write this
if __name__ == '__main__':
    rospy.init_node('stopping_distance')
    service = rospy.Service('stopping_distance', Float64, callback)
    rospy.loginfo('Service started. No number greater than 4 will be accepted and no number less than 0.5 will be accepted')
    #value greater than 4 and the robot will not move anywhere, value less than 0.5 and it will be getting to close 
    
    publisher = rospy.Publisher('distance',Float64, queue_size=10)
    
    rospy.spin()
