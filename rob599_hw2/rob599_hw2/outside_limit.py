import rclpy 
from rclpy.node import Node 

from geometry_msgs.msg import Twist, Vector3 

import time 

#used publisher.py in rob599r2 github to help structure how I do this 
#used examples in github for structure 
class OutsideLimit(Node): 
    def __init__(self):
        super().__init__('outside_limit')

        #create subscriber
        self.sub = self.create_subscription(Twist, 'speed_in', self.callback, 10)

        #Creating parameters 
        self.declare_parameter('linear_max',8.0)
        self.declare_parameter('angular_max', 8.0)
        self.timer = self.create_timer(1, self.callback_2)

        self.count = 0 
        self.over = 0 
        self.timer = 30 
        self.linear_constraint = 8.0
        self.angular_constraint = 8.0


    def callback(self, msg):
        
        if self.count == 0: 
            self.start = time.time()
        
        self.count = self.count + 1
        self.linear = Vector3(x=msg.linear.x, y=msg.linear.y, z=msg.linear.z)
        self.angular = Vector3(x=msg.angular.x, y=msg.angular.y, z=msg.angular.z)

        #check if they are within the absolute constraint 
        if abs(self.linear.x) > self.linear_constraint:
            self.over = self.over + 1
        elif abs(self.linear.y) > self.linear_constraint:
            self.over = self.over + 1
        elif abs(self.linear.z) > self.linear_constraint:
            self.over = self.over + 1
        elif abs(self.angular.x) > self.angular_constraint:
            self.over = self.over + 1
        elif abs(self.angular.y) > self.angular_constraint:
            self.over = self.over + 1
        elif abs(self.angular.z) > self.angular_constraint:
            self.over = self.over + 1

        if (time.time() - self.start) >= self.timer: 
            self.per = (self.over /self.count ) * 100
            self.get_logger().info(f"There have been {self.count} messages with {self.over} messages outside the constraint. This is a percentage of {self.per}")
            self.count = 0
            self.over = 0 
    
    
    def callback_2(self):
        self.linear_constraint = self.get_parameter('linear_max').get_parameter_value().double_value
        self.angular_constraint = self.get_parameter('angular_max').get_parameter_value().double_value

def main(args=None):
   rclpy.init(args=args)
   outside_limit = OutsideLimit()
   rclpy.spin(outside_limit)
   rclpy.shutdown()

if __name__ == '__main__':
   main()