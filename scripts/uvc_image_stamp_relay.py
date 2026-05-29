#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image

class ImageStampRelay:
    def __init__(self):
        self.frame_id = rospy.get_param('~frame_id', 'uvc_camera')
        self.pub = rospy.Publisher('/uvc_camera/image_sync', Image, queue_size=5)
        self.sub = rospy.Subscriber('/uvc_camera/image', Image, self.cb, queue_size=5)

    def cb(self, msg):
        out = Image()
        out.header = msg.header
        out.header.stamp = rospy.Time.now()
        if not out.header.frame_id:
            out.header.frame_id = self.frame_id
        out.height = msg.height
        out.width = msg.width
        out.encoding = msg.encoding
        out.is_bigendian = msg.is_bigendian
        out.step = msg.step
        out.data = msg.data
        self.pub.publish(out)

if __name__ == '__main__':
    rospy.init_node('uvc_image_stamp_relay')
    ImageStampRelay()
    rospy.spin()
