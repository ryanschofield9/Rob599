#!/usr/bin/env python

import rospy 
import actionlib 
import sys
import time 

from sensor_msgs.msg import LaserScan
from rob599_hw1.msg import StoppingAction, StoppingGoal, StoppingFeedback, StoppingResult

class ActionServer():
    def __init__(self):
        self.server= actionlib.SimpleActionServer('stopping_action', StoppingAction, self.callback, False)
        self.server.start()
        rospy.loginfo('Stopping action server started')
        self.subscriber = rospy.Subscriber('filter', LaserScan, self.callback_2)
        self.current_dist = 7.0

    def callback(self,goal):
        result = False 
        while (result == False):
            self.server.publish_feedback(StoppingFeedback(dist=self.current_dist))
            if self.server.is_new_goal_available():
                self.server.setpreemted(StoppingResult(result=result))
                return 
            if self.current_dist <= goal.goal: 
                result = True 
            time.sleep(0.1)
        print("out")
        self.server.set_succeeded(StoppingResult(result=result))

    def callback_2(self, msg):
        self.current_dist = min(msg.ranges) 

#used github exampel action_server.py to help write this 
if __name__ == '__main__':
    rospy.init_node('action', argv=sys.argv)
    action=ActionServer()

    rospy.spin()