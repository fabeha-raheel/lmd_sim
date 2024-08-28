#!/usr/bin/python3

import serial
import time

devport = 'COM4'
# devport = '/dev/ttyUSB-DEV'
baud = 115200
# mcport = '/dev/ttyUSB-MC'

devBoard = serial.Serial(devport, baud)
# mcBoard = serial.Serial(mcport, baud)

while True:
    try:
        print("Up command Dev Board")
        devBoard.write("UP\n".encode())
        time.sleep(5)
        print("Stoping Dev Board")
        devBoard.write("STOP\n".encode())
        time.sleep(2)
        print("Down command Dev Board")
        devBoard.write("DOWN\n".encode())
        time.sleep(5)
        print("Stoping Dev Board")
        devBoard.write("STOP\n".encode())
        time.sleep(2)
    except KeyboardInterrupt:
        print("Stoping Dev Board")
        devBoard.write("STOP\n".encode())
        break
        
        
        
# while True:
# 	try:
# 		signal = mcBoard.readline().decode().strip()
        
# 		if int(signal) > 1500:
# 			print("Enabling Dev Board")
# 			devBoard.write("ENABLE\n".encode())
# 			while True:
# 				signal = mcBoard.readline().decode().strip()
# 				if int(signal) < 1500:
# 					print("Disabling Dev Board")
# 					devBoard.write("DISABLE\n".encode())
# 					break
# 	except KeyboardInterrupt:
#             print("Disabling Dev Board")
#             devBoard.write("DISABLE\n".encode())
#             break
