import serial

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with your serial port
    baudrate=115200,       # Set the baudrate according to your device
    timeout=1              # Set a timeout value for reading
)

# Read serial data
try:
    while True:
        if ser.in_waiting > 0:
            # Read a line from the serial device
            data = ser.readline().decode('utf-8').rstrip()
            # print(f"Received: {data}")
            if data == "1":
                print("Go to Function LMD")
            else:
                print("No LMD")
            ser.reset_input_buffer()

except KeyboardInterrupt:
    print("Serial reading stopped.")

finally:
    ser.close()
