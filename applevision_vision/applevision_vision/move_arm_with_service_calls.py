import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Int64, Float32
from geometry_msgs.msg import TwistStamped, Vector3
from applecontroller_msgs.srv import Speed, Distance


class MoveArm(Node):
    def __init__(self):
        super().__init__('move_arm')
         # create publishers and subscripers (and timers as necessary )
        self.sub_x = self.create_subscription(Int64, 'x_centered', self.callback_x, 10)
        self.sub_speed = self.create_subscription(Float32, 'speed_request', self.callback_speed, 10)
        self.sub_distance = self.create_subscription(Int64, 'distance_request', self.callback_distance, 10)
        self.sub_y = self.create_subscription(Int64, 'y_centered', self.callback_y, 10)
        self.sub_tof = self.create_subscription(Int64, 'tof_fake', self.callback_tof, 10)
        self.pub = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds', 10)
        self.pub_timer = self.create_timer(1/10, self.publish_twist)

        #Create a service 
        #Speed Service
        self.client_speed = self.create_client(Speed, 'speed')
        while not self.client_speed.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service to start')
        #Distance Service
        self.client_distance = self.create_client(Distance, 'distance')
        while not self.client_distance.wait_for_service(timeout_sec=1):
            self.get_logger().info('waiting for service to start')

        #variables needed 
        self.centered = False
        self.y_centered = 0 
        self.speed = 0.0
        self.distance = 20
        self.x_centered = 0 
        self.count = 0 
        self.tof = 0

        #make service call 
        request = Speed.Request()
        request.data = 0.1
        response = self.client_speed.call_async(request)

        request = Distance.Request()
        request.data = 20
        response = self.client_distance.call_async(request)

    def publish_twist(self):

        my_twist_linear = [0.0, 0.0, 0.0] 
        my_twist_angular = [0.0, 0.0, 0.0]

        # positive y makes it go down 
        # negative y makes it go up

        # sif the apple is centered and has been centered for about 3.5 seconds 
        if self.centered == False or self.count < 35: 
            # set twist messages to send
            if self.x_centered == 0: 
                    
                my_twist_linear[0]= 0.0
            
            elif self.x_centered == -1 : 
                my_twist_linear[0] = self.speed 
            
            else: 
                my_twist_linear[0] = -1*self.speed 
                    
            if self.y_centered == 0: 
                my_twist_linear[1] = 0.0

            elif self.y_centered == -1:
                my_twist_linear[1] = -1 * self.speed 
            
            else: 
                my_twist_linear[1] = self.speed 
            
            if self.x_centered == 0 and self.y_centered == 0: 
                self.centered = True
                self.count = self.count + 1
            else: 
                self.centered = False 
                self.count = 0 
        # if the apple is centered and has been for about 1.5 seconds start to moving forward  
        else: 
            if self.tof >self.distance:
                my_twist_linear[2] = self.speed 
            else:    
                print("done")
            
        cmd = TwistStamped()
        cmd.header.frame_id = 'tool0'
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.twist.linear = Vector3(x=my_twist_linear[0], y=my_twist_linear[1], z=my_twist_linear[2])
        cmd.twist.angular = Vector3(x=my_twist_angular[0], y=my_twist_angular[1], z=my_twist_angular[2])
        self.get_logger().info(f"Sending: linear: {cmd.twist.linear} angular: {cmd.twist.angular}")

        self.pub.publish(cmd)
    
    def callback_x (self, msg):
        self.x_centered = msg.data 
    
    def callback_y (self, msg):
        self.y_centered = msg.data
    
    def callback_speed (self, msg):
        self.speed = msg.data 
        print(f"Set speed to be: {msg.data}")

    def callback_distance (self, msg):
        self.distance = msg.data 
        print(f"Set distance to be: {msg.data}")
    
    def callback_tof (self, msg):
        self.tof = msg.data

def main(args=None):
    rclpy.init(args=args)
    move = MoveArm()
    rclpy.spin(move)
    rclpy.shutdown ()

if __name__ == '__main__':
   main()
