#include <Arduino.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 18; // GPIO 18
const int LOADCELL_SCK_PIN = 19;  // GPIO 19

HX711 scale;
float calibration_factor = -1554; // Adjust this value to your setup

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
}

void loop() {
  scale.set_scale(calibration_factor); // Adjust to this calibration factor

  float weight = scale.get_units();
  Serial.println(weight); // Send weight over serial

  delay(1); // Send data every second
}
