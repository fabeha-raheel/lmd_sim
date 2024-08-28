#!/usr/bin/python3

import rospy
from mavros_msgs.msg import RCIn
from mavros_msgs.srv import StreamRate
from sensor_msgs.msg import Range
from std_msgs.msg import Int32

import serial
import time
import signal
import sys


devport = '/dev/ttyUSB0'
baud = 115200
devBoard = serial.Serial(devport, baud)

rc = []  # Initialize the rc variable
up_channel = 5 #RC channel
down_channel = 6 #RC channel
lmd_sensor = 0 #LMD range sensor
drone_range_sensor = 0 #Drone Range sensor


def set_stream_rate():
    rospy.wait_for_service('/mavros/set_stream_rate', timeout=3)
    try:
        streamService = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        streamService(0, 10, 1)
    except rospy.ServiceException as e:
        print("Setting Stream Rate failed: %s" % e)

def distance_callback(data):
    # Callback function that gets executed when data is received on the subscribed topic
    # rospy.loginfo(f"Received Distance: {data.data}")
    global lmd_sensor
    lmd_sensor = data.data
def rangefinder_callback(data):
    global drone_range_sensor
    # rospy.loginfo("Received rangefinder data: %s", data.range)
    drone_range_sensor = int((data.range)*100) # to convert into cm
    # print(drone_range_sensor)

def rc_callback(data):
    global rc
    rc = data.channels

def listener():
    rospy.init_node('lmd_auto', anonymous=True)
    set_stream_rate()

    rospy.Subscriber("/mavros/rc/in", RCIn, rc_callback)
    rospy.Subscriber('tfmini_pro/distance', Int32, distance_callback)
    rospy.Subscriber("/mavros/distance_sensor/rangefinder_pub", Range, rangefinder_callback)
def signal_handler(sig, frame):
    print("Exiting due to keyboard interrupt")
    devBoard.write("STOP\n".encode())
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    try:
        if not devBoard.isOpen():
            devBoard.open()

        listener()
    except rospy.ROSInterruptException:
        pass

    while not rospy.is_shutdown():
        try:
            if rc:
                if len(rc) > 0:
                    # read_lmd_range()
                    # print(lmd_sensor)
                    # print(drone_range_sensor)
                    if rc[up_channel-1] > 1200:
                        if lmd_sensor>15:
                            print("Up command Dev Board")
                            devBoard.write("UP\n".encode())
                            while lmd_sensor >15 and rc[up_channel-1] > 1200 and not rospy.is_shutdown():
                                print(lmd_sensor)
                                print(drone_range_sensor)
                                print("go down")
                                # pass
                        elif lmd_sensor < 15:
                            print("Down command Dev Board")
                            devBoard.write("DOWN\n".encode())
                            while lmd_sensor < 15 and rc[up_channel-1] > 1200 and not rospy.is_shutdown():
                                print(lmd_sensor)
                                print(drone_range_sensor)
                                print("go up")
                                # pass

                    elif rc[down_channel-1] > 1200 and (drone_range_sensor-lmd_sensor)>45:
                        print("Down command Dev Board")
                        devBoard.write("DOWN\n".encode())
                        while rc[down_channel-1] > 1200 and not rospy.is_shutdown():
                            print(lmd_sensor)
                            print("go up")
                            # pass
                    else:
                        print("Stopping Dev Board")
                        devBoard.write("STOP\n".encode())
                        while rc[up_channel-1] < 1200 and rc[down_channel-1] < 1200 and not rospy.is_shutdown():
                            print(lmd_sensor)
                            print("stop")
                            # pass
                else:
                    print("RC data does not have the expected elements")
            else:
                print("No RC data received yet")

            # rospy.sleep(0.5)  # Sleep for a while to avoid busy-waiting
        except KeyboardInterrupt:
            if devBoard:
                devBoard.close()

            print("Exiting due to keyboard interrupt")
            print("Stopping Dev Board")
            # devBoard.write("STOP\n".encode())
            signal_handler(None, None)

