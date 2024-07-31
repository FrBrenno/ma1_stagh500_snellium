import random
import serial
import time

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

class uC_Connection:
    """This class is responsible for establishing and maintaining a connection with a microcontroller.
    """
    def __init__(self, port, baudrate):
        self.uC_name = "Unknown"
        self.uC_board = "Board Unknown"
        self.uC_mcu_type = "MCU Unknown"
        self.uC_id = None
        self.port = port
        self.baudrate = baudrate
        self.serialComm = None
        self.is_connected = False
        
        self.connect_to_port()
        
    def connect_to_port(self):
        try:
            self.serialComm = serial.Serial(self.port, self.baudrate, timeout=TIMEOUT_RX)
            time.sleep(ARDUINO_AUTORESET_DURATION)
            self.serialComm.flushInput()
            self.serialComm.flushOutput()
            print(f"Connected to port {self.port}")
            
            print(f"Gathering information from microcontroller...")
            self.gather_info()
            self.is_connected = True
        except serial.serialutil.SerialException:
            print(f"Failed to connect to port {self.port}")
            self.port = None
            self.serialComm = None
            
            
    def disconnect(self):
        if self.is_connected:
            self.serialComm.close()
            self.is_connected = False
            print(f"Disconnected from port {self.port}")
    
    def verify_connection(self):
        if self.serialComm is None:
            return False
        try:
            self.serialComm.write(PingCommand().serialize().encode())
            response = self.serialComm.readline().decode().strip()
            if response == "||Success|pong||":
                self.is_connected = True
                return True
        except serial.serialutil.SerialException:
            pass
        self.is_connected = False
        return False
    
    def deserialize_response(self, response):
        """Deserialize the response from the microcontroller.
        Response Format:
        ||<STATUS>|<MESSAGE> or <ERROR_MESSAGE>[|<DEBUG_MESSAGE>] if debug mode on||
        """
        
        # Verify if response if correctly delimited.
        if response[0:2] != "||" or response[-2:] != "||":
            return None, None, None
        # Remove delimiters.
        response = response[2:-2]
        
        # Split response into tokens
        tokens = response.split("|")
        if len(tokens) < 2:
            return None, None, None
        
        status = tokens[0]
        message = tokens[1]
        debug_message = None
        if len(tokens) == 3:
            debug_message = tokens[2]
        
        if status != "Success" and status != "Error":
            return None, None, None
        
        return status, message, debug_message
        
    def send_command(self, command, do_print=False):
        try:
            ### DEBUG: Randomly raise a SerialException to test the reconnection mechanism.
            if (random.randint(0, 5) == 0):
                if (random.randint(0, 1) == 0):
                    ## Lose the connection.
                    self.disconnect()
                else:   
                    ## Connection is still active.
                    pass
                raise serial.serialutil.SerialException
            ### DEBUG
            
            if do_print:
                print(f"--> {command.serialize()}")
                print(f"-- expecting: {command.expected_response}")
                
            self.serialComm.write(command.serialize().encode())    
            response = self.serialComm.readline().decode().strip()
            
            if do_print:
                print(f"<-- {response}\n")
            return response
        except serial.serialutil.SerialException:
            ## If the command fails, try to reconnect and send the command again.
            print(f"Failed to send command {command.serialize()}")
            if self.verify_connection():
                print("Connection is still active\n")
                return self.send_command(command, do_print=True)
            else:
                if not self.is_connected:
                    print("Connection is not active\n")
                else:
                    ## If the connection is lost, return None.
                    print("Connection is lost\n")
                self.disconnect()
                return None
            
    def gather_info(self):
        response = self.send_command(InfoCommand())
        if response is not None:
            status, message, _ = self.deserialize_response(response)
            if status == "Success":
                ## info response format: "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
                info = message.split("-")
                if len(info) == 4:
                    self.uC_id = info[0]
                    self.uC_name = info[1]
                    self.uC_board = info[2]
                    self.uC_mcu_type = info[3]
                    print("Information gathered successfully")
                    return
        print("Failed to gather information from microcontroller")


if __name__ == "__main__":
    command_set = [
        PingCommand(),
        InfoCommand(),
        InfoCommand("ucid"),
        InfoCommand("custom_name"),
        InfoCommand("board"),
        InfoCommand("mcu_type"),
        TriggerCommand("all"),
        TriggerCommand("select", 1, 2, 3),
        DebugCommand()
    ]
    
    device_ports = [
        "/dev/ttyUSB0",
        "/dev/ttyUSB1",
    ]
    
    for port in device_ports:
        print(f"## Testing port {port}")
        uC = uC_Connection(port, 9600)
        if uC.is_connected:
            for command in command_set:
                uC.send_command(command, do_print=True)
        
        uC.disconnect()
        print("##############################")
        
        
    