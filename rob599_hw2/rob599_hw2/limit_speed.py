import rclpy 
from rclpy.node import Node 

from geometry_msgs.msg import Twist, Vector3 

#used publisher.py in rob599r2 github to help structure how I do this 
class SpeedLimit(Node): 
    def __init__(self):
        super().__init__('speed_limit')
        self.pub = self.create_publisher(Twist, 'speed_out',10)
        self.timer=self.create_timer(1, self.publish_twist)
        self.sub = self.create_subscription(Twist, 'speed_in', self.callback, 10)

        #Creating parameters 
        self.declare_parameter('linear_max',8.0)
        self.declare_parameter('angular_max', 8.0)
        self.timer_2 = self.create_timer(1, self.callback_2)

        #setting up inital variables 
        self.linear = Vector3(x=0.0, y=0.0, z=0.0)  
        self.angular = Vector3(x=0.0, y=0.0, z=0.0)
        self.linear_contraint = 8.0
        self.angular_contraint = 8.0

    
    def publish_twist(self):

        # What is meant by absolute value? assume check each individual x, y,z and make sure that no value is larger than the constraint and if it is then reduce to the contraint value 
        #alternative meaning: the square root of all the values can't 
        cmd = Twist()
        cmd.linear = self.linear
        cmd.angular = self.angular
        #check that they are within the abs constraint 
        if abs(cmd.linear.x) > self.linear_contraint:
            cmd.linear.x = cmd.linear.x * (self.linear_contraint/abs(cmd.linear.x))
        if abs(cmd.linear.y) > self.linear_contraint:
            cmd.linear.y = cmd.linear.y * (self.linear_contraint/abs(cmd.linear.y))
        if abs(cmd.linear.z) > self.linear_contraint:
            cmd.linear.z = cmd.linear.z * (self.linear_contraint/abs(cmd.linear.z))
        if abs(cmd.angular.x) > self.angular_contraint:
            cmd.angular.x = cmd.angular.x *(self.angular_contraint/abs(cmd.angular.x))
        if abs(cmd.angular.y) > self.angular_contraint:
            cmd.angular.y = cmd.angular.y *(self.angular_contraint/abs(cmd.angular.y))
        if abs(cmd.angular.z) > self.angular_contraint:
            cmd.angular.z = cmd.angular.z *(self.angular_contraint/abs(cmd.angular.z))

        self.get_logger().info(f"Sending linear: {cmd.linear} angular: {cmd.angular}")
        self.pub.publish(cmd)
        
    def callback(self, msg):
        self.get_logger().info(f"Got linear: {msg.linear} angular: {msg.angular}")
        self.linear = Vector3(x=msg.linear.x, y=msg.linear.y, z=msg.linear.z)
        self.angular = Vector3(x=msg.angular.x, y=msg.angular.y, z=msg.angular.z)

    
    def callback_2(self):
        self.linear_contraint = self.get_parameter('linear_max').get_parameter_value().double_value
        self.angular_contraint = self.get_parameter('angular_max').get_parameter_value().double_value




def main(args=None):
   rclpy.init(args=args)
   speed_limit = SpeedLimit()
   rclpy.spin(speed_limit)
   rclpy.shutdown()

if __name__ == '__main__':
   main()

