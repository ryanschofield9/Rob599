
import rclpy 
from rclpy.node import Node 

from rob599_hw3_msgs.srv import MemorizePosition, ClearPositions, Save, Load, Door
from rob599_hw3_msgs.action import GoTo, Roam

from std_msgs.msg import Bool 
from geometry_msgs.msg import PoseStamped, Pose
from visualization_msgs.msg import Marker


from rclpy.action import ActionServer, ActionClient

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformException
import tf2_geometry_msgs

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration

from rclpy.executors import MultiThreadedExecutor
import threading

import math
import time

import json 

class Memorize(Node):
    def __init__(self):
        super().__init__('services')
        # create services 
        self.memorize_position = self.create_service(MemorizePosition, 'memorize_position', self.memorize_position)
        self.clear_positions = self.create_service(ClearPositions, 'clear_positions', self.clear_positions)
        self.save = self.create_service(Save, 'save', self.save)
        self.load = self.create_service(Load, 'load', self.load)
        self.knock = self.create_service(Door, 'knock_knock', self.knock)

        #create action interfaces 
        self.go_to = ActionServer(self, GoTo, 'go_to', self.go_to)
        self.patrol = ActionServer(self, Roam, 'patrol', self.patrol)

        #action client of go to 
        self.client = ActionClient(self, GoTo, 'go_to')


        #setup to be able to get current position 
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        #setup dictionary, list, and other needed variables 
        self.locations = {}
        self.count = 1
        #self.count_text = 1
        self.places = []

        #setup publishers 
        self.pub = self.create_publisher(Marker, 'locations',10 )
        self.pub_2 = self.create_publisher(Marker, 'text',10 )

        #setup navigation 
        self.navigator=BasicNavigator()

        self.done= False
        self.count_patrol = 0
        self.wait = False 

        self._goal_lock = threading.Lock()
        self._goal_handle = None

        self.pub_3 = self.create_publisher(Bool, 'loaded_file',10)

    #function for memorize_position service 
    def memorize_position(self, request, response):

        self.get_logger().info(f'{request.place}')
        self.places.append(request.place)

        #find current position 
        cur_pos = self.get_current_pose()
        self.get_logger().info(f'current pos in map frame: {cur_pos.position.x}')

        #add position to dictonary with string in request as the key 
        self.locations[request.place] = (cur_pos.position.x, cur_pos.position.y, cur_pos.position.z, cur_pos.orientation.x , cur_pos.orientation.y, cur_pos.orientation.z, cur_pos.orientation.w)

        #add a marker to that location 
        self.add_marker(cur_pos, request.place)

        response.x = cur_pos.position.x
        response.y = cur_pos.position.y

        return response
    
    #function for clear_position service 
    def clear_positions(self, request, response): 
        if request.clear: 
            for x in range(len(self.locations.keys())): 
                #clear marker
                marker = Marker()
                marker.header.frame_id = 'map'
                marker.id =  self.count -1 
                marker.action = Marker.DELETE

                text = Marker()
                text.header.frame_id = 'map'
                text.id = self.count - 1
                text.action = text.DELETE

                self.count -= 1  
                
                #clear values in dictionary 
                del self.locations[self.places[self.count - 1]]
                self.pub.publish(marker)
                self.pub_2.publish(text)
            
            self.places = []

        response.result = request.clear
        return response

    #function for save service 
    def save(self, request, response): 
        file = request.file 
        try: 
            #used the following link to write a dictionary to a file https://www.geeksforgeeks.org/write-a-dictionary-to-a-file-in-python/
            with open(file, 'w') as save_to: 
                save_to.write(json.dumps(self.locations))

            response.result = True
        except: 
            response.result = False
        return response
    
    #function for load service 
    def load (self, request, response):
        print("request recieved")
        file = request.file 
        msg = Bool()
        try: 
                #used the following link to read a dictionary to a file https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
            with open(file) as read_from: 
                data = read_from.read() 
                    
            places = json.loads(data) 
            print(f'Places:{places}')
            for key, vals in places.items():
                    #add the dictionary loaded in into the dictionary saved in class 
                self.locations[key] = vals 
                self.places.append(key)

                    #add markers for the locations given in loaded dictionary 
                pos = Pose() 
                pos.position.x = vals[0]
                pos.position.y = vals[1]
                pos.position.z = vals[2]
                pos.orientation.x = vals[3]
                pos.orientation.y = vals[4]
                pos.orientation.z = vals[5]
                pos.orientation.w = vals[6]

                self.add_marker(pos,key)
            response.result = True 
            self.loaded = True  
            msg.data = True 
        
        except: 
            self.get_logger().info("The file you gave does not work.")
            response.result = False
            msg.data = False
            
        self.pub_3.publish(msg)
       
        return response 
    
    #function for knock knock server  
    def knock(self, request, response):
        #cancel current goal 
        self.navigator.cancelTask()
        self.wait = True 
        self.get_logger().info('There was a knock at the door. I must go see who it is.')
        self.send_to_location('door')
        time.sleep(0.5)
        while not self.navigator.isTaskComplete():
            self.get_logger().info("Still headed to door")
            time.sleep(0.5)

        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info('At Front Door')
            self.joke()
            response.result = True
        else:
            self.get_logger().info('Could not get to the front door')
            response.result = False
        self.wait = False         

        return response

    
    #create action server go_to
    def go_to(self,goal): 
        self.get_logger().info(f'Got a request to go to the following location: {goal.request.location}')

        #Calculate and send feedback 
        feedback = GoTo.Feedback()
        result = GoTo.Result()
        location = goal.request.location 
        try: 
            self.send_to_location(location)
            
            while not self.navigator.isTaskComplete():
                location = goal.request.location 
                distance = self.distance(location)

                feedback.distance = distance
                feedback.location = location
                goal.publish_feedback(feedback)

                time.sleep(1)

            if self.navigator.getResult() == TaskResult.SUCCEEDED:
                goal.succeed()
                result.result = True
                self.get_logger().info('The Location has been reached')
            else:
                result.result = False 
                self.get_logger().info('The location can not be reached and may not be valid location')
        except: 
            result.result = False 
            self.get_logger().info('The location can not be reached and may not be valid location')

        return result 
    
    #create action server patrol 
    def patrol (self, goal): 
        self.get_logger().info('Starting Patrol')
        result = Roam.Result()
        feedback = Roam.Feedback()
        while self.count_patrol < (len(self.locations.keys())):
            if not self.wait: 
                if self.places[self.count_patrol] != 'door':
                    self.send_to_location(self.places[self.count_patrol])
                    while not self.navigator.isTaskComplete():
                        feedback.location = self.places[self.count_patrol]
                        goal.publish_feedback(feedback)
                        time.sleep(1)
                self.count_patrol += 1
            elif self.wait:
                while self.wait:
                    time.sleep(0.5)
                self.count_patrol -= 1

        result.result = True 
        return result 

    def handle_accepted_callback(self, goal_handle):
        with self._goal_lock:
            # This server only allows one goal at a time
            if self._goal_handle is not None and self._goal_handle.is_active:
                self.get_logger().info('Aborting previous goal')
                # Abort the existing goal
                self._goal_handle.abort()
            self._goal_handle = goal_handle

        goal_handle.execute()

    # used breadcrumbs example to structure how I was doing this 
    def get_current_pose(self): 
        pt = PoseStamped()
        pt.header.frame_id = 'base_link'

        #current position in base_link is 0 ,0,0
        pt.pose.position.x = 0.0
        pt.pose.position.y = 0.0
        pt.pose.position.z = 0.0

        pt.pose.orientation.x = 0.0
        pt.pose.orientation.y = 0.0
        pt.pose.orientation.z = 0.0
        pt.pose.orientation.w = 1.0

        new_pose = self.tf_buffer.transform(pt,'map', rclpy.duration.Duration(seconds=1))
        return new_pose.pose

    def add_marker(self, cur_pos, location):
        #Add spot marker
        marker = Marker()
        marker.header.frame_id = 'map'

        marker.id =  self.count 
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        pose = cur_pos
        marker.pose = pose 

        #Add text marker 
        text = Marker()
        text.header.frame_id = 'map'
        text.id =  self.count
        text.type = text.TEXT_VIEW_FACING
        text.action = text.ADD

        text.text = location
        
        text.scale.z = 0.2

        text.color.r = 0.0
        text.color.b = 1.0
        text.color.g = 0.0
        text.color.a = 0.8

        text.pose = pose

        self.count += 1
        print (self.count)

        self.pub_2.publish(text)
        self.pub.publish(marker)


        return 

    def distance(self, location):
        #get x and y goal positions 
        place = self.locations[location]
        x_goal = place[0]
        y_goal = place[1]

        #get x and y current positions 
        cur_pos = self.get_current_pose()
        x = cur_pos.position.x 
        y = cur_pos.position.y

        #calculate distance 
        distance = math.sqrt(pow((x_goal-x),2)+pow((y_goal-y),2) )
        return distance 
    
    def send_to_location (self, location):
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        #try: 
        place = self.locations[location]
        goal_pose.pose.position.x = place[0]
        goal_pose.pose.position.y = place[1]
        goal_pose.pose.position.z = place[2]
        goal_pose.pose.orientation.x = place[3]
        goal_pose.pose.orientation.y = place[4]
        goal_pose.pose.orientation.z = place[5]
        goal_pose.pose.orientation.w = place[6]

        self.navigator.goToPose(goal_pose)
        #except: 
           
            #goal_pose.pose = self.get_current_pose()
            
        return 
    
    #Functions below are for the action call to GoTo
    def feedback(self,feedback):
        self.get_logger().info(f'Currently {feedback.feedback.distacne}m from the {feedback.feedback.location}')

    def joke (self):
        joke = input('Would you like to hear a knock knock joke?')
        if joke == 'yes' or joke =='Yes': 
            self.get_logger().info("Knock Knock ")
            input('Enter next line: ')
            self.get_logger().info("Jewel ")
            input('Enter next line: ')
            self.get_logger().info("Jewel be happy to know its Friday!")
            self.get_logger().info("HAHAHA")
        else: 
            self.get_logger().info("Ok no joke")
        


        
def main(args=None):
    rclpy.init(args=args)
    memorize=Memorize()
    executor = MultiThreadedExecutor()
    rclpy.spin(memorize, executor=executor)
    rclpy.shutdown()

if __name__ == '__main__':
    main()