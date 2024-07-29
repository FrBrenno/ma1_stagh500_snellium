#include <Arduino.h>
#include <MicrocontrollerID.h>
#include "deserializer.hpp"

//======== MICROCONTROLLER INFORMATION ========//
      
#define CUSTOM_NAME "Device A"      // User-defined
#define BOARD "Uno Clone"
#define MCU_TYPE "ATmega328P"     
char uCID[IDSIZE*2+1];              // uCID: uC identifier obtain from uC chips, generally a serial number

//======== MACROS DEFINITION ========//
//=== PINS
#define LED 13

//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 500;
String message = "";
String errorMessage = "";

String debugMessage = "Success";
bool debugMode = false;

//======== CYCLE FUNCTION ========//
void setup() {
  // Retrieve uC unique identify
  MicroID.getUniqueIDString(uCID, IDSIZE);

  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}


void loop() {
  // Turns on LED when blinking delay is achieved.
  unsigned long currentTimeBlink = millis();
  if (currentTimeBlink - lastTimeBlink >= delayBlink){
    if (!digitalRead(LED)){
      LED_ON();
    }
  }
  
  if (Serial.available()){
    String commandString = Serial.readString();
    CommandArgs comArgs = Deserializer::deserialize(commandString);

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
      else if (comArgs.command.equals(STRING_HELP)){
        help(comArgs);
      }
      else{
        message += "Command \""+ comArgs.fullString +"\"" + " unknown.";
      }
    }
   

    if (message.length() > 0){
      Serial.println(message);
      message = "";
    }
    if (debugMode){
      Serial.println(debugMessage);
      debugMessage = "Success";
    }
    if (errorMessage.length() > 0){
      Serial.println(errorMessage);
      errorMessage = "";
    }
  }
   
}

//======== UTILITY FUNCTIONS ========//

void blinkLED(){
  LED_OFF();
  lastTimeBlink = millis();
}

void error(String errorMsg){
  debugMessage = "Fail";
  errorMessage += errorMsg;
}


//======== COMMANDS FUNCTIONS ========//
void info(CommandArgs comArgs){
  // ||info|| returns all information about the device
  // ||info-<INFO_TYPE>|| returns specific information about the device
  message += "INFO: ";
  
  if (comArgs.option.equals(INFO_ARG_CUSTOM_NAME)){
    message += CUSTOM_NAME;
  }
  else if (comArgs.option.equals(INFO_ARG_BOARD)){
    message += BOARD;
  }
  else if (comArgs.option.equals(INFO_ARG_MCU_TYPE)){
    message += MCU_TYPE;
  }
  else if (comArgs.option.equals(INFO_ARG_UCID)){
    message += uCID;
  }
  else{
    message += "Custom Name: " + String(CUSTOM_NAME) + " | Board: " + BOARD + " | MCU Type: " + MCU_TYPE + " | uCID: " + uCID;
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
  message += "trigger";
  
  if (comArgs.option.equals(TRIGGER_OPTION_ALL)){
    message += " all";
    blinkLED();
  }
  else if (comArgs.option.equals(TRIGGER_OPTION_SELECTIVE)){
    message += " selective";
    for (int i = 0; i < comArgs.argNumber; i++){
      message += " " + comArgs.args[i];
    }
    blinkLED();
  }
  else if (comArgs.option.equals(TRIGGER_OPTION_SHOW)){
    message += " show";
  }
  else{
    message += " all";
    blinkLED();
  }
}

void debug(CommandArgs comArgs){
  // ||debug|| toggles debug mode
  debugMode = !debugMode;
  message += "debug mode: ";
  if (debugMode)
    message += "true";
  else
    message += "false";  
}

void help(CommandArgs comArgs){
  // ||help|| returns all available commands and short description
  // ||help-<COMMAND>|| returns detailed information about the command
  message += "HELP: ";

  if (comArgs.option.equals(""))
  {
    message += "Available commands: ";
    message += "ping, info, trigger, debug, help\n";
  }
  else if (comArgs.option.equals(STRING_PING)){
    message += "ping: returns 'pong' \n";
    message += "It is used to check if the communication with the device still active.\n";
  }
  else if (comArgs.option.equals(STRING_INFO)){
    message += "info: returns all device information\n";
    message += "It is used to retrieve information about the device.\n";
    message += "Options: custom_name, board, mcu_type, ucid\n";
  }
  else if (comArgs.option.equals(STRING_TRIGGER)){
    message += "trigger: sends a trigger to the device\n";
    message += "It is used to trigger the device to perform image acquisition.\n";
    message += "Options: all, selective, show\n";
  }
  else if (comArgs.option.equals(STRING_DEBUG)){
    message += "debug: toggles debug mode\n";
    message += "Debug mode is used to check the device's internal state.\n";
  }
  else if (comArgs.option.equals(STRING_HELP)){
    message += "help: returns available commands\n";
    message += "It is used to retrieve information about the available commands.\n";
    message += "Options: ping, info, trigger, debug, help\n";
  }
  else{
    message += "Command \"" + comArgs.option + "\" not found.";
  }
}