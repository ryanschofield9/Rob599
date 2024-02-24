import rclpy 
from rclpy.node import Node 

from geometry_msgs.msg import Twist, Vector3 
import time 
from rob599_hw2_msgs.srv import Brakes

#used publisher.py in rob599r2 github to help structure how I do this 
#used examples in github for structure 
class SpeedLimit(Node): 
    def __init__(self):
        super().__init__('speed_limit')

        #create service 
        self.client = self.create_client(Brakes, 'apply_brakes')
        while not self.client.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service to start')

        
        #create subscriber and publisher 
        self.pub = self.create_publisher(Twist, 'speed_out',10)
        self.timer=self.create_timer(1,self.watch_dog)
        self.sub = self.create_subscription(Twist, 'speed_in', self.callback, 10)

        #Creating parameters 
        self.declare_parameter('linear_max',8.0)
        self.declare_parameter('angular_max', 8.0)
        self.declare_parameter('with_watchdog', False)
        self.declare_parameter('watchdog_period', 30.0)
        self.timer_2 = self.create_timer(1, self.callback_2)

        #setting up inital variables 
        self.linear = Vector3(x=0.0, y=0.0, z=0.0)  
        self.angular = Vector3(x=0.0, y=0.0, z=0.0)
        self.linear_contraint = 8.0
        self.angular_contraint = 8.0
        self.with_watchdog = False 
        self.watchdog_period = 30.0
        self.start = time.time()

        #make service call 
        request = Brakes.Request()
        request.data = False
        self.response = self.client.call_async(request)


    def watch_dog(self):
        if self.with_watchdog == True: 
            if (time.time() -self.start) >= self.watchdog_period:
                self.linear = Vector3(x=0.0, y=0.0, z=0.0)  
                self.angular = Vector3(x=0.0, y=0.0, z=0.0)
                cmd = Twist()
                cmd.linear = self.linear
                cmd.angular = self.angular
                self.get_logger().info(f"Sending linear: {cmd.linear} angular: {cmd.angular}")
                self.pub.publish(cmd)
                self.start = time.time()
        
    def callback(self, msg):
        
        self.get_logger().info(f"Got linear: {msg.linear} angular: {msg.angular}")
        self.linear = Vector3(x=msg.linear.x, y=msg.linear.y, z=msg.linear.z)
        self.angular = Vector3(x=msg.angular.x, y=msg.angular.y, z=msg.angular.z)
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
        self.start = time.time()

    
    def callback_2(self):
        self.linear_contraint = self.get_parameter('linear_max').get_parameter_value().double_value
        self.angular_contraint = self.get_parameter('angular_max').get_parameter_value().double_value
        self.with_watchdog = self.get_parameter('with_watchdog').get_parameter_value().bool_value
        self.watchdog_period = self.get_parameter('watchdog_period').get_parameter_value().double_value



def main(args=None):
   rclpy.init(args=args)
   speed_limit = SpeedLimit()
   rclpy.spin(speed_limit)
   rclpy.shutdown()

if __name__ == '__main__':
   main()

