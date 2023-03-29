import cv2
import rospy
import socket
import rospy
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
from image_geometry import PinholeCameraModel
from geometry_msgs.msg import PointStamped
import numpy as np

subscribed=False
bridge = CvBridge()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.241.8.183', 8888))



def depth_image_callback(msg):

    #将图像转换到opencv下（passthrough保留原始编码格式）
    global depth_image,subscribed
    subscribed=True
    print(subscribed)
    depth_image = bridge.imgmsg_to_cv2(msg,desired_encoding='passthrough')
    #获取相机坐标系下的坐标

    img_data = cv2.imencode('.jpg', depth_image)[1].tobytes()
    s.sendall(len(img_data).to_bytes(4, byteorder='big'))
    s.sendall(img_data)


rospy.init_node("target_site")


rospy.Subscriber("/qingzhou/camera_link/image_raw",Image,depth_image_callback)


response = s.recv(1024)
print(response.decode())


s.close()

