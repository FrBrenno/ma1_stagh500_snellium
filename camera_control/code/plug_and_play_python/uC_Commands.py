class Command():
    def __init__(self, command=None, response=None):
        self.command = command
        self.response = response
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        pass
    
class HelloCommand(Command):
    """Establishes communication with the microcontroller.

    Args:
        Command (HelloComm): _description_
    """
    def __init__(self):
        super().__init__("hello", "hello")
        
    def on_success(self, uC):
        uC.is_active = True
        
    def on_failure(self, uC):
        print("Hello command failed")
        
class PingCommand(Command):
    """ Ping command to check if the communication is active.
    """
    def __init__(self):
        super().__init__("ping", "pong")
    
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        print("Ping command failed")
        
class TriggerCommand(Command):
    """ Trigger command to trigger cameras controlled by the microcontroller.
    """
    def __init__(self):
        super().__init__("trigger", "triggered")
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        print("Trigger command failed")
        
class InfoCommand(Command):
    """ Info command to get information from the microcontroller.
    """
    def __init__(self):
        super().__init__("info", None)
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        print("Info command failed")

class StopCommand(Command):
    """ Stop command to stop the communication with the microcontroller.
    """
    def __init__(self):
        super().__init__("stop", "stopped")
        
    def on_success(self, uC):
        uC.is_active = False
    
    def on_failure(self, uC):
        print("Stop command failed")