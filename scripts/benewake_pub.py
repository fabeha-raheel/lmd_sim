#!/usr/bin/env python3
import serial
import rospy
from std_msgs.msg import Int32

def read_data(ser, distance_pub):
    while not rospy.is_shutdown():
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3] * 256

                # Publish the distance data
                distance_pub.publish(distance)

                ser.reset_input_buffer()

if __name__ == "__main__":
    # Initialize the ROS node
    rospy.init_node('tfmini_pro_distance_node', anonymous=True)
    
    # Create a publisher for distance
    distance_pub = rospy.Publisher('tfmini_pro/distance', Int32, queue_size=10)

    ser = serial.Serial("/dev/ttyUSB0", 115200)

    try:
        if not ser.isOpen():
            ser.open()

        # Read and publish the distance data
        read_data(ser, distance_pub)
        
    except KeyboardInterrupt:
        if ser:
            ser.close()
            print("Program interrupted by the user")
