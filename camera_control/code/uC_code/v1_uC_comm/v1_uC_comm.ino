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
#define BLOCK_DELIMITER "|"
#define COMMAND_SEPARATOR "-"
 
#define ARGUMENT_LIST_MAXSIZE 10

#define INFO_COMMAND String ("info")
#define PING_COMMAND String("ping")
#define TRIGGER_COMMAND String("trigger")
#define DEBUG_COMMAND String ("debug")
#define HELP_COMMAND String ("help")

#define INFO_RESPONSE
#define PING_RESPONSE String("pong")
#define TRIGGER_RESPONSE String("triggered")
#define DEBUG_RESPONSE String("debug mode:")
#define HELP_RESPONSE String("Commands available: \"info\" \"ping\" \"trigger\" \"help\"")
//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)

//======== STRUCT DEFINITION ========//
struct CommandArgs{
  String fullString = "";
  String command = "";
  String option = "";
  String arguments = "";
  int argNumber = 0;
  String args[ARGUMENT_LIST_MAXSIZE];
};

//======== GLOBAL VARIABLES ========//
unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 500;
String message = "";
String errorMessage = "Error: ";
String errorOrigin = "";

String debugMessage = "Success";
bool debugMode = false;
bool debugParser = false;

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
    String command = comArgs.command;

    if (command.equals(INFO_COMMAND)){
      info(comArgs);
    }
    else if (command.equals(PING_COMMAND)) {
      ping(comArgs);
    }
    else if (command.equals(TRIGGER_COMMAND)){
      trigger(comArgs);
    }
    else if (command.equals(DEBUG_COMMAND)){
      debug(comArgs);
    }
    else if (command.equals(HELP_COMMAND)){
      help(comArgs);
    }
    else{
      message += "Command \""+ comArgs.fullString +"\"" + " unknown.";
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
void deserilizeArgumentsBlock(CommandArgs& deserialized){
  String arguments = deserialized.arguments;
  // Parse argument number
  int idxFirstSeparator = arguments.indexOf(COMMAND_SEPARATOR);

  if (idxFirstSeparator == -1){ // Empty argument block or bad-formatted.
    errorParser("Arguments block is empty or not well formatted.");
  }
  else{
    int argNumber = arguments.substring(0, idxFirstSeparator).toInt();
    arguments = arguments.substring(idxFirstSeparator + 1);
    deserialized.argNumber = argNumber;

    // See if argNumber is lower than argument list capacity
    if (argNumber > ARGUMENT_LIST_MAXSIZE){
      errorParser("There are too many arguments.");
    }

    // Parse arguments and put them in the array
    int argCount = 0;
    for (argCount = 0; argCount < argNumber; argCount++){
      int idxSeparator = arguments.indexOf(COMMAND_SEPARATOR);
      
      // grab arg and set into the array
      String arg = arguments.substring(0, idxSeparator);
      deserialized.args[argCount] = arg;
      // reduce input
      arguments = arguments.substring(idxSeparator + 1); 
    }
    if (argCount + 1 != argNumber)
      errorParser("There is not the same number of arguments as mentioned!");
  }
}

CommandArgs deserialize(){
  String input = Serial.readString();
  CommandArgs deserialized;
  deserialized.fullString = input;
  
  if (input.startsWith(COMMAND_DELIMITER) ){ 
    input = input.substring(2);

    if (input.endsWith(COMMAND_DELIMITER)){
      input = input.substring(0, input.length()-2);
      // Empty command: ||||
      if (input.equals(COMMAND_DELIMITER)){
        errorParser("Empty command block.");
        return deserialized;
      }

      //=== Separate COMMAND-OPTIONS from #ARGS-ARGUMENTS
      int idxBlockDelimiter = input.indexOf(BLOCK_DELIMITER);

      if (idxBlockDelimiter == -1){     // No block delimitation, no arguments
        deserialized.arguments = "";
      }
      else{                             // Arguments
        String arguments = input.substring(idxBlockDelimiter + 1);
        deserialized.arguments = arguments;
        // break down arguments into array
        deserilizeArgumentsBlock(deserialized);
      }

      //=== Separate COMMAND from OPTION
      input = input.substring(0, idxBlockDelimiter);
      int idxOptionSeparator = input.indexOf(COMMAND_SEPARATOR);

      if (idxOptionSeparator == -1){  // No separator on command block, single command word
        deserialized.option = "";
      }
      else{
        String option = input.substring(idxOptionSeparator + 1);
        if (option.length() == 0){ // option block is empty : command-
          errorParser("Empty option block.");
        }
        else{
          deserialized.option = option;
        } 
      }
      deserialized.command = input.substring(0, idxOptionSeparator);
    }
    else{
      errorParser("Command is not correctly delimited: Not ending with ||.");
    }
  }else{
    errorParser("Command is not correctly delimited: Not starting with ||.");
  }

  return deserialized;
}



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
  message += PING_RESPONSE;
  blinkLED();
}

void trigger(CommandArgs comArgs){
  message += TRIGGER_RESPONSE;
  blinkLED();
}

void debug(CommandArgs comArgs){
  message += DEBUG_COMMAND;
  debugMode = !debugMode;

  if (comArgs.option == "parser")
  {
    debugParser = !debugParser;
    message += " -" + comArgs.option + " " + debugParser;
    debugMessage = "Success";
  }
  
}

void help(CommandArgs comArgs){
  message += HELP_RESPONSE;
}