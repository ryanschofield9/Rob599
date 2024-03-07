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
        self.timer = self.create_timer(1, self.callback)
        self.image_center = cv2.imread('/home/ryan/ros2_ws_applecontroller/src/applevision_vision/applevision_vision/apple.jpg')
        self.image_right = cv2.imread('/home/ryan/ros2_ws_applecontroller/src/applevision_vision/applevision_vision/apple_right.jpg')
        self.image_left = cv2.imread('/home/ryan/ros2_ws_applecontroller/src/applevision_vision/applevision_vision/apple_left.jpg')
        self.count = 0 
        self.bridge= CvBridge()

    def callback(self):
        if self.count < 6: 
            self.pub.publish(self.bridge.cv2_to_imgmsg(np.array(self.image_left),"bgr8" ))
            self.get_logger().info('Publishing an image that is left')
        elif self.count < 11: 
            self.pub.publish(self.bridge.cv2_to_imgmsg(np.array(self.image_right),"bgr8" ))
            self.get_logger().info('Publishing an image that is right')
        else: 
            self.pub.publish(self.bridge.cv2_to_imgmsg(np.array(self.image_center),"bgr8" ))
            self.get_logger().info('Publishing an image that is center')
        self.count = self.count + 1 



def main(args=None):
    rclpy.init(args=args)
    image_pub = ImagePub()
    rclpy.spin(image_pub)
    rclpy.shutdown ()

if __name__ == '__main__':
   main()