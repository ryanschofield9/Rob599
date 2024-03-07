import rclpy 
from rclpy.node import Node 

from applecontroller_msgs.srv import Speed
from std_msgs.msg import Float32

import time 

#used examples in github for structure 
class SpeedService(Node):
    def __init__(self):
        super().__init__('service_speed')
        self.service = self.create_service(Speed, 'speed', self.callback)
        self.pub = self.create_publisher(Float32, 'speed_request', 10)

    def callback(self, request, response):
        self.get_logger().info(f"Got: {request.data}")
        msg = Float32()
        msg.data = request.data
        for i in range(10): 
            self.pub.publish(msg) 
            time.sleep(0.1)

        response.returned == True
        
        return response
def main():
    rclpy.init()
    speed=SpeedService()
    rclpy.spin(speed)
    rclpy.shutdown()

if __name__ == '__main__':
    main()