#!/usr/bin/env python

import Jetson.GPIO as GPIO
import math
import pickle

import rospy
from sensor_msgs.msg import NavSatFix

import drone_data as data

DETECTOR_CHANNEL = 11
LOG_FILEPATH = '/home/df/lmd_ws/src/lmd_sim/logs/lmd_data.pickle'

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
                    previous_state = detected
                elif previous_state == True and detected == False:
                    # reset counter
                    counter = 0

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

if __name__ == "__main__":

    rospy.init_node('Landmine_Detection') 

    GPS_Subscriber=rospy.Subscriber('/mavros/global_position/global',NavSatFix, GPS_Subscriber_callback)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DETECTOR_CHANNEL, GPIO.IN)

    while data.latitude is None or data.longitude is None:
        pass

    find_landmines()