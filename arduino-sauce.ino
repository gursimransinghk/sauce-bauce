#include <Wire.h>
#include <Adafruit_Trellis.h>
#include <LiquidCrystal_I2C.h>

#define MOMENTARY 0
#define LATCHING 1

#define MODE MOMENTARY

LiquidCrystal_I2C lcd(0x3F, 20, 4);

Adafruit_Trellis matrix0 = Adafruit_Trellis();
Adafruit_TrellisSet trellis = Adafruit_TrellisSet(&matrix0);

#define NUMTRELLIS 1
#define numKeys (NUMTRELLIS * 16)

void setup() {
  Serial.begin(9600);
  Serial.println("Trellis Keypad Test:");

  Wire.begin();
  trellis.begin(0x70);
  lcd.begin(20, 4);
  lcd.print("Keypad test:");

  for (uint8_t i = 0; i < numKeys; i++) {
    trellis.setLED(i);
    trellis.writeDisplay();
    delay(50);
  }
  
  for (uint8_t i = 0; i < numKeys; i++) {
    trellis.clrLED(i);
    trellis.writeDisplay();
    delay(50);
  }

  Serial1.begin(9600);
}

void loop() {
  delay(30);

  if (MODE == MOMENTARY) {
    if (trellis.readSwitches()) {
      for (uint8_t i = 0; i < 16; i++) {
        if (trellis.justPressed(i)) {
          Serial.print("Key Pressed: ");
          Serial.println(i);
          lcd.setCursor(0, 1);
          lcd.print("Key Pressed: ");
          lcd.print(i);
          trellis.setLED(i);

          char letter = 'A' + i;
          Serial1.print(letter);
        }
        
        if (trellis.justReleased(i)) {
          Serial.print("Key Released: ");
          Serial.println(i);
          trellis.clrLED(i);
          
          if(i == 3) {  // Assuming the key that represents 'D' is at index 3 (D = 'A' + 3)
            Serial1.print('E');  // Send 'E' when 'D' is released
          }
        }
      }
      trellis.writeDisplay();
    }
  }

  while (Serial1.available()) {
    char receivedChar = Serial1.read();
  }
}
