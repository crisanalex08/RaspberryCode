#include <Wire.h>
#include "DHT.h"

#define SGP30_I2C_ADDR 0x58  // Default I2C address of the SGP30 sensor
#define DHTPIN 10
#define DHTTYPE DHT11

const float RLOAD = 10.0;        // Load resistance (kΩ)
const float RZERO = 76.63;       // Sensor resistance in clean air (kΩ)
const float PARA = 116.6020682;  // Constant for the equation
const float PARB = 2.769034857;  // Constant for the equation

// Initialize DHT sensor
DHT dht_sensor(DHTPIN, DHTTYPE);

// Function to initialize the ADC
void adc_init(void) {
  // Set the reference voltage to AVcc (5V)
  ADMUX |= (1 << REFS0);

  // Set the ADC prescaler to 128 for a 125kHz ADC clock with a 16MHz system clock
  ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

  // Enable the ADC
  ADCSRA |= (1 << ADEN);
}

// Function to read from the ADC
uint16_t adc_read(uint8_t channel) {
  // Select the ADC channel (0-7)
  ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);

  // Start the conversion
  ADCSRA |= (1 << ADSC);

  // Wait for the conversion to complete
  while (ADCSRA & (1 << ADSC))
    ;

  // Read the ADC result (ADCL must be read first)
  uint16_t adc_result = ADCL;
  adc_result |= (ADCH << 8);

  return adc_result;
}

// Simple delay function
void delay_ms(uint16_t ms) {
  while (ms) {
    // This loop is roughly calibrated to take 1 ms
    // on a 16 MHz system clock
    for (uint16_t i = 0; i < 4000; i++) {
      asm volatile("nop");
    }
    ms--;
  }
}

// Function to calculate the resistance of the sensor
float getSensorResistance(int rawADC) {
  float vrl = (rawADC / 1024.0) * 5.0;   // Convert ADC value to voltage
  float rs = (5.0 - vrl) / vrl * RLOAD;  // Calculate sensor resistance
  return rs;
}

// Function to calculate the PPM of CO2 (or other gases) using the sensor resistance
float getPPM(float rs) {
  float ratio = rs / RZERO;              // Ratio of Rs/Ro
  float ppm = PARA * pow(ratio, -PARB);  // Calculate PPM using the equation
  return ppm;
}

bool initSGP30() {
  Wire.beginTransmission(SGP30_I2C_ADDR);
  Wire.write(0x20);  // Command to initialize air quality readings
  delay(10);
  Wire.write(0x03);  // Command parameters
  delay(10);
  Wire.write(0x00);  // CRC
  delay(10);
  if (Wire.endTransmission() != 0) {
    return false;  // Error initializing SGP30
  }
  delay(10);    // Wait for initialization to complete
  return true;  // SGP30 initialized successfully
}

void softResetSGP30() {
  Wire.beginTransmission(0x58); // SGP30 I2C address
  Wire.write(0x00);
  delay(10);
  Wire.write(0x06);
  Wire.endTransmission();
  delay(10); // Delay to allow the sensor to reset
}

void setup() {
  // Initialize the ADC
  adc_init();
  Wire.begin();
  dht_sensor.begin();
  // Initialize Serial communication at 9600 baud
  Serial.begin(9600);
  delay_ms(1000);
  if (!initSGP30()) {
    Serial.println("SGP_ERROR");
    while (1)
      ;  // Hang indefinitely if initialization fails
  } else {
    Serial.println("SGP_OKAY");
    softResetSGP30();
  }
}

bool measureAirQuality(uint16_t& co2, uint16_t& tvoc) {
  Wire.beginTransmission(SGP30_I2C_ADDR);
  Wire.write(0x20);  // Command to measure air quality
  delay(10);
  Wire.write(0x08);  // Command parameters
  int endTransmissionResult = Wire.endTransmission();
  
  if (endTransmissionResult != 0) {
    Serial.print("Transmission Error: ");
    Serial.println(endTransmissionResult);  // Print the error code
    return false;                           // Error sending command
  }
  delay(12);  // Wait for measurement to complete
  // Read air quality data
  Wire.requestFrom(SGP30_I2C_ADDR, 6);  // Request 6 bytes of data

  if (Wire.available() < 6) {
    return false;  // Error reading data
  }
  co2 = Wire.read() << 8 | Wire.read();   // CO2 data (MSB + LSB)
  Wire.read();                            // Discard CRC byte
  tvoc = Wire.read() << 8 | Wire.read();  // TVOC data (MSB + LSB)
  Wire.read();                            // Discard CRC byte
  return true;                            // Air quality measurement successful
}

void loop() {
  // Variable to store ADC result
  uint16_t a0_adc_value, co2 = 0, tvoc = 0;
  float temperature, humidity;
  bool airQualityMeasured = false;

  char buffer[10];
  airQualityMeasured = measureAirQuality(co2, tvoc);

  //Measure co2 and tvoc using SGP30

  // Read the ADC value from channel 0
  a0_adc_value = adc_read(0);

  // Convert the ADC value to a string
  itoa(a0_adc_value, buffer, 10);
  float rs = getSensorResistance(a0_adc_value);  // Calculate the sensor resistance
  float ppm = getPPM(rs);
  // Calculate the PPM of the gas
  humidity = dht_sensor.readHumidity();
  temperature = dht_sensor.readTemperature();

  char hum_str[20];
  char temp_str[20];
  char ppm_str[20];
  char stringResult[100];
  dtostrf(humidity, 8, 2, hum_str);
  dtostrf(temperature, 8, 2, temp_str);
  dtostrf(ppm, 8, 2, ppm_str);
  sprintf(stringResult, "%s %d %d %s %s", ppm_str, co2, tvoc, temp_str, hum_str);

  // Send the ADC value over Serial
  Serial.println(stringResult);

  // Delay for 1000 milliseconds
  delay_ms(1000);
}
