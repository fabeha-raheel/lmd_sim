#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import math
import pickle

import rospy
from sensor_msgs.msg import NavSatFix

import drone_data as data

DETECTOR_CHANNEL = 11
LOG_FILEPATH = '/home/df/lmd_ws/src/lmd_sim/logs/lmd_data.pickle'
MAPPING_LOG = '/home/df/lmd_ws/src/lmd_sim/logs/lmd_data.txt'

def GPS_Subscriber_callback(mssg):

    data.latitude = mssg.latitude
    data.longitude = mssg.longitude
    data.altitude = mssg.altitude


def find_landmines():
    detected = False
    previous_state = False
    counter = 0

    try:
        while True:
            detected = GPIO.input(DETECTOR_CHANNEL)

            # If landmine is Detected
            if detected == True:

                # Save detection
                location = (data.latitude, data.longitude)
                print("Landmine Detected")

                if (previous_state == False and detected == True) or (previous_state == True and detected == True):
                    # increment counter
                    counter += 1
                elif previous_state == True and detected == False:
                    # reset counter
                    counter = 0
                previous_state = detected

                # Check if landmines is already saved
                landmine_present = False

                for landmine in data.landmines:
                    gps_distance = get_distance_metres(location, landmine[1])
                    
                    if gps_distance < 2:
                        landmine_present = True

                        if counter > landmine[0]:
                            index = data.landmines.index(landmine)
                            data.landmines[index] = (counter, location)
                            print("Updated landmine")
                            print(data.landmines)
                            write_to_log(data.landmines)
                            # save_log(data.landmines)
                            break
                        else:
                            #no need to update and check with other landmine
                            break

                # if no landmine is present in the list, then append it to the list                
                if landmine_present == False:
                    detection = (counter, location)
                    data.landmines.append(detection)
                    print("Adding new Landmine")
                    print(data.landmines)
                    write_to_log(data.landmines)
                    # save_log(data.landmines)

    finally:
        GPIO.cleanup()

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two GPS locations.
    
    Locations should be passed as a tuple in the form (lat, long).

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2[0] - aLocation1[0]
    dlong = aLocation2[1] - aLocation1[1]
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def write_to_log(data):

    f = open(LOG_FILEPATH, 'wb')
    pickle.dump(data, f)
    f.close()

def save_log(data):

    with open(MAPPING_LOG, 'w') as f:
        f.write(str(data))

if __name__ == "__main__":

    rospy.init_node('Landmine_Detection') 

    GPS_Subscriber=rospy.Subscriber('/mavros/global_position/global',NavSatFix, GPS_Subscriber_callback)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DETECTOR_CHANNEL, GPIO.IN)

    while data.latitude is None or data.longitude is None:
        pass

    find_landmines()


'''
How to run this code:

Connect the signal from the landmine detector to the Jetson Nano GPIO Pins. Specify the pin number in the DETECTOR_CHANNEL variable.

In order to run the Drone simulation on a separate computer, we need to configure the master slave communication.
Get the IP of the Jetson Nano using the ifconfig command. Save it.
Modify the .bashrc file in the Jetson Nano with the following lines:
export ROS_MASTER_URI=http://localhost:11311/
export ROS_HOSTNAME=<IP_address_of_Jetson>
export ROS_IP=<IP_address_of_Jetson>

Then get the IP address of your PC using ifconfig and modify its .bashrc file as follows:
export ROS_MASTER_URI=http://<IP_address_of_Jetson>:11311/
export ROS_HOSTNAME=<IP_address_of_PC>
export ROS_IP=<IP_address_of_PC>

Now run the lmd_detector simulation in your PC using "roslaunch lmd_sim lmd_detector_simulation.launch" command.

You should be able to access the mavros topics on the Jetson Nano when you run rostopic list.

Run the following file in the Jetson Nano to detect the landmines and save their GPS coordinates:
roscd lmd_sim/scripts && ./lmd_detector.py
Make sure that the file has executable permissions using sudo chmod +x *.*

After all the landmine locations are saved to the log file, you can visualize the locations on a Map:
roscd lmd_sim/scripts && ./offline-mapping.py
Make sure that the file has executable permissions using sudo chmod +x *.*
'''