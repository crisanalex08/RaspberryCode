import random

#Produce mock data for the data sender
# Generate mock data for the data sender
def generate_mock_temp_hum_data():
    temperature = random.uniform(20, 40)  # Generate a random temperature between 20 and 30 degrees Celsius
    humidity = random.uniform(40, 80)  # Generate a random humidity between 40% and 60%
    air_quality = random.uniform(80, 120)  # Generate a random air quality value between 0 and 100
    
    # Return the generated data as a dictionary
    return {
        'temperature': temperature,
        'humidity': humidity,
        'air_quality': air_quality
    }

def generate_mock_co2_data():
    co2 = random.uniform(400, 500)  # Generate a random CO2 level between 400 and 500 ppm
    
    # Return the generated data as a dictionary
    return {
        'co2': co2
    }