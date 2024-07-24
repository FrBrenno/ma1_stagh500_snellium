#include <Arduino.h>
#include <EEPROM.h>

#if defined(ARDUINO_AVR_UNO)       
  #define BOARD "Uno"

//======== MICROCONTROLLER INFORMATION ========//
const String customName = "Device A";       # User-defined
const String board = "Board " + BOARD;      # Hardware defined, defined on IDE
const String mcuType = "ATmega328P-AU";     # Hardware defined
const String serialNumber = "123456789";    # Hardware defined, some MCU types has built-in SID

//======== MACROS DEFINITION ========//
//=== PINS
#define LED 13

//=== COMMANDS STRINGS
#define HELLO_COMMAND String("hello")
#define PING_COMMAND String("ping")
#define TRIGGER_COMMAND String("trigger")
#define STOP_COMMAND String("stop")

#define HELLO_RESPONSE String("hello")
#define PING_RESPONSE String("pong")
#define TRIGGER_RESPONSE String("triggered")
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
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}


void loop() {
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

void stop(){
  Serial.println(STOP_RESPONSE);
  is_ready = false;
  LED_OFF();
}