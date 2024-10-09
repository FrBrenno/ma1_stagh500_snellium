#include <Arduino.h>

//======== MACROS DEFINITION ========//

//=== ENUMS
#define STATUS_SUCCESS String("Success")
#define STATUS_ERROR String("Error")

//=== PINS
#define GPIO_1 3


//=== MACRO FUNCTIONS
#define GPIO_1_ON() digitalWrite(GPIO_1, HIGH)
#define GPIO_1_OFF() digitalWrite(GPIO_1, LOW)
#define GPIO_1_TOGGLE() digitalWrite(GPIO_1, !digitalRead(GPIO_1))

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;  //ms
unsigned long delayBlink = 500;   //ms

String commandStatus = STATUS_SUCCESS;
String message = "";
String errorMessage = "";

bool debugMode = false;
String debugMessage = "";

//======== CYCLE FUNCTION ========//
void setup() {
  Serial.begin(9600);
  pinMode(GPIO_1, OUTPUT);
}


void loop() {
  // Turns on LED when blinking delay is achieved.
  unsigned long currentTimeBlink = millis();
  if (currentTimeBlink - lastTimeBlink >= delayBlink) {
    GPIO_1_OFF();
  }

  // Waits for serial input
  if (Serial.available()) {
    String serialMessage = Serial.readString();
    if (serialMessage.equals("trigger")) {
      trigger();
    } else if (serialMessage.equals("ping")) {
      ping();
    } else {
      error("Invalid command");
    }

    send_response();
  }
}

//======== UTILITY FUNCTIONS ========//


void error(String errorMsg) {
  commandStatus = STATUS_ERROR;
  errorMessage += errorMsg;
}

void send_response() {
  String response = commandStatus;
  //response += ": ";
  //response += message;
  Serial.println(response);

  // Reset variables
  message = "";
  commandStatus = STATUS_SUCCESS;
  errorMessage = "";
  debugMessage = "";
}

//======== COMMANDS FUNCTIONS ========//
void ping() {
  message = "pong";
}

void trigger() {
  GPIO_1_ON();
  lastTimeBlink = millis();
  message = "All cameras were triggered";
}
