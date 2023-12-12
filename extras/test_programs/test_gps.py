from dataclasses import dataclass
import rospy
from sensor_msgs.msg import NavSatFix

import tests.test_drone_data as test_drone_data


def GPS_Subscriber_callback(mssg, args):

    # data = args
    test_drone_data.latitude = mssg.latitude
    test_drone_data.longitude = mssg.longitude
    test_drone_data.altitude = mssg.altitude

    # print(mssg.latitude)

if __name__ == "__main__":

    rospy.init_node('Test_gps_coordinates') 

    GPS_Subscriber=rospy.Subscriber('/mavros/global_position/global',NavSatFix, GPS_Subscriber_callback)

    while True:
        # try:
            # print("I am running")
            if test_drone_data.latitude is not None:
                print("Lat: %f, Long: %f, Alt: %.2f" %(test_drone_data.latitude, test_drone_data.longitude, test_drone_data.altitude))
        # except:
        #     pass

        # rospy.spin()