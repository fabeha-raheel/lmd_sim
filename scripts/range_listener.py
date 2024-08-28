#!/usr/bin/env python

import rospy
from mavros_msgs.srv import StreamRate
from sensor_msgs.msg import Range  # Import the Range message type for distance sensor


def set_stream_rate():
    rospy.wait_for_service('/mavros/set_stream_rate', timeout=3)
    try:
        streamService = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        streamService(0, 10, 1)
    except rospy.ServiceException as e:
        print("Setting Stream Rate failed: %s" % e)

def rangefinder_callback(data):
    rospy.loginfo("Received rangefinder data: %s", data.range)

def listener():
    rospy.init_node('range_listener', anonymous=True)
    set_stream_rate()
    
    # Subscriber for distance sensor (rangefinder)
    rospy.Subscriber("/mavros/distance_sensor/rangefinder_pub", Range, rangefinder_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
