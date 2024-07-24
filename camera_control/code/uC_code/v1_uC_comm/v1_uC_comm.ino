#include <Arduino.h>
#include <MicrocontrollerID.h>
#include <avr/eeprom.h>

//======== MICROCONTROLLER INFORMATION ========//
      
#define CUSTOM_NAME "Device A"      // User-defined
#define BOARD "Uno Clone"
#define MCU_TYPE "ATmega328P"     
char uCID[IDSIZE*2+1];              // uCID: uC identifier obtain from uC chips, generally a serial number

//======== MACROS DEFINITION ========//
//=== PINS
#define LED 13

//=== COMMANDS STRINGS
#define HELLO_COMMAND String("hello")
#define PING_COMMAND String("ping")
#define TRIGGER_COMMAND String("trigger")
#define INFO_COMMAND String ("info")
#define STOP_COMMAND String("stop")

#define HELLO_RESPONSE String("hello")
#define PING_RESPONSE String("pong")
#define TRIGGER_RESPONSE String("triggered")
#define INFO_RESPONSE String(String(CUSTOM_NAME) + " (uCID:"+ uCID +") Board "+ BOARD + " " + MCU_TYPE)
#define STOP_RESPONSE String ("stopped")

//=== MACRO FUNCTIONS
#define LED_ON() digitalWrite(LED, HIGH)
#define LED_OFF() digitalWrite(LED, LOW)

//======== GLOBAL VARIABLES ========//
bool is_ready = false;
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
    if (!digitalRead(LED) && is_ready){
      LED_ON();
    }
  }
  
  
  String message = Serial.readString();
  if (message != "")
  {
    if (!is_ready){
      if (message.equals(HELLO_COMMAND)) {
        hello();
      } 
      else{
        error("\"" +message + "\": Unknown command. Available command: \"hello\".");
      }
    }
    else{
      if (message.equals(PING_COMMAND)) {
        ping();
      }
      else if (message.equals(TRIGGER_COMMAND)){
        trigger();
      }
      else if (message.equals(INFO_COMMAND)){
        info();
      }
      else if (message.equals(STOP_COMMAND)){
        stop();
      } 
      else{
        error("\"" + message + "\": Unknown command. Available command: \"ping\" \"trigger\" \"stop\".");
      }
    }    
  }
}

//======== UTILITY FUNCTIONS ========//
void blinkLED(){
  LED_OFF();
  lastTimeBlink = millis();
}
//======== COMMANDS FUNCTIONS ========//
void hello() {
  Serial.println(HELLO_RESPONSE);
  is_ready = true;
  LED_ON();
}

void error(String message){
  Serial.println(message);
}


void ping() {
  Serial.println(PING_RESPONSE);
  blinkLED();
}

void trigger(){
  Serial.println(TRIGGER_RESPONSE);
  blinkLED();
}

void info(){
  Serial.println(INFO_RESPONSE);
  blinkLED();
}

void stop(){
  Serial.println(STOP_RESPONSE);
  is_ready = false;
  LED_OFF();
}