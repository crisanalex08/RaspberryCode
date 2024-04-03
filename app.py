import sys
import re
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import time
from azure.iot.device import Message
import random

SIMULATE_DATA = True
MESSAGE_TIMESPAN = 2000

EVENT_FAILED = "failed"
EVENT_SUCCESS = "success"

def is_correct_connection_string():
    m = re.search("HostName=.*;DeviceId=.*;", CONNECTION_STRING)
    if m:
        return True
    else:
        return False

CONNECTION_STRING = sys.argv[1]

if len(sys.argv) < 2:
    print ( "You need to provide the device connection string as command line arguments." )
    sys.exit(0)

if not is_correct_connection_string():
    print ( "Device connection string is not correct." )
    sys.exit(0)

print ( "Device connection string is correct." )

async def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("IoTHub Device Client Recurring Telemetry Sample")
    print("Press Ctrl+C to exit")
    loop = asyncio.get_event_loop()
    
    await send_recurring_telemetry(device_client)

async def send_recurring_telemetry(device_client):
    await device_client.connect()

    if SIMULATE_DATA:
        print("Simulating data")
        while True:
            telemetry_data = generate_mock_temp_hum_data()
            msg = Message(telemetry_data)
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"
            await device_client.send_message(msg)
            print("Sending message: {}".format(msg))
            time.sleep(MESSAGE_TIMESPAN/1000)

# Generate mock data for the data sender
def generate_mock_temp_hum_data():
    temperature = random.uniform(20, 30)  # Generate a random temperature between 20 and 30 degrees Celsius
    humidity = random.uniform(40, 60)  # Generate a random humidity between 40% and 60%
    
    # Return the generated data as a dictionary
    msg_txt_formatted = '{{"temperature": {temperature}, "humidity": {humidity}}}'
    return msg_txt_formatted.format(temperature=temperature, humidity=humidity)

def generate_mock_co2_data():
    co2 = random.uniform(400, 500)  # Generate a random CO2 level between 400 and 500 ppm
    
    # Return the generated data as a dictionary
    msg_txt_formatted = '{{"co2": {co2}}'
    return msg_txt_formatted.format(co2=co2)

asyncio.run(main())
