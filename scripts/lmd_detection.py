import cv2
import numpy as np
import imutils
import math
import rospy
from sensor_msgs.msg import NavSatFix

import Lmd_Data


DETECT_THRESHOLD = 20

detections = []

def GPS_Subscriber_callback(mssg, args):

    data = args[0]
    data.latitude = mssg.latitude
    data.longitude = mssg.longitude
    data.altitude = mssg.altitude

def landmine_detection(frame, frame_center):

    distance = 0

    # lower boundary RED color range values; Hue (0 - 10)
    HSV_LOWER_1 = np.array([0, 100, 20])
    HSV_UPPER_1 = np.array([10, 255, 255])
    
    # upper boundary RED color range values; Hue (160 - 180)
    HSV_LOWER_2 = np.array([160,100,20])
    HSV_UPPER_2 = np.array([179,255,255])

    result = frame.copy()
    
    result = cv2.GaussianBlur(result, (13,13), 0)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_mask = cv2.inRange(image, HSV_LOWER_1, HSV_UPPER_1)
    upper_mask = cv2.inRange(image, HSV_LOWER_2, HSV_UPPER_2)
    
    full_mask = lower_mask + upper_mask
    full_mask = cv2.erode(full_mask, None, iterations=2)
    full_mask = cv2.dilate(full_mask, None, iterations=2)

    result = cv2.bitwise_and(result, result, mask=full_mask)

    contours = cv2.findContours(full_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(max_contour)
        bbox = cv2.boundingRect(max_contour)

        moment = cv2.moments(max_contour)
        center = (int(moment["m10"] / moment["m00"]), int(moment["m01"] / moment["m00"]))

        if radius > DETECT_THRESHOLD:

            cv2.circle(result, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv2.circle(result, center, 5, (255,0,0), -1)
            cv2.rectangle(result, (int(bbox[0]), int(bbox[1])), (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])), (0,0,255), 1)

            # Computing Distance from center
            distance = math.sqrt((frame_center[1]-center[1])**2 + (frame_center[0]-center[0])**2)

            cv2.line(result, frame_center, center, (0,255,0), 2) 
    
    return result, distance


if __name__ == "__main__":

    data = Lmd_Data()
    
    GPS_Subscriber=rospy.Subscriber('/mavros/global_position/global',NavSatFix, GPS_Subscriber_callback, (data))

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else:
        FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
        FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
        # FRAME_FPS =  cap.get(cv2.CAP_PROP_FPS)

        frame_center = (int(FRAME_WIDTH/2) , int(FRAME_HEIGHT/2))

    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Landmine Detection Codeblock
        detection, distance = landmine_detection(frame, frame_center)

        # Display the resulting frame
        cv2.imshow('frame', detection)
        if cv2.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()