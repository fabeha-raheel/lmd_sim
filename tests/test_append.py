import cv2
import numpy as np
import imutils
import math
import rospy
from sensor_msgs.msg import NavSatFix

dist_threshold = 1

my_list= [(6,(1,1)),(7,(1,2)),(8,(1,3)),(9,(1,4)),(10,(1,5))]
print((my_list[0]))

def calc_dist(x,y):
    return math.dist(x,y)


d = int(input("Enter d : "))
lat = int(input("Enter lat : "))
lon = int(input("Enter lon : "))
input_data = [(d,(lat,lon))]
print("you entered : ", input_data)
update = True
d_update =  False
for n in range(len(my_list)):
    distance = calc_dist((input_data[0][1]),((my_list[n])[1]))
    print("distance = ", distance)
    if distance < dist_threshold:
        if input_data[0][0] < my_list[n][0]:
            my_list[n] = input_data[0]
            print("distance updated : ", my_list[n])
            print("New list : ", my_list)
            d_update = True
        update = False
        break
    else:
        pass
if update:
    my_list.append(input_data[0])
    print(my_list)
else:
    if not d_update:
        print("Nothing to update")