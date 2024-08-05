#include <Arduino.h>
#include <MicrocontrollerID.h>
#include "deserializer.hpp"

//======== MICROCONTROLLER INFORMATION ========//
      
#define CUSTOM_NAME F("Device A")      // User-defined
#define BOARD F("Uno Clone")
#define MCU_TYPE F("ATmega328P")    
char uCID[IDSIZE*2+1];              // uCID: uC identifier obtain from uC chips, generally a serial number

//======== MACROS DEFINITION ========//

//=== ENUMS
#define STATUS_SUCCESS String("Success")
#define STATUS_ERROR String("Error")

//=== PINS
#define LED 13
#define GPIO_1 2

//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)
#define LED_TOGGLE() digitalWrite(LED, !digitalRead(LED))

#define GPIO_1_ON() digitalWrite(GPIO_1, HIGH)
#define GPIO_1_OFF() digitalWrite(GPIO_1, LOW)
#define GPIO_1_TOGGLE() digitalWrite(GPIO_1, !digitalRead(GPIO_1))

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 2000;
String message = "";
String commandStatus = STATUS_SUCCESS;
String errorMessage = "";

bool debugMode = false;
String debugMessage = "";

//======== CYCLE FUNCTION ========//
void setup() {
  // Retrieve uC unique identify
  MicroID.getUniqueIDString(uCID, IDSIZE);

  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(GPIO_1, OUTPUT);
}


void loop() {
  // Turns on LED when blinking delay is achieved.
  unsigned long currentTimeBlink = millis();
  if (currentTimeBlink - lastTimeBlink >= delayBlink){
    if (debugMode){
      LED_ON();
    }
    else{
      LED_OFF();
    }
    GPIO_1_OFF();
  }
  
  if (Serial.available()){
    String serialMessage = Serial.readString();
    CommandArgs comArgs = Deserializer::deserialize(serialMessage);
    
    if (comArgs.status != 0){
      // Deserialization has failed.
      error(comArgs.errorMessage);
    }
    else{
      // Deserialization was successful.
      if (comArgs.command.equals(STRING_INFO)){
        info(comArgs);
      }
      else if (comArgs.command.equals(STRING_PING)) {
        ping(comArgs);
      }
      else if (comArgs.command.equals(STRING_TRIGGER)){
        trigger(comArgs);
      }
      else if (comArgs.command.equals(STRING_DEBUG)){
        debug(comArgs);
      }
      else{
        error("Command \""+ comArgs.fullString +"\"" + " unknown.");
      }
    }
    send_response();
  }
}

//======== UTILITY FUNCTIONS ========//

void blinkLED(){
  LED_TOGGLE();
  lastTimeBlink = millis();
}

void error(String errorMsg){
  commandStatus = STATUS_ERROR;
  errorMessage += errorMsg;
}

void send_response(){
  // Response construction
  // ||SUCCESS|<MESSAGE>|| or ||SUCCESS|<MESSAGE>|<DEBUG_MESSAGE>||
  // ||ERROR|<ERROR_MESSAGE>|| or ||ERROR|<ERROR_MESSAGE>|<DEBUG_MESSAGE>||
  String response = "||" + commandStatus;
  if (commandStatus.equals(STATUS_SUCCESS)){
    response += "|" + message;
  }
  else{
    response += "|" + errorMessage;
  }
  if (debugMode){
    response += "|" + debugMessage;
  }
  response += "||"; 
  // Send response
  Serial.println(response);

  // Reset variables
  message = "";
  commandStatus = STATUS_SUCCESS;
  errorMessage = "";
  debugMessage = "";

}

//======== COMMANDS FUNCTIONS ========//
void info(CommandArgs comArgs){
  // ||info|| returns all information about the device
  // ||info-<INFO_TYPE>|| returns specific information about the device
  if (comArgs.option.equals(INFO_OPTION_CUSTOM_NAME)){
    message += CUSTOM_NAME;
  }
  else if (comArgs.option.equals(INFO_OPTION_BOARD)){
    message += BOARD;
  }
  else if (comArgs.option.equals(INFO_OPTION_MCU_TYPE)){
    message += MCU_TYPE;
  }
  else if (comArgs.option.equals(INFO_OPTION_UCID)){
    message += uCID;
  }
  else{
    message += String(uCID) + "-" + CUSTOM_NAME + "-" + BOARD + "-" + MCU_TYPE;
  }
}

void ping(CommandArgs comArgs) {
  // ||ping|| returns "pong"
  message += "pong";
}

void trigger(CommandArgs comArgs){
  // ||trigger-all|| triggers all devices
  // ||trigger-selective|<ARGBLOCK>|| triggers selected devices based on ARGBLOCK
  // ||trigger-show|| shows all devices
  message += "trigger ";
  
  if (comArgs.option.equals(TRIGGER_OPTION_SELECT)){
    message += "select ";
    for (int i = 0; i < comArgs.argNumber; i++){
      message += comArgs.args[i];
    }
    GPIO_1_ON();
    blinkLED();
  }
  else if (comArgs.option.equals(TRIGGER_OPTION_SHOW)){
    message += "show";
  }
  else{
    message += "all";
    GPIO_1_ON();
    blinkLED();
  }
}

void debug(CommandArgs comArgs){
  // ||debug|| toggles debug mode
  debugMode = !debugMode;
  message += "debug mode: ";
  if (debugMode){
    message += "true";
  }
  else{
    message += "false"; 
  } 
}
