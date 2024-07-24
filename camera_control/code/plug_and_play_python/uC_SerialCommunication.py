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
        return self.ser.readline().decode().strip()
        
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
        print("## Executing command...")
        print("-> Sending:", command.command)  
           
        self.tx_message(command.command)
        
        print("- Waiting for:", command.response)
        
        response = self.rx_message()
        
        print("<- Received:", response)
        
        if command.response == None:
            print("## Command executed...")
            return
        
        # Check if the response is the expected one
        if response == command.response:
            return command.on_success(self)
        else:
            return command.on_failure(self)
        print("## Command executed...")
    
    def test_connection(self):
        """Test the connection with the microcontroller.
        """
        print("## Testing connection...")
        if self.execute_command(PingCommand()):
            print("## Connection active...")
        else:
            print("## Connection failed...")
    
if __name__ == "__main__":
    print("## uC Serial Communication")
    
    print("## Opening serial port...")
    uC = uC_SerialCommunication("/dev/ttyUSB0", 9600)
    print("## Serial port opened...")
    
    for i in range(0, random.randint(1, 2)):
        for i in range(0, random.randint(1, 10)):
            uC.execute_command(InfoCommand())
        for i in range(0, random.randint(0, 2)):
            uC.execute_command(PingCommand())
    for i in range(0, random.randint(1, 2)):
        uC.execute_command(TriggerCommand())
    uC.execute_command(HelpCommand())
    
    print("## Closing serial port...")
    uC.ser.close()
    print("## Serial port closed...")
    
    print("## uC Serial Communication")
    