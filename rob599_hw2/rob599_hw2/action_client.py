import rclpy 
from rclpy.node import Node 
from rclpy.action import ActionClient

from rob599_hw2_msgs.action import Nasa 

import time

#used examples in github for structure 
class NasaActonClient(Node):
    def __init__(self):
        super().__init__('Nasa_client')

        self.client = ActionClient(self, Nasa, 'nasa')

    def send(self,seconds):
        goal = Nasa.Goal()
        goal.seconds = seconds

        self.client.wait_for_server()

        self.result = self.client.send_goal_async(goal,feedback_callback=self.feedback)

        self.result.add_done_callback(self.done)

    def feedback(self,feedback):
        self.get_logger().info(f'{feedback.feedback.progress}')

    def done (self, result):
        self.get_logger().info('Here')
        goal = result.result()
        self.goal_handle = goal
            
        if not goal.accepted:
            self.get_logger().info('Goal rejected')
            return 
        
        self.timer = self.create_timer(2.0,self.timer_callback)
        self.result_handle = goal.get_result_async()
        self.result_handle.add_done_callback(self.process_result)


    
    def process_result(self,future):
        result = future.result().result
        if result.launch == True:
            self.get_logger().info('The rocket has successfully been launched!')
        else:
             self.get_logger().info('The rocket has NOT been launched.')
    
    #used the following github to structure how to do the canceling (https://github.com/ros2/examples/blob/master/rclpy/actions/minimal_action_client/examples_rclpy_minimal_action_client/client_cancel.py)
    def cancel_done (self,future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling )> 0: 
            self.get_logger().info ('Goal succesfully canceled')
        else:
            self.get_logger().info ('Goal NOT canceled')
        
        rclpy.shutdown()
    
    def timer_callback(self):
        self.get_logger().info('Canceling goal')
        future = self.goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancel_done)
        self.timer.cancel()

        
        
def main(args=None):
    rclpy.init(args=args)

    action_client = NasaActonClient()

    action_client.send(10)

    rclpy.spin(action_client)


# This is the entry point for running the node directly from the command line.
if __name__ == '__main__':
	main()