#!/usr/bin/env python

import rospy 
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
    
    min_range = min(msg.ranges)
    rospy.loginfo(f"Got {min_range}, {len(msg.ranges)}")

    cmd = Twist()
    if min_range > 2: 
        cmd.linear.x = 1 
    elif min_range > 1.8:
        cmd.linear.x = 0.8
    elif min_range > 1.6: 
        cmd.linear.x = 0.6
    elif min_range > 1.4: 
        cmd.linear.x = 0.4 
    elif min_range > 1.0: 
        cmd.linear.x = 0.2 
    elif min_range < 1: 
        cmd.linear.x = 0
    
    publisher.publish(cmd)


if __name__ == '__main__':
    # used publisher and subsriber noted in rob599_basic to write this 
    rospy.init_node('stop_node', argv=sys.argv)
    
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    subscriber = rospy.Subscriber('filter', LaserScan, callback)
    rospy.spin()