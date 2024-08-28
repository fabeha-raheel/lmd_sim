#!/usr/bin/env python3

import rospy

from std_msgs.msg import Int16

# Configure the serial port
lmd_sense = 0

def lmd_callback(data):
    global lmd_sense
    # Callback function that gets executed when data is received on the subscribed topic
    # rospy.loginfo(f"Received Distance: {data.data}")
    lmd_sense = data.data



def find_landmines():
    global detected
    global lmd_sense
    detected = False
 
    try:
        while True:
            if lmd_sense == 1:
                detected = True
                print("#################################")
            else:
                detected = False
            
            # if detected == True:
            #     print(detected)
            # elif detected == False:
            #     print(detected)
            print(lmd_sense)
            print(detected)
    except KeyboardInterrupt:
        print("aaaaa")

if __name__ == "__main__":

    rospy.init_node('LMD_Detection') 
    rospy.Subscriber('land_mine', Int16, lmd_callback)

    find_landmines()
a