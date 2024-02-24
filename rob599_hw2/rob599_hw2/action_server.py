import rclpy 
from rclpy.node import Node 
from rclpy.action import ActionServer, CancelResponse

from rob599_hw2_msgs.action import Nasa 
from rob599_hw2_msgs.srv import LaunchRocket

import time 

from rclpy.executors import MultiThreadedExecutor
#used examples in github for structure 
class NasaActionServer(Node):
    def __init__(self):
       super().__init__('Nasa_server')

       self.server = ActionServer(self, Nasa, 'nasa', self.callback,cancel_callback=self.cancel_callback)
       self.client = self.create_client(LaunchRocket, 'launch_rocket')
       while not self.client.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service to start')
    
    def callback(self, goal): 
        self.get_logger().info(f'Got a request to launch the rocket in {goal.request.seconds} seconds')

        result = Nasa.Result()
        feedback = Nasa.Feedback()
        seconds = goal.request.seconds 
        feedback.progress = seconds
        goal.publish_feedback(feedback)
        while  seconds != 0: 
            if goal.is_cancel_requested:
                 goal.canceled()
                 self.get_logger().info('Launch Aborted')
                 return Nasa.Result(launch=False)
            else: 
                time.sleep(1)
                seconds = seconds - 1
                feedback.progress = seconds 
                goal.publish_feedback(feedback)
        

        request = LaunchRocket.Request()
        request.request = True
        launch_rocket_response = self.client.call_async(request)
        
        result.launch = True
        goal.succeed()
        self.get_logger().info('The rocket has been launched!')
        return result 
    
    def cancel_callback(self,goal):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    
   
         
         

def main(args=None):
    rclpy.init(args=args)
     
    action_server = NasaActionServer()
    
    executor = MultiThreadedExecutor()
    
    rclpy.spin(action_server, executor=executor)

    action_server.destroy()

    rclpy.shutdown()


# This is the entry point for running the node directly from the command line.
if __name__ == '__main__':
	main()
        

            
 