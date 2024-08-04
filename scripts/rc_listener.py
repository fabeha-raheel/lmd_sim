#!/usr/bin/env python

import rospy
from mavros_msgs.srv import StreamRate, StreamRateRequest, StreamRateResponse
from mavros_msgs.msg import RCIn

def set_stream_rate():
    rospy.wait_for_service('/mavros/set_stream_rate')
    try:
        stream_rate_srv = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        req = StreamRateRequest()
        req.stream_id = 0  # all streams
        req.message_rate = 10  # 10 Hz
        req.on_off = 1  # start stream
        resp = stream_rate_srv(req)
        return resp.success
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)
        return False

def rc_callback(data):
    rospy.loginfo("Received RC data: %s", data)

def listener():
    rospy.init_node('rc_listener', anonymous=True)
    
    # Set stream rate
    if set_stream_rate():
        rospy.loginfo("Stream rate set successfully")
    else:
        rospy.logwarn("Failed to set stream rate")
    
    rospy.Subscriber("/mavros/rc/in", RCIn, rc_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
