#include <Arduino.h>
#include <MicrocontrollerID.h>

//======== MICROCONTROLLER INFORMATION ========//
      
#define CUSTOM_NAME "Device A"      // User-defined
#define BOARD "Uno Clone"
#define MCU_TYPE "ATmega328P"     
char uCID[IDSIZE*2+1];              // uCID: uC identifier obtain from uC chips, generally a serial number

//======== MACROS DEFINITION ========//
//=== PINS
#define LED 13

//=== COMMANDS STRINGS
#define COMMAND_DELIMITER "||"
#define ARGUMENTS_DELIMITER "|"
 
#define ARGUMENT_LIST_MAXSIZE 10

#define PING_COMMAND String("ping")
#define TRIGGER_COMMAND String("trigger")
#define INFO_COMMAND String ("info")
#define HELP_COMMAND String ("help")

#define PING_RESPONSE String("pong")
#define TRIGGER_RESPONSE String("triggered")
#define INFO_RESPONSE String(String(CUSTOM_NAME) + " (uCID:"+ uCID +") Board "+ BOARD + " " + MCU_TYPE)
#define HELP_RESPONSE String("Commands available: \"info\" \"ping\" \"trigger\" \"help\"")
//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)

//======== STRUCT DEFINITION ========//
struct CommandArgs{
  String fullString = "";
  String command = "";
  String argumentsString = "";
  int argNumber = 0;
  String arguments[ARGUMENT_LIST_MAXSIZE];
};

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 500;

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
    CommandArgs comArgs = deserialize();
    Serial.println("Command: " + comArgs.command + " Arguments(" + comArgs.argNumber + "): ");
    String command = comArgs.command;

    if (command.equals(INFO_COMMAND)){
      info();
    }
    else if (command.equals(PING_COMMAND)) {
      ping();
    }
    else if (command.equals(TRIGGER_COMMAND)){
      trigger();
    }
    else if (command.equals(HELP_COMMAND)){
      help();
    }
    else{
      error("\"" + comArgs.fullString + "\": Unknown command.");
      help();
    }
      
  }
}

//======== UTILITY FUNCTIONS ========//
void deserializeArguments(CommandArgs deserialized){
  int i = 0;
  int delimiterPosition = 0;
  String input = deserialized.argumentsString;

  while (input.length() > 0){
    delimiterPosition = input.indexOf(ARGUMENTS_DELIMITER);
    String token = input.substring(0, delimiterPosition);
    if (i == 1){// Parse number of arguments
      int argNumber = token.toInt();
      deserialized.argNumber = argNumber;
      if (argNumber > ARGUMENT_LIST_MAXSIZE) // more arguments than supported
      {
        error("Too many arguments. More arguments than total capacity (10).");
        return;
      }
    }
    else{
      deserialized.arguments[i - 1] = token;
    }
    input = input.substring(delimiterPosition+1);
    i++;
  }
}

CommandArgs deserialize(){
  String input = Serial.readString();
  CommandArgs deserialized;
  deserialized.fullString = input;

  if (input.startsWith(COMMAND_DELIMITER) && input.endsWith(COMMAND_DELIMITER)){
    input = input.substring(2, input.length() - 2);

    // Parse command
    int firstDelimiterPosition = input.indexOf(ARGUMENTS_DELIMITER);
    deserialized.command = input.substring(0, firstDelimiterPosition);
    // Check if there is arguments to this command
    if (firstDelimiterPosition != -1){
      deserialized.argumentsString = input.substring(firstDelimiterPosition+1);
      deserializeArguments(deserialized);
    }
  }
  else{
    error("Incorrect command pattern.");
  }
  return deserialized;
}



void blinkLED(){
  LED_OFF();
  lastTimeBlink = millis();
}

void error(String message){
  Serial.println(message);
}

//======== COMMANDS FUNCTIONS ========//
void info(){
  Serial.println(INFO_RESPONSE);
}

void ping() {
  Serial.println(PING_RESPONSE);
  blinkLED();
}

void trigger(){
  Serial.println(TRIGGER_RESPONSE);
  blinkLED();
}

void help(){
  Serial.println(HELP_RESPONSE);
}