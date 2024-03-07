import rclpy 
from rclpy.node import Node 
from applecontroller_msgs.msg import RegionOfInterestWithConfidenceStamped
from std_msgs.msg import Int64

class FindCenter(Node):
    def __init__(self):
        super().__init__('center_info')
        self.sub = self.create_subscription(RegionOfInterestWithConfidenceStamped, 'applevision/apple_camera', self.find_center, 20)
        self.pub_x = self.create_publisher(Int64, 'x_centered', 10)
        self.pub_y = self.create_publisher(Int64, 'y_centered', 10)
    
    def find_center(self,msg):
        x = msg.x 
        y = msg.y 
        w = msg.w 
        h = msg.h 
        image_w = msg.image_w
        image_h = msg.image_h
        print(f"x: {x}")
        print(f"w: {w}")

        center_x = x + (w/2)
        print(f"center_x: {center_x}")
        center_y = y+ (h/2) 
        im_center_x = image_w/2
        im_center_y = image_h/2 
        print(f"apple box center:({center_x}, {center_y})")
        print(f"image center({im_center_x}, {im_center_y})")
        if abs(im_center_x - center_x) < 20:
            x_val = 0
            print("X is center ")
        elif im_center_x - center_x > 0 :
            x_val = -1 
            print("X is left")
        else: 
            x_val = 1 
            print("X is right")
        
        if abs(im_center_y - center_y) < 8.5:
            y_val = 0
            print("Y is center") 
        elif im_center_y - center_y > 0 : 
            y_val = -1  
            print("Y is down") 
        else: 
            y_val = 1
            ("Y is up")
        
        print (f"X is {x_val} and Y is {y_val}")
        x_centered = Int64()
        x_centered.data = x_val
        y_centered= Int64()
        y_centered.data = y_val
        self.pub_x.publish(x_centered) 
        self.pub_y.publish(y_centered)
        print(f"Publishing x_centered: {x_centered.data} and y_centered: {y_centered.data}")           
            

def main(args=None):
    rclpy.init(args=args)

    # TODO: add image_proc
    find = FindCenter()

    rclpy.spin(find)
    rclpy.shutdown()

if __name__ == '__main__':
    main()