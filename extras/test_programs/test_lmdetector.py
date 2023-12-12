import Jetson.GPIO as GPIO
import time

# Pin Definitions
channel = 11

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)
    try:
        while True:
            # Toggle the output every second
            data = GPIO.input(channel)

            if data == True:
                print("Landmine Detected")
            else:
                print("Clear")
            # time.sleep(0.1)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()