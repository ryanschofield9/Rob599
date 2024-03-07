import rclpy 
from rclpy.node import Node 

from std_msgs.msg import Int64

#used publisher.py in rob599r2 github to help structure how I do this 
#used examples in github for structure 
class TOFData(Node): 
    def __init__(self):
        super().__init__('tof')
        self.pub = self.create_publisher(Int64, 'tof_fake',10)
        self.timer=self.create_timer(1, self.publish_tof)
        self.count = 50
    
    def publish_tof(self):
        msg = Int64()
        if self.count > 0:
            msg.data = self.count 
            self.get_logger().info(f"Sending tof data: {msg.data} ")
            self.pub.publish(msg)
            self.count = self.count - 1
        else: 
            msg.data = self.count 
            self.get_logger().info(f"Sending tof data: {msg.data} ")
            self.pub.publish(msg)

        
def main(args=None):
   rclpy.init(args=args)
   tof = TOFData()
   rclpy.spin(tof)
   rclpy.shutdown()

if __name__ == '__main__':
   main()