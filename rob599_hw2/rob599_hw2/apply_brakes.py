import rclpy 
from rclpy.node import Node 

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Bool
import time 

from rob599_hw2_msgs.srv import Brakes

#used examples in github for structure 
class ApplyBrakes(Node):
    def __init__(self):
        super().__init__('service')
        self.service = self.create_service(Brakes, 'apply_brakes', self.callback)
        self.pub = self.create_publisher(Twist, 'speed_in',10)
        self.pub_2 = self.create_publisher(Bool, 'service_active',10)

    def callback(self, request, response):
        self.get_logger().info(f"in Function: {request.data}")
        while request.data == True:
            self.get_logger().info(f"Here")
            self.linear = Vector3(x=0.0, y=0.0, z=0.0)  
            self.angular = Vector3(x=0.0, y=0.0, z=0.0)
            cmd = Twist()
            cmd.linear = self.linear
            cmd.angular = self.angular
            self.get_logger().info(f"Sending linear: {cmd.linear} angular: {cmd.angular}")
            self.pub.publish(cmd)
            time.sleep(.1)
        
        response.returned = False
        msg = Bool()
        msg.data = False
        self.pub_2.publish(msg) 
        
        return response
def main():
    rclpy.init()
    apply_brakes=ApplyBrakes()
    rclpy.spin(apply_brakes)
    rclpy.shutdown()

if __name__ == '__main__':
    main()