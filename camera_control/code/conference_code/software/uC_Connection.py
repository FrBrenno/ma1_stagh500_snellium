from software.colors import bcolors
from software.uC_Commands import PingCommand, TriggerCommand
from software.uC_SerialCommunication import uC_SerialCommunication


class uC_Connection:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

        self.serialComm = None
        self.is_connected = False

        self.connect_to_port()

    def __str__(self):
        connectivity = "Connected" if self.is_connected else "Disconnected"
        return f"{self.port} ({connectivity})"

    def __print__(self):
        print(self.__str__())

    ### Connection control functions ###
    def connect_to_port(self):
        if self.port is None:
            print("No port specified")
            return

        self.serialComm = uC_SerialCommunication(self.port, self.baudrate)
        if self.verify_connection():
            print(f"Connected to port {self.port}")
            self.is_connected = True
        else:
            print(f"{bcolors.FAIL}Failed to connect to port {self.port}{bcolors.ENDC}")
            self.disconnect()

    def disconnect(self):
        """Disconnects from the port."""
        if self.is_connected:
            self.serialComm.disconnect_from_port()
            self.is_connected = False

    def verify_connection(self):
        if self.serialComm is None:
            return False
        response = self.send_command(PingCommand())
        if response == "Success":
            self.is_connected = True
            return True
        else:
            self.is_connected = False
            return False

    def send_command(self, command, do_print=False):
        serialized_command = command.serialize()
        response = self.serialComm.send_command(serialized_command)
        if do_print:
            print(f"{bcolors.OKBLUE}-->: {str(command)}{bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}<--: {response}{bcolors.ENDC}")
        return response
