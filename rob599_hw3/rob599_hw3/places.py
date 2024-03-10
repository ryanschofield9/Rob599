
import rclpy 
from rclpy.node import Node 

from rob599_hw3_msgs.srv import MemorizePosition, ClearPositions, Save, Load

#used examples in github for structure 
class Places(Node):
    def __init__(self):
        super().__init__('places')

        #create services  
        self.client = self.create_client(MemorizePosition, 'memorize_position')
        while not self.client.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service memorize position to start')

        self.client_2 = self.create_client(ClearPositions, 'clear_positions')
        while not self.client_2.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service clear positions to start')

        self.client_3 = self.create_client(Save, 'save')
        while not self.client_3.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service save to start')

        self.client_4 = self.create_client(Load, 'load')
        while not self.client_4.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service load to start')
        
        #create a timer to run the program 
        self.timer = self.create_timer(1, self.callback)

        #load any locations in from a file
        self.load()
        
    def callback(self):
            self.send_request()

    def send_request(self):
        location = input("Enter the name of your current location (type 'done' if you want to clear all positions or save if you want to save your current locations): ")
        if location == 'done' or location == 'Done':
            request = ClearPositions.Request()
            request.clear = True
            self.future = self.client_2.call_async(request)
            self.done = True 
            return 
        elif location == 'save' or location == 'Save':
            self.save()
        else: 
            request = MemorizePosition.Request()
            request.place = location
            self.future = self.client.call_async(request)
            return 
    
    def save (self):
        file = input("Enter the file path to save your current locations to: ")
        try: 
            request = Save.Request()
            request .file = file 
            self.future = self.client_3.call_async(request)
        except: 
            self.get_logger().info("The file you gave does not work, the locations were not saved") 
    
    def load(self): 
        want_to_load = input("Would you like to load a file of locations(type yes or no): ")
        if want_to_load == 'Yes' or want_to_load == 'yes':
            file = input("Enter the file path to load your locations from: ")
            try: 
                request = Load.Request()
                request.file = file 
                self.future = self.client_4.call_async(request)
                self.get_logger().info("The file you gave has been loaded")
            except: 
                self.get_logger().info("The file you gave does not work, the locations were  not loaded") 
        elif want_to_load == 'No' or want_to_load == 'no':
            self.get_logger().info("No locations are going to be loaded ")
        else: 
            self.get_logger().info("You did not enter yes or no and no file will be loaded ")



        
def main(args=None):
    rclpy.init(args=args)
    places=Places()
    rclpy.spin(places)
    
    #rclpy.shutdown()

if __name__ == '__main__':
    main()
