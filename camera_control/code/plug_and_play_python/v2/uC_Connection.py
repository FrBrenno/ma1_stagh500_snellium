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
        
    def __str__(self):
        return f"uC_Connection({self.port}, {self.baudrate}, {self.uC_id}, {self.uC_name}, {self.uC_board}, {self.uC_mcu_type})"
        
    ### Connection control functions ###
    def connect_to_port(self):
        """Connects to the port and initializes the connection.
        It sends a ping command to the microcontroller to verify the connection.
        If the connection is successful, it gathers information from the microcontroller.
        Else, it disconnects from the port.
        """
        try:
            self.serialComm = serial.Serial(self.port, self.baudrate, timeout=TIMEOUT_RX)
            time.sleep(ARDUINO_AUTORESET_DURATION)
            self.serialComm.flushInput()
            self.serialComm.flushOutput()
            print(f"Connected to port {self.port}")    
            
            response = self.send_command(PingCommand())
            if response != "":
                print("Gathering information from microcontroller...")
                self.gather_info()
                self.is_connected = True
        except serial.serialutil.SerialException:
            print(f"Failed to connect to port {self.port}")
            self.port = None
            self.serialComm = None            
            
    def disconnect(self):
        """Disconnects from the port.
        It closes the serial communication and sets the is_connected flag to False.
        """
        if self.is_connected:
            self.serialComm.close()
            self.is_connected = False
            print(f"Disconnected from port {self.port}")
    
    def verify_connection(self):
        """Verifies the connection with the microcontroller.
        It sends a ping command to the microcontroller and waits for a pong response.
        If the response is correct, it sets the is_connected flag to True.
        Else, it sets the is_connected flag to False."""
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

    
    def gather_info(self):
        """Gathers information from the microcontroller.
        It sends an info command to the microcontroller and parses the response.
        """
        response = self.send_command(InfoCommand())
        if response is not None:
            status, message, _ = self.deserialize_response(response)
            if status == "Success":
                ## info response format: "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
                info_tokens = message.split("-")    
                if len(info_tokens) == 4:
                    self.uC_id = info_tokens[0]
                    self.uC_name = info_tokens[1]
                    self.uC_board = info_tokens[2]
                    self.uC_mcu_type = info_tokens[3]
                    print("Information gathered successfully")
                    return
        print("Failed to gather information from microcontroller")
    ### End of connection control functions ###
    
    ### Communication functions ###
    def send_command(self, command, do_print=False):
        """Sends a command to the microcontroller.
        It serializes the command and sends it to the microcontroller.
        It waits for the response and returns it.
        If the command fails, it tries to reconnect and send the command again.
        If connection is not restablished, communication is lost, and it returns None.
        """
        try:
            """ ### DEBUG: Randomly raise a SerialException to test the reconnection mechanism.
            if (random.randint(0, 5) == 0):
                if (random.randint(0, 1) == 0):
                    ## Lose the connection.
                    self.disconnect()
                else:   
                    ## Connection is still active.
                    pass
                raise serial.serialutil.SerialException
            ### DEBUG
             """
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
            
            
            
    def deserialize_response(self, response):
        """Deserialize the response from the microcontroller.
        Response Format:
        ||<STATUS>|<MESSAGE> or <ERROR_MESSAGE>[|<DEBUG_MESSAGE>] if debug mode on||
        """
        
        # Default return values
        status, message, debug_message = None, None, None

        # Check if response is correctly delimited
        if response.startswith("||") and response.endswith("||"):
            # Remove delimiters
            response_content = response[2:-2]

            # Split response into tokens
            tokens = response_content.split("|")

            # Ensure the correct number of tokens
            if len(tokens) == 2 or len(tokens) == 3:
                # Extract status, message, and optional debug_message
                status, message = tokens[0], tokens[1]
                if len(tokens) == 3:
                    debug_message = tokens[2]
                
                # Validate status
                if status not in {"Success", "Error"}:
                    status, message, debug_message = None, None, None
        
        return status, message, debug_message

    ### End of communication functions ###

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
        
        
    