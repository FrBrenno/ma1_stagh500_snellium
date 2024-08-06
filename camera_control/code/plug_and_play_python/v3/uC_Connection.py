from uC_SerialCommunication import uC_SerialCommunication
from uC_Commands import *
from colors import bcolors

class uC_Connection:
    """This class is responsible for establishing and maintaining a connection with a microcontroller.
    """
    def __init__(self, port=None, baudrate=9600):
        self.uC_name = "Unknown"
        self.uC_board = "Board Unknown"
        self.uC_mcu_type = "MCU Unknown"
        self.uC_id = None
        self.serialComm = None
        self.is_connected = False
        
        self.connect_to_port(port, baudrate)
        
    def __str__(self):
        return f"uC_Connection: {self.uC_id}, {self.uC_name}, {self.uC_board}, {self.uC_mcu_type}"
        
    ### Connection control functions ###
    def connect_to_port(self, port, baudrate=9600):
        """Creates a serial communication object and connects to the port.
        """
        if port is None:
            print("No port specified")
            return
        
        self.serialComm = uC_SerialCommunication(port, baudrate)
        if self.verify_connection():
            print(f"Connected to port {port}")
            print("Gathering information from microcontroller...")
            self.gather_info()
            self.is_connected = True
        else:
            print(f"Failed to connect to port {port}")
            self.disconnect()
            
    def disconnect(self):
        """Disconnects from the port.
        """
        if self.is_connected:
            self.serialComm.disconnect_from_port()
            self.is_connected = False
            self.reset_uC_info()
            print("Disconnected from port")

    def reset_uC_info(self):
        """Resets the microcontroller information.
        """
        self.uC_id = None
        self.uC_name = "Unknown"
        self.uC_board = "Board Unknown"
        self.uC_mcu_type = "MCU Unknown"
    
    def verify_connection(self):
        """Verifies the connection with the microcontroller.
        It sends a ping command to the microcontroller and waits for a pong response.
        If the response is correct, it sets the is_connected flag to True.
        Else, it sets the is_connected flag to False."""
        if self.serialComm is None:
            return False
        response = self.send_command(PingCommand())
        status, message, _ = self.deserialize_response(response)
        if  status == "Success" and message == "pong":
            self.is_connected = True
            return True
        else:
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
                uC_id, uC_name, uC_board, uC_mcu_type = self.deserialize_info_response(message)
                self.uC_id = uC_id
                self.uC_name = uC_name
                self.uC_board = uC_board
                self.uC_mcu_type = uC_mcu_type
                print("Information gathered successfully")
                return
        print("Failed to gather information from microcontroller")

    def send_command(self, command, do_print=False):
        """Sends a command to the microcontroller.
        It serializes the command and sends it to the microcontroller.
        Always waits for the response and returns it, even if it is None.
        """
        serialized_command = command.serialize()
        response = self.serialComm.send_command(serialized_command)
        if do_print:
            print(f"{bcolors.OKBLUE}-->: {str(command)}{bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}<--: {response}{bcolors.ENDC}")
        return response
    
    def deserialize_response(self, response):
        """Deserialize the response from the microcontroller.
        Response Format:
        ||<STATUS>|<MESSAGE> or <ERROR_MESSAGE>[|<DEBUG_MESSAGE>] if debug mode on||
        """
        status, message, debug_message = None, None, None
        if response is None:
            return status, message, debug_message
        
        # Check if response is correctly delimited
        if not (response.startswith("||") and response.endswith("||")):
            return status, message, debug_message
        response_content = response[2:-2]
        tokens = response_content.split("|")
        if not(len(tokens) == 2 or len(tokens) == 3):    # Ensure the correct number of tokens
            return status, message, debug_message
        
        status, message = tokens[0], tokens[1]
        if len(tokens) == 3:
            debug_message = tokens[2]
        if status not in {"Success", "Error"}:
            status, message, debug_message = None, None, None
        return status, message, debug_message

    def deserialize_info_response(self, response):
        """Deserialize the info response from the microcontroller.
        Info Response Format:
        "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
        """
        info_tokens = response.split("-")
        if len(info_tokens) == 4:      
            # info response format: "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
            uC_id, uC_name, uC_board, uC_mcu_type = info_tokens
            return uC_id, uC_name, uC_board, uC_mcu_type
        elif len(info_tokens) == 1:
            return info_tokens[0], None, None, None
        else:
            return None, None, None, None
            
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
        uC = uC_Connection(port)
        if uC.is_connected:
            for command in command_set:
                uC.send_command(command, do_print=True)
        
        uC.disconnect()
        print("##############################")
        
        
    