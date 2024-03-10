import rclpy 
from rclpy.node import Node 
from rclpy.action import ActionClient

from rob599_hw3_msgs.action import GoTo 
from rob599_hw3_msgs.srv import Load

from std_msgs.msg import Bool

import time


#used examples in github for structure 
class GoToActonClient(Node):
    def __init__(self):
        super().__init__('GoTo_Client')

        self.client = ActionClient(self, GoTo, 'go_to')

        self.client_2= self.create_client(Load, 'load')
        while not self.client_2.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service load to start')
        self.loaded = False 

                                            
        self.finished = True 


    def send(self,location):
        self.finished = False
        goal = GoTo.Goal()
        goal.location = location

        self.client.wait_for_server()

        self.result = self.client.send_goal_async(goal,feedback_callback=self.feedback)

        self.result.add_done_callback(self.done)

        #return self.result


    def feedback(self,feedback):
        self.get_logger().info(f'You are {feedback.feedback.distance}m from {feedback.feedback.location}')

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
            self.get_logger().info('The desired location has been reached')
        else:
             self.get_logger().info('The desired location has NOT been reached and may not be a valid location or the file name was bad')
        self.finished = True

    def load (self):
        while not self.loaded:
            file = input("Enter the file path to load your locations from: ")
            try: 
                request = Load.Request()
                request.file = file 
                self.future = self.client_2.call_async(request)
                self.get_logger().info("The file you gave may have been loaded. Check services messages to see if there was an error")
                self.loaded = True
            except: 
                self.get_logger().info("The file you gave does not work. Please enter another file") 
            
        
def main(args=None):
    rclpy.init(args=args)

    go_to = GoToActonClient()

    go_to.load()

    
    location = input("Please enter the name of the locaion that you want to go to: ")
            
    go_to.send(location)

    rclpy.spin(go_to)



# This is the entry point for running the node directly from the command line.
if __name__ == '__main__':
	main()