import rclpy 
from rclpy.node import Node 
from rclpy.action import ActionClient

from rob599_hw3_msgs.action import Roam
from rob599_hw3_msgs.srv import Load

import time


#used examples in github for structure 
class Patrol(Node):
    def __init__(self):
        super().__init__('Patrol_client')

        self.client = ActionClient(self, Roam, 'patrol')

        self.client_2= self.create_client(Load, 'load')
        while not self.client_2.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service load to start')
        self.loaded = False

    def send(self):

        goal = Roam.Goal()
        goal.patrol = True
        self.client.wait_for_server()

        self.result = self.client.send_goal_async(goal, feedback_callback=self.feedback)

        #self.result.add_done_callback(self.done)

    def feedback(self,feedback):
        self.get_logger().info(f'Currently headed to the {feedback.feedback.location}')

    def done (self, result):
        goal = result.result()
        self.goal_handle = goal
            
        if not goal.accepted:
            self.get_logger().info('Goal rejected')
            return 
        
        self.result_handle = goal.get_result_async()
        self.result_handle.add_done_callback(self.process_result)
    
    def process_result(self,future):
        result = future.result().result
        if result.result == True:
            self.get_logger().info('The Patrol is complete')
        else:
             self.get_logger().info('The Patrol was not able to be finished ')
    
    def load (self):
        while not self.loaded:
            file = input("Enter the file path to load your locations from: ")
            try: 
                request = Load.Request()
                request.file = file 
                self.future = self.client_2.call_async(request)
                self.get_logger().info("The file you gave has been loaded")
                self.loaded = True
            except: 
                self.get_logger().info("The file you gave does not work. Please enter another file") 
            
        
def main(args=None):
    rclpy.init(args=args)
    patrol = Patrol()
    patrol.load()
    patrol.send()

    rclpy.spin(patrol)


# This is the entry point for running the node directly from the command line.
if __name__ == '__main__':
	main()