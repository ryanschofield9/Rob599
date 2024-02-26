import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from cv_bridge.core import CvBridge
import cv2 
import numpy as np

# used this website to help figure out how to publish images https://answers.ros.org/question/359029/how-to-publish-batch-of-images-in-a-python-node-with-ros-2/
class ImagePub(Node):
    def __init__(self):
        super().__init__('image_pub')
        self.pub = self.create_publisher(Image, 'palm_camera/image_rect_color', 10)
        self.timer = self.create_timer(5, self.callback)
        self.image = cv2.imread('/home/ryan/ros2_ws_applecontroller/src/applevision_vision/applevision_vision/apple.jpg')
        self.bridge= CvBridge()

    def callback(self):
        self.pub.publish(self.bridge.cv2_to_imgmsg(np.array(self.image),"bgr8" ))
        self.get_logger().info('Publishing an image')

def main(args=None):
    rclpy.init(args=args)
    image_pub = ImagePub()
    rclpy.spin(image_pub)
    rclpy.shutdown ()

if __name__ == '__main__':
   main()