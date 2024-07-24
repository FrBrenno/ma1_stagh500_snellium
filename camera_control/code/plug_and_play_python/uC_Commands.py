class Command():
    def __init__(self, command=None, response=None):
        self.command = command
        self.response = response
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        pass
    
class PingCommand(Command):
    """ Ping command to check if the communication is active.
    """
    def __init__(self):
        super().__init__("ping", "pong")
    
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Ping command failed")
        return False
        
class TriggerCommand(Command):
    """ Trigger command to trigger cameras controlled by the microcontroller.
    """
    def __init__(self):
        super().__init__("trigger", "triggered")
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Trigger command failed")
        return False
        
class InfoCommand(Command):
    """ Info command to get information from the microcontroller.
    """
    def __init__(self):
        super().__init__("info", None)
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Info command failed")
        return False
    
class HelpCommand(Command):
    """ Help command to get help from the microcontroller.
    """
    def __init__(self):
        super().__init__("help", None)
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Help command failed")
        return False
