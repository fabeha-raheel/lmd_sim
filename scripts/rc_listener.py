#!/usr/bin/env python

import rospy
from mavros_msgs.msg import RCIn
from mavros_msgs.srv import StreamRate
rc_channel = 5

def set_stream_rate():
    rospy.wait_for_service('/mavros/set_stream_rate', timeout=3)
    try:
        streamService = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        streamService(0, 10, 1)
    except rospy.ServiceException as e:
        print("Setting Stream Rate failed: %s" %e)

def rc_callback(data):
    rospy.loginfo("Received RC data: %s", data)
    print(data.channels[rc_callback-1])

def listener():
    rospy.init_node('rc_in_listener', anonymous=True)
    set_stream_rate()

    rospy.Subscriber("/mavros/rc/in", RCIn, rc_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass