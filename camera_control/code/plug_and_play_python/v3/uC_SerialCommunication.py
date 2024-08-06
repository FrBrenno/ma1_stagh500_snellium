import serial
import time


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
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serialComm = None
        
        self.connect_to_port()
       
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
        except serial.serialutil.SerialException:
            self.port = None
            self.serialComm = None    
            
    def disconnect_from_port(self):
        """Disconnects from the port.
        """
        if self.serialComm is not None:
            self.serialComm.close()
            self.serialComm = None
            self.port = None
    
    def send_command(self, serialized_command):
        """Sends a command to the microcontroller.
        It serializes the command and sends it to the microcontroller.
        It waits for the response and returns it.
        If the command fails, it tries to reconnect and send the command again.
        If connection is not restablished, communication is lost, and it returns None.
        """
        try:
            if self.serialComm is None:
                return None
        
            self.serialComm.write(serialized_command.encode())    
            response = self.serialComm.readline().decode().strip()
            return response
        except serial.serialutil.SerialException:
            return None