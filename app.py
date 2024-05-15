import sys
import re
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import time
from azure.iot.device import Message
import random
from mock_data_sender import generate_mock_temp_hum_data
from mock_data_sender import generate_mock_co2_data
import serial
import os

SIMULATE_DATA = sys.argv[1] if len(sys.argv) > 1 else False
MESSAGE_TIMESPAN = 2000

EVENT_FAILED = "failed"
EVENT_SUCCESS = "success"

def is_correct_connection_string():
    m = re.search("HostName=.*;DeviceId=.*;", CONNECTION_STRING)
    if m:
        return True
    else:
        return False


CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

if not is_correct_connection_string():
    print("Device connection string is not correct.")
    sys.exit(0)

print("Device connection string is correct.")


async def main():
    try:
        device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        
        print("IoTHub Device Client Recurring Telemetry Sample")
        print("Press Ctrl+C to exit")
        loop = asyncio.get_event_loop()

        await send_recurring_telemetry(device_client)
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            device_client.shutdown()
            print("Quitting...")
            return
    except Exception as e:
        print("Unexpected error %s " % e)
        device_client.shutdown()
        print("Shutting down device client")


async def send_recurring_telemetry(device_client):
    await device_client.connect()
    while True:
        if SIMULATE_DATA:
            print("Simulating data")
            await send_data(generate_mock_temp_hum_data(), device_client)
        else:
            print("Reading data from serial port")
            serial1 = serial.Serial('/dev/ttyACM0', 9600)
            
            await send_data(serial1.readline(), device_client) 
        time.sleep(MESSAGE_TIMESPAN/1000)


async def send_data(telemetry_data, device_client):
        print(telemetry_data)
        msg = Message(telemetry_data)
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        print("Sending message: {}".format(msg))

asyncio.run(main())


