#!/usr/bin/env python

import rospy 
import sys
import actionlib
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64 
from rob599_hw1.srv import StoppingDistance
from rob599_hw1.msg import StoppingAction, StoppingGoal, StoppingResult



class StopFetch():
    def __init__(self):
        self.distance = 1.0
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        #comment out next line if runnign action (make sure uncommented otherwise)
        self.subscriber = rospy.Subscriber('filter', LaserScan, self.callback)
        
        #comment out next line if running sever or action 
        self.distance = 1.0

        #Uncomment out if running action 
        #self.client= actionlib.SimpleActionClient('stopping_action', StoppingAction)
        #self.client.wait_for_server()
        #goal = StoppingGoal(goal=1.2)
        #self.client.send_goal(goal,done_cb = self.callback_done, active_cb = self.callback_active, feedback_cb=self.callback_feedback )
        #self.count = 0
        #End comments if running action 
        
        #Uncomment out below if running server 
        #self.sub = rospy.Subscriber('distance', Float64, self.callback_2)
        #rospy.wait_for_service("stopping_distance")
        #self.distance_service = rospy.ServiceProxy('stopping_distance', StoppingDistance)
        #self.distance_recieved = self.distance_service(1.2)
        #End comments if runnign server

    def callback(self,msg):
        
        #rospy.loginfo("here")
     


        min_range = min(msg.ranges)
        rospy.loginfo(f"Got {min_range}, {self.distance}")

        cmd = Twist()
        if min_range > (self.distance * 2.0): 
            cmd.linear.x = 1 
        elif min_range > (self.distance*1.8):
            cmd.linear.x = 0.8
        elif min_range > (self.distance*1.6): 
            cmd.linear.x = 0.6
        elif min_range > (self.distance*1.4): 
            cmd.linear.x = 0.4 
        elif min_range > (self.distance): 
            cmd.linear.x = 0.2 
        elif min_range < (self.distance): 
            cmd.linear.x = 0
        
        self.publisher.publish(cmd)

    #def callback_2(self,msg):
        #self.distance = msg.data
        #rospy.loginfo(f"Got {self.distance}" )

    def callback_done(self, status, result):
        cmd = Twist()
        cmd.linear.x = 0
        self.publisher.publish(cmd)
        if status == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal was reached")
        else: 
            rospy.loginfo(f'Goal was not reached.{status}')

    def callback_feedback(self, feedback):
        
        cmd = Twist()
        if self.count < 2:
            cmd.linear.x = 1 
        elif self.count < 4: 
            cmd.linear.x = 0.8
        elif self.count < 6: 
            cmd.linear.x = 0.6
        elif self.count < 10: 
            cmd.linear.x = 0.4
        else:
            cmd.linear.x = 0.2  
        self.publisher.publish(cmd)
        rospy.loginfo(f"The robot is currently at {feedback.dist} ")
        self.count = self.count +1
        

    def callback_active(self):
        rospy.loginfo("in active")



if __name__ == '__main__':
    # used publisher and subsriber noted in rob599_basic to write this 
    #rospy.loginfo("here1")
    rospy.init_node('stop_node', argv=sys.argv)
    stoping = StopFetch()
    rospy.spin()