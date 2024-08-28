#!/usr/bin/env python3

import math
import pickle

import rospy
from sensor_msgs.msg import NavSatFix

import drone_data as data
from std_msgs.msg import Int16

# Configure the serial port
lmd_sense = 0
LOG_FILEPATH = '/home/df/lmd_ws/src/lmd_sim/logs/lmd_data.pickle'

def GPS_Subscriber_callback(mssg):

    data.latitude = mssg.latitude
    data.longitude = mssg.longitude
    data.altitude = mssg.altitude
def lmd_callback(data):
    global lmd_sense
    # Callback function that gets executed when data is received on the subscribed topic
    # rospy.loginfo(f"Received Distance: {data.data}")
    lmd_sense = data.data



def find_landmines():
    global detected
    global lmd_sense
    detected = False
    previous_state = False
    counter = 0

    try:
        while True:
            if lmd_sense == 1:
                detected = True
            else:
                detected = False
            # If landmine is Detected
            if detected == True:

                # Save detection
                location = (data.latitude, data.longitude)
                print("Landmine Detected")

                if (previous_state == False and detected == True) or (previous_state == True and detected == True):
                    # increment counter
                    counter += 1
                elif (previous_state == True and detected == False) or (previous_state == False and detected == False):
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
    except KeyboardInterrupt:
        print("Keyboard Interrupt")

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

    rospy.init_node('LMD_Detection') 

    GPS_Subscriber=rospy.Subscriber('/mavros/global_position/global',NavSatFix, GPS_Subscriber_callback)
    rospy.Subscriber('land_mine', Int16, lmd_callback)

    while data.latitude is None or data.longitude is None:
        pass

    find_landmines()
