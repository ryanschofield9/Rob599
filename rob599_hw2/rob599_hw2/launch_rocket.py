import rclpy 
from rclpy.node import Node 

from rob599_hw2_msgs.srv import LaunchRocket
#used examples in github for structure 
class LaunchRockets(Node):
    def __init__(self):
        super().__init__('service_launch_rocket')
        self.service = self.create_service(LaunchRocket, 'launch_rocket', self.callback)

    def callback(self, request, response):
        self.get_logger().info(f'{request.request}')
        if request.request == True: 
            response.success = True
        else: 
            response.success = False
        
        return response
def main():
    rclpy.init()
    launch_rocket=LaunchRockets()
    rclpy.spin(launch_rocket)
    rclpy.shutdown()

if __name__ == '__main__':
    main()