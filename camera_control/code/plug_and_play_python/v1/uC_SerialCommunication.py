import serial
import time

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

class uC_SerialCommunication:
    def __init__(self, baudrate, port=None):
        self.baudrate = baudrate    # Generaly 9600
        self.port_list = set(serial.tools.list_ports.comports())
        self.port = port or self.scan_for_uC_port(self.port_list)
        self.serialComm = None
        
        if self.port != None:
            self.connect_to_port(self.port)
        else:
            self.monitor_ports()
        
    def connect_to_port(self, port):
        try:
            self.serialComm = serial.Serial(port, self.baudrate, timeout=TIMEOUT_RX)
            time.sleep(ARDUINO_AUTORESET_DURATION)
            self.serialComm.flushInput()
            self.serialComm.flushOutput()
            print(f"Connected to port {port}")
        except serial.serialutil.SerialException:
            print(f"Failed to connect to port {port}")
            self.port = None
            self.serialComm = None
                                                   
    def is_uC_port(self, serialComm):
        serialComm.write(PingCommand().serialize().encode())    
        response = serialComm.readline().decode().strip()
        if response == "||Success|pong||":
            return True
        else:
            return False         
    
    def scan_for_uC_port(self, port_list):
        """Scan the ports and return the first available one.
        """
        for port in port_list:
            try:
                print(f"Scanning port {port.device}")
                serialComm = serial.Serial(port.device, self.baudrate, timeout=TIMEOUT_RX)
                time.sleep(ARDUINO_AUTORESET_DURATION)
                if self.is_uC_port(serialComm):
                    print(f"uC found in port {port.device}")
                    return port.device
                serialComm.close()
            except serial.serialutil.SerialException:
                pass
        return None
    
    def monitor_ports(self):
        """Monitor the ports to find the uC port.
        """
        while self.port == None:
            print("Monitoring ports...")
            current_port_list = set(serial.tools.list_ports.comports())
            new_ports = current_port_list - self.port_list
            
            if len(new_ports) > 0: ## Try to connect to the new ports
                print("New ports found")
                self.port_list = current_port_list
                self.port = self.scan_for_uC_port(new_ports)
                if self.port != None:
                    self.connect_to_port(self.port)
            
            time.sleep(3)
    
            
    def rx_message(self):
        """Receive a message from the serial port.
        Response format: 
        ||Success|<Message>|| or ||Success|<Message>|<DebugMessage>||
        or
        ||Error|<ErrorMessage>|| or ||Error|<ErrorMessage>|<DebugMessage>||
        
        Returns:
            str: Message received from the serial port.
        """
        response = self.serialComm.readline().decode().strip()
        # Verify if response is correctly formatted
        if response[0:2] != "||" or response[-2:] != "||":
            return None, None, None
        
        # Remove the delimiters
        response = response[2:-2]
        # Split the response in tokens
        tokens = response.split("|")
        
        # Verify if the status is valid and if the number of tokens is correct
        if tokens[0] != "Success" and tokens[0] != "Error":
            return None, None, None
    
        if len(tokens) == 2:
            return tokens[0], tokens[1], None
        elif len(tokens) == 3:
            return tokens[0], tokens[1], tokens[2]
        else:
            return None, None, None
        
    ## Transmit functions
    def tx_message(self, command):
        """Transmit a message to the serial port.

        Args:
            command (Command): Command to be transmitted.
        """
        self.serialComm.write(command.encode())
        
    def execute_command(self, command, do_print=True):  
        """Execute a command. It sends through the seraial port the command message and 
        waits for the response.

        Args:
            command (Command): Command to be executed.
        """
        try:
            if do_print:
                print("-> Sending:", command.serialize())     
                print("-- Waiting for:", command.expected_response)
            self.tx_message(command.serialize())
            
            status, message, debug_message = self.rx_message()
            if do_print:
                print(f"<- Received: ({status}) {message}" + (f" | {debug_message}" if debug_message != None else "") +"\n\n")
            
            # If an expected response is defined, check if the response is the expected one
            if command.expected_response != None:
                if message == command.expected_response:
                    return command.on_success(self)
                else:
                    return command.on_failure(self)
            else:
                if status == "Success":
                    return command.on_success(self)
                else:
                    return command.on_failure(self)
        except serial.serialutil.SerialException:
            print("Serial communication error")
            self.port = None
            self.monitor_ports()
            if self.port != None:
                self.execute_command(command)
            return False
    
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
    uC.execute_command(TriggerCommand("selective", "cam_1", "cam_2", "cam_3", "cam_4", "cam_5", "cam_6", "cam_7", "cam_8", "cam_9", "cam_10"))
    
    
    uC.close()