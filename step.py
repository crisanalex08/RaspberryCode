
import RPi.GPIO as GPIO
import time

ControlPin = [7, 11, 13, 15]

GPIO.setmode(GPIO.BOARD)

def actionWindows(action):
    seq = [[0]*4]*8
    if action == "open":
        print("Opening windows")
        seq = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]

    elif action == "close":
        print("Closing windows")
        seq = [ [1,0,0,1],
                [0,0,0,1],
                [0,0,1,1],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0],
                [1,1,0,0],
                [1,0,0,0] ]

    for i in range(512):
            for halfStep in range(8):
                    for pin in range(4):
                            GPIO.output(ControlPin[pin], seq[halfStep][pin])
                    time.sleep(0.001)

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

try:
        actionWindows("cloes")
except Exception as e:
        print(e)
finally:
        GPIO.cleanup()



