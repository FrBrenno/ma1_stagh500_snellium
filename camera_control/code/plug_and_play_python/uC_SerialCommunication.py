import serial
import time
import random

from uC_Commands import *

### Sleep time between port opening and command execution.
### This is necessary because of Arduino auto-reset feature.
### Whenever a serial communication is established, the Arduino resets and
### the bootloader needs some time to run before accepting commands.
SLEEP_TIME = 1.62 
### Timeout for serial communication.
### This is the time the program waits for a response from the Arduino.
### Needed because of readline() function.
TIMEOUT_RX = 1.5

class uC_SerialCommunication:
    def __init__(self, port, baudrate):
        self.port = port    
        self.baudrate = baudrate    # Generaly 9600
        self.ser = serial.Serial(port, baudrate, timeout=TIMEOUT_RX)
        time.sleep(SLEEP_TIME)      # Wait for Arduino reset
        self.ser.flushInput()
        self.ser.flushOutput()

    def rx_message(self):
        """Receive a message from the serial port.

        Returns:
            str: Message received from the serial port.
        """
        return self.ser.readline().decode(errors="ignore").strip()
        
    ## Transmit functions
    def tx_message(self, command):
        """Transmit a message to the serial port.

        Args:
            command (Command): Command to be transmitted.
        """
        self.ser.write(command.encode())
        
    def execute_command(self, command):  
        """Execute a command. It sends through the seraial port the command message and 
        waits for the response.

        Args:
            command (Command): Command to be executed.
        """
        print("-> Sending:", command.serialize())  
           
        self.tx_message(command.serialize())
        
        print("-- Waiting for:", command.expected_response)
        
        response_status = self.rx_message()
        response_message = self.rx_message()
        
        print("<- Received:", response_message, end="\n\n")
        
        if command.expected_response == None:
            return
        
        # Check if the response is the expected one
        if response_message == command.expected_response:
            return command.on_success(self)
        else:
            return command.on_failure(self)
    
            
    def execute_custom_command(self, commands_str):
        """Execute a list of commands.

        Args:
            commands_str (list): List of commands to be executed.
        """        
        print("-> Sending:", commands_str)  
           
        self.tx_message(commands_str)
        
        response = self.rx_message()
        
        print("<- Received:", response)
        return response
        
    
if __name__ == "__main__":
    print("## uC Serial Communication")
    
    uC = uC_SerialCommunication("/dev/ttyUSB0", 9600)
    
    uC.execute_command(InfoCommand())
    uC.execute_command(TriggerCommand())
    uC.execute_command(HelpCommand())
    
    uC.execute_command(TriggerCommand(1, 2, 3, 4, 5))
    
    uC.ser.close()