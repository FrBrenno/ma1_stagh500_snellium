#include <Arduino.h>
#include <MicrocontrollerID.h>

#include "protocol_symbols.hpp"

//======== MICROCONTROLLER INFORMATION ========//

#define DEVICE_NAME F("Device A")  // User-defined
#define BOARD_NAME F("Uno Clone")
#define UNIT_TYPE F("ATmega328P")
char SERIAL_NUMBER[IDSIZE * 2 + 1];  // uCID: uC identifier obtain from uC chips,
                                     // generally a serial number

//======== MACROS DEFINITION ========//

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

//=== PARSER
#define ARGUMENT_LIST_MAXSIZE 10

enum CommandStatus {
  COMMAND_SUCCESS,
  COMMAND_ERROR_ARG_LIST_FULL,
  COMMAND_ERROR_ARG_NUMBER
};

struct Command {
  String command = "";
  String arguments[ARGUMENT_LIST_MAXSIZE];
  String errorMessage = "";

  int arg_number = 0;
  CommandStatus status = COMMAND_SUCCESS;
};

enum ParserState { COMMAND,
                   ARGUMENTS,
                   ERROR };

//======== GLOBAL VARIABLES ========//

unsigned long lastTimeBlink = 0;
unsigned long delayBlink = 3000;  // ms

bool debug_mode = false;
Command cmd;

//========= UTILS FUNCTIONS ========//

void blink_LED() {
  LED_ON();
  lastTimeBlink = millis();
}

//======== SERIAL COMMUNICATION ========//
bool serial_has_data() {
  return Serial.available() > 0;
}

String serial_read() {
  String received = "";
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == START_COMMAND_CHAR) {
      received = "";
    } else if (c == END_COMMAND_CHAR) {
      break;
    } else {
      received += c;
    }
  }
  return received;
}

void serial_write_data(String data) {
  Serial.print(START_COMMAND_CHAR);
  Serial.print(data);
  Serial.print(END_COMMAND_CHAR);
}

//======== CYCLE FUNCTION ========//

void setup() {
  // Retrieve uC unique identify
  MicroID.getUniqueIDString(SERIAL_NUMBER, IDSIZE);
  Serial.begin(9600);

  pinMode(LED, OUTPUT);
  pinMode(GPIO_1, OUTPUT);
  LED_OFF();
}

void loop() {
  // Turns on LED when blinking delay is achieved.
  unsigned long currentTimeBlink = millis();
  if (currentTimeBlink - lastTimeBlink >= delayBlink) {
    LED_OFF();
  }

  if (serial_has_data()) {
    String received = serial_read();
    cmd = parse_command(received);

    if (cmd.status == 0) {
      if (cmd.command == CMD_PING) {
        serial_write_data(CMD_PING);
      } else if (cmd.command == CMD_INFO) {
        serial_write_data(CMD_INFO);
      } else {
        serial_write_data("Command not found");
      }
    } else {
      serial_write_data(cmd.errorMessage);
    }
  }
}

//======== PARSER FUNCTIONS ========//
Command parse_command(String received) {
  Command cmd;
  ParserState state = COMMAND;

  for (size_t i = 0; i < received.length(); i++) {
    char c = received[i];
    if (state == COMMAND) {
      if (c == ELEMENT_SEPARATOR_CHAR) {
        state = ARGUMENTS;
      } else {
        cmd.command += c;
      }
    } else if (state == ARGUMENTS) {
      if (c == ELEMENT_SEPARATOR_CHAR) {
        cmd.arg_number++;
        if (cmd.arg_number >= ARGUMENT_LIST_MAXSIZE) {
          cmd.status = COMMAND_ERROR_ARG_LIST_FULL;
          cmd.errorMessage = "Argument list is full";
          break;
        }
      } else {
        cmd.arguments[cmd.arg_number] += c;
      }
    }

    if (cmd.arguments[0].toInt() != cmd.arg_number) {
      cmd.status = COMMAND_ERROR_ARG_NUMBER;
      cmd.errorMessage = "Argument number is invalid";
      break;
    }
  }

  return cmd;
}

//======== COMMAND TASK FUNCTIONS ========//

String ping() {
  String message = "";
  message += CMD_PING;
  message += ELEMENT_SEPARATOR_CHAR;
  message += "PONG";
  return message;
}

String info() {
  String message = "";
  message += CMD_INFO;
  message += ELEMENT_SEPARATOR_CHAR;
  message += "INFO";
  return message;
}
