#include <Arduino.h>
#include "HX711.h"
#include <ArduinoBLE.h>

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 18; // GPIO 18
const int LOADCELL_SCK_PIN = 19;  // GPIO 19

HX711 scale;
float calibration_factor = -1554; // Adjust this value to your setup

BLEService weightService("4fafc201-1fb5-459e-8fcc-c5c9c331914b"); // BLE Service
BLEFloatCharacteristic weightCharacteristic("beb5483e-36e1-4688-b7f5-ea07361b26a8", BLERead | BLENotify); // BLE Characteristic

void calibrate() {
  Serial.println("Start calibration:");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");

  scale.set_scale();
  scale.tare(); // Reset the scale to 0

  long zero_factor = scale.read_average(); // Get a baseline reading
  Serial.print("Zero factor: "); // This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}

void setup() {
  Serial.begin(115200);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  calibrate();

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }
  String address = BLE.address();
  Serial.print("BLE MAC Address: ");
  Serial.println(address);  

  BLE.setLocalName("ESP32_BT_Scale");
  BLE.setAdvertisedService(weightService);
  weightService.addCharacteristic(weightCharacteristic);
  BLE.addService(weightService);
  weightCharacteristic.writeValue(0.0);

  BLE.advertise();
  Serial.println("BLE device ready to connect");
}

void loop() {
  scale.set_scale(calibration_factor); // Adjust to this calibration factor

  float weight = scale.get_units();

  BLEDevice central = BLE.central();

  if (central.connected()){
      weightCharacteristic.writeValue(weight);
      delay(100); // Send data every second
  }
  else {
    Serial.println(weight); // Send weight over serial
  }
}
