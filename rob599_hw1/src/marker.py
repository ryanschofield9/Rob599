#!/usr/bin/env python

import rospy 
import sys
from visualization_msgs.msg import Marker
from sensor_msgs.msg import LaserScan


def callback(msg):
    ranges = min(msg.ranges)
    arrow = Marker()
    arrow.header.frame_id = "laser_link"
    arrow.type = arrow.ARROW
    arrow.id = 0
    arrow.action= arrow.ADD
    arrow.scale.x = ranges
    arrow.scale.y = 0.5 
    arrow.scale.z - 0.5
    arrow.color.r = 0.0
    arrow.color.b = 1.0
    arrow.color.g = 0.0
    arrow.color.a = 1.0
    publisher.publish(arrow)
    
    text = Marker()
    text.header.frame_id = "laser_link"
    text.type = text.TEXT_VIEW_FACING
    text.id = 1
    text.action= text.ADD
    text.text = str(ranges)
    text.scale.z = 1.0
    text.color.r = 1.0
    text.color.b = 1.0
    text.color.g = 1.0
    text.color.a = 1.0
    publisher2.publish(text)


#used marker.py example in github to write this 
if __name__ == '__main__':
    rospy.init_node('markers', argv=sys.argv)
    subscriber = rospy.Subscriber('filter', LaserScan, callback)
    publisher = rospy.Publisher('arrow', Marker, queue_size=10)
    publisher2 = rospy.Publisher('text', Marker, queue_size=10)
    rospy.spin()
        