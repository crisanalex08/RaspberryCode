import random

#Produce mock data for the data sender
# Generate mock data for the data sender
def generate_mock_temp_hum_data():
    temperature = random.uniform(20, 30)  # Generate a random temperature between 20 and 30 degrees Celsius
    humidity = random.uniform(40, 60)  # Generate a random humidity between 40% and 60%
    
    # Return the generated data as a dictionary
    return {
        'temperature': temperature,
        'humidity': humidity
    }

def generate_mock_co2_data():
    co2 = random.uniform(400, 500)  # Generate a random CO2 level between 400 and 500 ppm
    
    # Return the generated data as a dictionary
    return {
        'co2': co2
    }