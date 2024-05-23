import time
import serial
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.cleanup()

ControlPin = [7, 11, 13, 15]

GPIO.setmode(GPIO.BOARD)  # Use Board pin numbering
GPIO.setup(36, GPIO.OUT) # Set Output mode for pin 36 (GPIO 16)

GPIO.output(36, GPIO.LOW) # Stop the fan
global fan_running # Variable for storing the fan state
global win_open # Variable for Storing the windows state

#Assing false to both variables initially
fan_running = False 
win_open = False

#Set Output mode for pins 7, 11, 13, 15
for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0) # Set pin to low (0)

def actionWindows(action):
    seq = [[0]*4]*8 # 2D array for storing the sequence of steps for the motor
    if action == "open": 
        print("Opening windows")
        seq = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ] # 8 step sequence

    elif action == "close":
        print("Closing windows")
        seq = [ [1,0,0,1],
                [0,0,0,1],
                [0,0,1,1],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0],
                [1,1,0,0],
                [1,0,0,0] ] # 8 step sequence

    for i in range(512): #512 cycles for one full revolution
            for halfStep in range(8): #8 halfstepts 
                    for pin in range(4):#4 pins (4 coils)
                            GPIO.output(ControlPin[pin], seq[halfStep][pin]) # Set the pin to the value of the sequence
                    time.sleep(0.001) #Wait for the moovement to be done
                    
def high_temperature(payload):
    print("high_temperature method called")
    return

def high_humidity(payload):
    print("high_humidity method called")
    return

def high_air_quality(payload):
    print("high_air_quality method called")
    return

def start_fan():
    global fan_running 
    GPIO.output(36, GPIO.HIGH) # Output high on pin 36(signal for the relay that controls the fan)
    fan_running = True # Set the fan state to running

def stop_fan():
    global fan_running
    GPIO.output(36, GPIO.LOW)# Output low on pin 36(signal for the relay that controls the fan)
    fan_running = False # Set the fan state to stopped
    print("Stopping fan")


def open_window():
    global win_open 
    if not win_open:
        actionWindows("open") #Open the window
        win_open = True 

def close_window():
    global win_open
    if win_open:
        actionWindows("close") #Close the window
        win_open = False

#Method to check if the data is
# a string of 5 numbers separated by spaces
def is_num_array(data):
    try:
        data_arr = data.split()
        if len(data_arr) != 5:
            return False
        for item in data_arr:
            float(item)
        return True
    except ValueError:
        return False

#Method for formatting the data
def format_message(data):
    data = data.strip() #Remove leading and trailing whitespaces
    if is_num_array(data): #Check if the data is a string of 5 numbers separated by spaces
        data_arr = data.split() #Split the data into an array
        return {
            'gas': float(data_arr[0]),
            'co2': float(data_arr[1]),
            'tvoc': float(data_arr[2]),
            'temp': float(data_arr[3]),
            'hum': float(data_arr[4])
        }
    else:
        print("SERIAL_NOT_OKAY")
        return None


serial1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
print("Reading data from serial port")

#Weights for air quality variables
w_gas = 1
w_co2 = 1.1
w_tvoc = 1
w_hum = 2.0
w_temp = 2.0
aqi = 0
try:
    while True:
        if serial1.is_open: #Check if serial is opened
            serial_line = serial1.readline() #Read the data from the serial port
            air_data = format_message(serial_line.decode('utf-8')) #Format the data

            if air_data is not None: #Check if the data is not None
                print(air_data)
                # Compute the aqi
                aqi = (w_gas * air_data['gas']) + (w_co2 * air_data['co2']) + (w_tvoc * air_data['tvoc']) + (w_temp * air_data['temp']) + (w_hum * air_data['hum'])
                print(aqi)

                if aqi > 1600 and not fan_running: #If the aqi is greater than 1600 and the fan is not running
                    start_fan() 

                elif aqi > 1600 and not win_open: #If the aqi is greater than 1600 and the window is not open
                    open_window()

                elif aqi < 1500 and fan_running: #If the aqi is less than 1500 and the fan is running
                    stop_fan()

                elif aqi < 1500 and win_open: #If the aqi is less than 1500 and the window is open
                    close_window()
        else:
            print('Serial is not open')

        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
    serial1.close()
    close_window()
    stop_fan()
    
    