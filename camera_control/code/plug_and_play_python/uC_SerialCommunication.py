import serial
import time
import threading

import serial.serialutil
import serial.tools
import serial.tools.list_ports

from uC_Commands import *

### Sleep time between port opening and command execution.
### This is necessary because of Arduino auto-reset feature.
### Whenever a serial communication is established, the Arduino resets and
### the bootloader needs some time to run before accepting commands.
ARDUINO_AUTORESET_DURATION = 1.62 #seconds
### Timeout for serial communication.
### This is the time the program waits for a response from the Arduino.
### Needed because of readline() function.
TIMEOUT_RX = 1.5 #seconds
### Period for scanning the ports.
### This is the time the program waits before scanning for the uC again.
THREAD_SCANNING_PERIOD = 5 #seconds

class uC_SerialCommunication:
    def __init__(self, baudrate):
        self.baudrate = baudrate    # Generaly 9600
        self.port = self.scan_for_uC()
        self.serialComm = serial.Serial(baudrate=self.baudrate, timeout=TIMEOUT_RX)
        
        if self.port != None:
            self.serialComm.port = self.port
            self.serialComm.open()
            time.sleep(ARDUINO_AUTORESET_DURATION)
            self.serialComm.flushInput()
            self.serialComm.flushOutput()                                           
        
    def scan_for_uC(self):
        """ Return the port to which the uC is connected.
        The software executes a info-hello command to every port and waits for the response.
        If the response is the expected one, the port is returned.
        Expected response: "INFO: hello"
        """
        port_list = serial.tools.list_ports.comports()
        for port in port_list:
            print("Testing port:", port.device)
            try:
                # Opening the port
                serialComm = serial.Serial(port.device, 9600, timeout=TIMEOUT_RX)
                time.sleep(ARDUINO_AUTORESET_DURATION)
                serialComm.flushInput()
                serialComm.flushOutput()
                # Sending the hello command
                serialComm.write(InfoCommand("hello").serialize().encode())
                response = serialComm.readline().decode(errors="ignore").strip()
                # Evaluating the response                
                if response == "INFO: hello":
                    print("uC found at port:", port.device)
                    return port.device
            except serial.serialutil.SerialException:
                pass
        return None 
            
    def rx_message(self):
        """Receive a message from the serial port.

        Returns:
            str: Message received from the serial port.
        """
        return self.serialComm.readline().decode(errors="ignore").strip()
        
    ## Transmit functions
    def tx_message(self, command):
        """Transmit a message to the serial port.

        Args:
            command (Command): Command to be transmitted.
        """
        self.serialComm.write(command.encode())
        
    def execute_command(self, command):  
        """Execute a command. It sends through the seraial port the command message and 
        waits for the response.

        Args:
            command (Command): Command to be executed.
        """
        
        print("-> Sending:", command.serialize())     
        self.tx_message(command.serialize())
        
        print("-- Waiting for:", command.expected_response)
        
        response_message = self.rx_message()
        print("<- Received:", response_message, end="\n\n")
        
        if command.expected_response == None:
            return
        
        # Check if the response is the expected one
        if response_message == command.expected_response:
            return command.on_success(self)
        else:
            return command.on_failure(self)
    
    def close(self):
        self.serialComm.close()
    
if __name__ == "__main__":
    print("## uC Serial Communication")
    
    uC = uC_SerialCommunication(9600)
    
    uC.execute_command(PingCommand())
    uC.execute_command(InfoCommand())
    uC.execute_command(InfoCommand("ucid"))  
    uC.execute_command(TriggerCommand())
    uC.execute_command(TriggerCommand("selective", 1, 4))
    uC.execute_command(DebugCommand())
    uC.execute_command(DebugCommand()) 
    
    uC.close()