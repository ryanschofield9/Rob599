import rclpy 
from rclpy.node import Node 

from applecontroller_msgs.srv import Distance
from std_msgs.msg import Int64

import time 

#used examples in github for structure 
class DistanceService(Node):
    def __init__(self):
        super().__init__('service_distance')
        self.service = self.create_service(Distance, 'distance', self.callback)
        self.pub = self.create_publisher(Int64, 'distance_request', 10)

    def callback(self, request, response):
        self.get_logger().info(f"Got: {request.data}")
        msg = Int64()
        msg.data = request.data
        for i in range(10): 
            self.pub.publish(msg) 
            time.sleep(0.1)

        response.returned == True
        
        return response
def main():
    rclpy.init()
    distance=DistanceService()
    rclpy.spin(distance)
    rclpy.shutdown()

if __name__ == '__main__':
    main()