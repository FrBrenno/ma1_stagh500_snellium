import serial
import time

SLEEP_TIME = 1.62 ### WTF

class Command():
    def __init__(self):
        self.command = None
        self.response = None
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        pass
    
class HelloCommand(Command):
    def __init__(self):
        self.command = "hello"
        self.response = "hello"
        
    def on_success(self, uC):
        uC.is_active = True
        
    def on_failure(self, uC):
        print("Hello command failed")
        
class PingCommand(Command):
    def __init__(self):
        self.command = "ping"
        self.response = "pong"
    
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        print("Ping command failed")
        
class TriggerCommand(Command):
    def __init__(self):
        self.command = "trigger"
        self.response = "triggered"
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        print("Trigger command failed")
        
class StopCommand(Command):
    def __init__(self):
        self.command = "stop"
        self.response = "stopped"
        
    def on_success(self, uC):
        uC.is_active = False
    
    def on_failure(self, uC):
        print("Stop command failed")

class uC_SerialCommunication:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=2)
        self.ser.flushInput()
        self.ser.flushOutput()
        
        self.is_active = False

    ## Receive functions     
    def rx_message(self):
        return self.ser.readline().decode().strip()
        
    ## Transmit functions
    def tx_message(self, command):
        self.ser.write(command.encode())
        
    def execute_command(self, command):  
        print("## Executing command...")
        print("-> Sending:", command.command)     
        self.tx_message(command.command)
        print("- Waiting for:", command.response)
        response = self.rx_message()
        print("<- Received:", response)
        if response == command.response:
            command.on_success(self)
        else:
            command.on_failure(self)
        print("## Command executed...")
        
    
if __name__ == "__main__":
    print("## uC Serial Communication")
    
    print("## Opening serial port...")
    uC = uC_SerialCommunication("/dev/ttyUSB0", 9600)
    print("## Serial port opened...")
    time.sleep(SLEEP_TIME)
    uC.execute_command(HelloCommand())
    uC.execute_command(PingCommand())
    uC.execute_command(StopCommand())
    """ 
    while True:
        inpt = input("Enter command: ")
        if inpt == "hello":
            uC.execute_command(HelloCommand())
        elif inpt == "ping":
            uC.execute_command(PingCommand())
        elif inpt == "trigger":
            uC.execute_command(TriggerCommand())
        elif inpt == "stop":
            uC.execute_command(StopCommand())
        elif inpt == "exit":
            break
        else:
            print("Invalid command")
    """
    """ 
    print("## Sending hello command...")
    uC.execute_command(HelloCommand())
    
    while uC.is_active:
        for i in range(5):
            print("## Sending ping command...")
            uC.execute_command(PingCommand())
            time.sleep(1)
        
        print("## Sending trigger command...")
        uC.execute_command(TriggerCommand())
        
        print("## Sending stop command...")
        uC.execute_command(StopCommand())
    """
    print("## Closing serial port...")
    uC.ser.close()
    print("## Serial port closed...")
    
    print("## uC Serial Communication")
    