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

#define INFO_COMMAND String ("info")
#define PING_COMMAND String("ping")
#define TRIGGER_COMMAND String("trigger")
#define DEBUG_COMMAND String ("debug")
#define HELP_COMMAND String ("help")

//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 500;
String message = "";
String errorMessage = "Error: ";
String errorOrigin = "";

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

    if (!comArgs.status){
      // Deserialization has failed.
      errorMessage +=  comArgs.errorMessage;
    }
    else{
      // Deserialization was successful.
      if (comArgs.command.equals(INFO_COMMAND)){
        info(comArgs);
      }
      else if (comArgs.command.equals(PING_COMMAND)) {
        ping(comArgs);
      }
      else if (comArgs.command.equals(TRIGGER_COMMAND)){
        trigger(comArgs);
      }
      else if (comArgs.command.equals(DEBUG_COMMAND)){
        debug(comArgs);
      }
      else if (comArgs.command.equals(HELP_COMMAND)){
        help(comArgs);
      }
      else{
        message += "Command \""+ comArgs.fullString +"\"" + " unknown.";
      }
    }
   

    if (message != ""){
      Serial.println(message);
      message = "";
    }
    if (debugMode){
      Serial.println(debugMessage);
      debugMessage = "Success";
    }
    if (errorMessage != "Error: "){
      Serial.println(errorMessage);
      errorMessage = "Error: ";
      errorOrigin = "";
    }
  }
   
}

//======== UTILITY FUNCTIONS ========//

void blinkLED(){
  LED_OFF();
  lastTimeBlink = millis();
}

void errorParser(String errorMsg){
  error("Parser: "+ errorMsg);
}

void error(String errorMsg){
  debugMessage = "Fail";
  errorMessage += errorMsg;
}


//======== COMMANDS FUNCTIONS ========//
void info(CommandArgs comArgs){
  // It is possible to get every individual info of uC
  // by passing the derised info name as arguments
  message += "INFO: ";
  if (comArgs.argNumber == 0){
    message += String(CUSTOM_NAME) + " (uCID:"+ uCID +") Board "+ BOARD + " " + MCU_TYPE;
  }
  else{
    for (int i = 0; i < comArgs.argNumber; i++){
      String arg = comArgs.args[i];
      debugMessage += "###" + String(i) + ": " + arg + "\n";
      if (arg.equals("custom_name")) {
        message += CUSTOM_NAME;
      } else if (arg.equals("ucid")) {
          message += uCID;
      } else if (arg.equals("board")) {
          message += BOARD;
      } else if (arg.equals("mcu_type")) {
          message += MCU_TYPE;
      } else {}
    }
  }
}

void ping(CommandArgs comArgs) {
  message += "pong";
  blinkLED();
}

void trigger(CommandArgs comArgs){
  message += "triggered";
  blinkLED();
}

void debug(CommandArgs comArgs){
  debugMode = !debugMode;
  message += "debug mode: ";
  if (debugMode)
    message += "true";
  else
    message += "false";  
}

void help(CommandArgs comArgs){
  message += "Commands available: \"info\" \"ping\" \"trigger\" \"help\"";
}