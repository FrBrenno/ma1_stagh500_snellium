from colors import bcolors
from .uC_Commands import DebugCommand, InfoCommand, PingCommand, TriggerCommand
from .uC_SerialCommunication import uC_SerialCommunication


class uC_Connection:
    """This class is responsible for establishing and maintaining a connection with a microcontroller."""

    def __init__(self, port, baudrate):
        self.is_info_initialized = (
            False  # Flag to indicate if the information is gathered
        )
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
        connectivity = "Connected" if self.is_connected else "Disconnected"
        return f"{self.port} ({connectivity}): {self.uC_id}, {self.uC_name}, {self.uC_board}, {self.uC_mcu_type}"

    def __print__(self):
        print(self.__str__())

    ### Connection control functions ###
    def connect_to_port(self):
        """Creates a serial communication object and connects to the port."""
        if self.port is None:
            print("No port specified")
            return

        self.serialComm = uC_SerialCommunication(self.port, self.baudrate)
        if self.verify_connection():
            print(f"Connected to port {self.port}")
            if not self.is_info_initialized:
                print("Gathering information from microcontroller...")
                self.gather_info()
                self.is_info_initialized = True
            self.is_connected = True
        else:
            print(f"Failed to connect to port {self.port}")
            self.disconnect()

    def disconnect(self):
        """Disconnects from the port."""
        if self.is_connected:
            self.serialComm.disconnect_from_port()
            self.is_connected = False

    def verify_connection(self):
        """Verifies the connection with the microcontroller.
        It sends a ping command to the microcontroller and waits for a pong response.
        If the response is correct, it sets the is_connected flag to True.
        Else, it sets the is_connected flag to False."""
        if self.serialComm is None:
            return False
        response = self.send_command(PingCommand())
        status, message, _ = self.deserialize_response(response)
        if status == "Success" and message == "pong":
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
                uC_id, uC_name, uC_board, uC_mcu_type = self.deserialize_info_response(
                    message
                )
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
        DebugCommand(),
    ]

    device_ports = [
        "/dev/ttyUSB0",
        "/dev/ttyUSB1",
    ]

    for port in device_ports:
        print(f"## Testing port {port}...")
        uC = uC_Connection(port, 9600)
        if uC.is_connected:
            for command in command_set:
                uC.send_command(command, do_print=True)

        uC.disconnect()
        print("##############################")
