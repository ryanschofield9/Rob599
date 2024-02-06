import rospy 
import sys
from sensor_msgs.msg import LaserScan
import math 


def callback(msg):
    
    
    front = msg.ranges[0]
    angle = math.atan (0.5/front)
    

    min_angle = (msg.angle_min) 
    ang_not_used = abs(round((min_angle -(-angle) )/ msg.angle_increment))

    ang_used = abs(round(angle*2 / msg.angle_increment))
    
    # used https://www.geeksforgeeks.org/python-k-middle-elements/ to help figure out how to do this in python
    start_idx = ang_not_used 
    end_idx = ang_not_used + ang_used

    ranges = msg.ranges[start_idx: end_idx]
    
    
    filter_msg = LaserScan()
    filter_msg= msg
    filter_msg.ranges = ranges
    filter_msg.angle_min = -angle 
    filter_msg.angle_max = angle


    
    rospy.loginfo(f"angle {front}")

    publisher.publish(filter_msg)



if __name__ == '__main__':
    # used publisher and subsriber noted in rob599_basic to write this 
    rospy.init_node('filter_node', argv=sys.argv)
    
    publisher = rospy.Publisher('filter', LaserScan, queue_size=10)
    subscriber = rospy.Subscriber('base_scan', LaserScan, callback)
    rospy.spin()