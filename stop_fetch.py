#!/usr/bin/env python

import rospy 
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64 

class StopFetch():
    def __init__(self):
        self.distance = 1.0
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.subscriber = rospy.Subscriber('filter', LaserScan, self.callback)
        self.sub = rospy.Subscriber('distance', Float64, self.callback_2)

    def callback(self,msg):
        
        rosy.wait_for_service("stopping_distance")
        distance_service = rospy.ServiceProxy('stopping_distance', Float64)

        distance_recieved = distance_service(1.2)

        min_range = min(msg.ranges)
        rospy.loginfo(f"Got {min_range}, {len(msg.ranges)}")

        cmd = Twist()
        if min_range > (self.distance * 2): 
            cmd.linear.x = 1 
        elif min_range > (self.distance*1.8):
            cmd.linear.x = 0.8
        elif min_range > (seld.distance*1.6): 
            cmd.linear.x = 0.6
        elif min_range > (self.distance*1.4): 
            cmd.linear.x = 0.4 
        elif min_range > (self.distance): 
            cmd.linear.x = 0.2 
        elif min_range < (sel.distance): 
            cmd.linear.x = 0
        
        self.publisher.publish(cmd)

    def callback_2(self,msg):
        self.distance = msg.data




if __name__ == '__main__':
    # used publisher and subsriber noted in rob599_basic to write this 
    rospy.init_node('stop_node', argv=sys.argv)
    stoping = StopFetch()
    rospy.spin(StopFetch)