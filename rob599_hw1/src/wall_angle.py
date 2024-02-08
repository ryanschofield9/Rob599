#!/usr/bin/env python

import rospy 
import sys
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
import math 
from geometry_msgs.msg import Point

def callback(msg):
    
    short = min(msg.ranges)
    total = len (msg.ranges)

    idx = msg.ranges.index(short)

    if (idx == round(total/2)):
        angle = 90 
    elif(idx < round(total/2)):
        angle = 90 -((round (total/2) - idx) *msg.angle_increment)
    else: 
        angle = 90 + (( idx - round (total/2)) * msg.angle_increment)
    
    x = short *math.cos(angle)
    y = (short*short) - (x*x)
    z= short
    pts = Point()
    pts.x = - x *10 
    pts.y = y *10
    pts.z = 0
    
    arrow = Marker()
    arrow.header.frame_id = "laser_link"
    arrow.type = arrow.POINTS
    arrow.id = 0
    arrow.action= arrow.ADD
    arrow.scale.x = short
    arrow.scale.y = 0.5
    arrow.scale.z - 0.5
    arrow.color.r = 0.0
    arrow.color.b = 1.0
    arrow.color.g = 0.0
    arrow.color.a = 1.0
    arrow.points= [pts]
    publisher.publish(arrow)
    
    text = Marker()
    text.header.frame_id = "laser_link"
    text.type = text.TEXT_VIEW_FACING
    text.id = 1
    text.action= text.ADD
    text.text = str(angle)
    text.scale.z = 1.0
    text.color.r = 1.0
    text.color.b = 1.0
    text.color.g = 1.0
    text.color.a = 1.0
    publisher2.publish(text)







if __name__ == '__main__':
    # used publisher and subsriber noted in rob599_basic to write this 
    rospy.init_node('wall_angle_node', argv=sys.argv)
    
    
    subscriber = rospy.Subscriber('base_scan', LaserScan, callback)
    publisher = rospy.Publisher('arrow', Marker, queue_size=10)
    publisher2 = rospy.Publisher('text', Marker, queue_size=10)
    rospy.spin()