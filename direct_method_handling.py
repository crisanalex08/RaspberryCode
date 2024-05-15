import os
from azure.iot.device import IoTHubDeviceClient, MethodResponse

# The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
# The client object is used to interact with your Azure IoT hub.
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)


# connect the client.
device_client.connect()

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
    print("start_fan method called")
    return

def stop_fan():
    print("stop_fan method called")
    return

def open_window():
    print("open_window method called")
    return

def close_window():
    print("close_window method called")
    return

def update_fan_speed(payload):
    print("update_fan_speed method called")
    return

# Define behavior for handling methods
def method_request_handler(method_request):
    # Determine how to respond to the method request based on the method name
    if method_request.name == "high_temperature":
        high_temperature(method_request.payload)
        payload = {"result": True, "data": "some data"}  # set response payload
        status = 200  # set return status code
        print("executed high_temperature")

    elif method_request.name == "high_humidity":
        high_humidity(method_request.payload)
        payload = {"result": True, "data": 1234}  # set response payload
        status = 200  # set return status code
        print("executed high_humidity")

    elif method_request.name == "high_air_quality":
        high_air_quality(method_request.payload)
        payload = {"result": False, "data": "high_air_quality method"}  # set response payload
        status = 400  # set return status code
        print("executed high_air_quality method: " + method_request.name)

    elif method_request.name == "start_fan":
        start_fan()
        payload = {"result": True, "data": 1234}  # set response payload
        status = 200  # set return status code
        print("executed start_fan")

    elif method_request.name == "stop_fan":
        stop_fan()
        payload = {"result": True, "data": 1234}  # set response payload
        status = 200  # set return status code
        print("executed stop_fan")

    elif method_request.name == "update_fan_speed":
        update_fan_speed(method_request.payload)
        payload = {"result": True, "data": 1234}  # set response payload
    
    elif method_request.name == "open_window":
        open_window()
        payload = {"result": True, "data": 1234}
        status = 200
        print("executed open_window")

    elif method_request.name == "close_window":
        close_window()
        payload = {"result": True, "data": 1234}
        status = 200
        print("executed close_window")
        
    else:
        # handle other unknown method requests
        payload = {"result": False, "data": "unknown method"}
        status = 404
    # Send the response
    method_response = MethodResponse.create_from_method_request(method_request, status, payload)
    device_client.send_method_response(method_response)


# Set the method request handler on the client
device_client.on_method_request_received = method_request_handler


# Wait for user to indicate they are done listening for messages
while True:
    selection = input("Press Q to quit\n")
    if selection == "Q" or selection == "q":
        print("Quitting...")
        break


# finally, shut down the client
device_client.shutdown()