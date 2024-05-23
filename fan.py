import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(16, GPIO.OUT)

try:
    while True:
        print("GPIO 16 ON")
        GPIO.output(16, GPIO.HIGH)  # Turn on GPIO 16 (LED on)
        time.sleep(1)  # Wait for 1 second
        
        print("GPIO 16 OFF")
        GPIO.output(16, GPIO.LOW)  # Turn off GPIO 16 (LED off)
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    pass  # Exit the loop when Ctrl+C is pressed

# Clean up GPIO
GPIO.cleanup()
