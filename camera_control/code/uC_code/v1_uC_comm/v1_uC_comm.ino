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
    String message = Serial.readString();
    // INFO command can be called anytime
    if (message.equals(INFO_COMMAND)){
        info();
    }
    else if (message.equals(PING_COMMAND)) {
      ping();
    }
    else if (message.equals(TRIGGER_COMMAND)){
      trigger();
    }
    else if (message.equals(HELP_COMMAND)){
      help();
    }
    else{
      error("\"" + message + "\": Unknown command.");
      help();
    }
      
  }
}

//======== UTILITY FUNCTIONS ========//
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