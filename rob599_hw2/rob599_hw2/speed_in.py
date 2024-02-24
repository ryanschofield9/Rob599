import rclpy 
from rclpy.node import Node 

from geometry_msgs.msg import Twist, Vector3 
from std_msgs.msg import Bool

#used publisher.py in rob599r2 github to help structure how I do this 
#used examples in github for structure 
class SpeedIn(Node): 
    def __init__(self):
        super().__init__('speed')
        self.pub = self.create_publisher(Twist, 'speed_in',10)
        self.timer=self.create_timer(1, self.publish_twist)
        self.sub = self.create_subscription(Bool, 'service_active', self.callback, 10)
        self.count = 0.0
        self.service_active = True
    
    def publish_twist(self):
       
        if self.service_active == False: 

            my_twist_linear = [self.count, self.count, self.count]
            my_twist_angular = [self.count+1, self.count+1, self.count+1]

            cmd = Twist()
            cmd.linear = Vector3(x=my_twist_linear[0], y=my_twist_linear[1], z=my_twist_linear[2])
            cmd.angular = Vector3(x=my_twist_angular[0], y=my_twist_angular[1], z=my_twist_angular[2])
            #self.get_logger().info(f"Sending linear: {cmd.linear} angular: {cmd.angular}")
            self.pub.publish(cmd)
            self.count = self.count + 1

            if self.count > 15.0: 
                self.count = -15.0

    def callback(self,msg):
        self.service_active = msg.data
        
def main(args=None):
   rclpy.init(args=args)
   speed = SpeedIn()
   rclpy.spin(speed)
   rclpy.shutdown()

if __name__ == '__main__':
   main()

       