import rclpy 
from rclpy.node import Node 

from rob599_hw3_msgs.srv import Door
from rclpy.action import ActionClient

from rob599_hw3_msgs.action import Roam

import time

#used publisher.py in rob599r2 github to help structure how I do this 
#used examples in github for structure 
class KnockKnock(Node): 
    def __init__(self):
        super().__init__('knock_client')

        #create service client 
        self.client = self.create_client(Door, 'knock_knock')
        while not self.client.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service to start')

    def send(self):
        request = Door.Request()
        request.input = True
        self.response = self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    knock=KnockKnock()

    time.sleep (2)
    knock.send()
    rclpy.spin(knock)


if __name__ == '__main__':
    main()    
        