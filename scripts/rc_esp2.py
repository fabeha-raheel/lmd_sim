#!/usr/bin/python3

import rospy
from mavros_msgs.msg import RCIn
from mavros_msgs.srv import StreamRate

import serial
import time
import signal
import sys

# devport = 'COM4'
devport = '/dev/ttyUSB0'
baud = 115200

devBoard = serial.Serial(devport, baud)

rc = []  # Initialize the rc variable
up_channel = 5
down_channel = 6

def set_stream_rate():
    rospy.wait_for_service('/mavros/set_stream_rate', timeout=3)
    try:
        streamService = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        streamService(0, 10, 1)
    except rospy.ServiceException as e:
        print("Setting Stream Rate failed: %s" % e)

def rc_callback(data):
    global rc
    rc = data.channels

def listener():
    rospy.init_node('rc_in_listener', anonymous=True)
    set_stream_rate()

    rospy.Subscriber("/mavros/rc/in", RCIn, rc_callback)

def signal_handler(sig, frame):
    print("Exiting due to keyboard interrupt")
    devBoard.write("STOP\n".encode())
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    try:
        listener()
    except rospy.ROSInterruptException:
        pass

    while not rospy.is_shutdown():
        try:
            if rc:
                if len(rc) > 0:
                    if rc[up_channel-1] > 1200:
                        print("Up command Dev Board")
                        devBoard.write("UP\n".encode())
                        time.sleep(2)
                        print("Stopping Dev Board")
                        devBoard.write("STOP\n".encode())
                        time.sleep(1)
                        print("Down command Dev Board")
                        devBoard.write("DOWN\n".encode())
                        time.sleep(2)
                        print("Stopping Dev Board")
                        devBoard.write("STOP\n".encode())
                        time.sleep(1)
                    else:
                        print("Stopping Dev Board")
                        devBoard.write("STOP\n".encode())
                        while rc[up_channel-1] < 1200 and not rospy.is_shutdown():
                            pass
                else:
                    print("RC data does not have the expected elements")
            else:
                print("No RC data received yet")

            rospy.sleep(0.5)  # Sleep for a while to avoid busy-waiting
        except KeyboardInterrupt:
            print("Exiting due to keyboard interrupt")
            print("Stopping Dev Board")
            # devBoard.write("STOP\n".encode())
            signal_handler(None, None)

