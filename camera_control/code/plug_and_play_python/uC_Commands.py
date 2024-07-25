class Command():
    def __init__(self, command=None, response=None):
        self.delimiter = '|'
        self.command_str = command
        self.expected_response = response
        self.arguments = []
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        pass
    
    def add_argument(self, arg):
        self.arguments.append(str(arg))

    def show_arguments(self):
        print("Arguments:", self.arguments)
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}{self.delimiter}"
        if len(self.arguments) > 0:
            serialized += f"{len(self.arguments)}:"
            serialized += f"{self.delimiter.join(self.arguments)}{self.delimiter}"
            serialized += f"{self.delimiter}"
        serialized += f"{self.delimiter}"
        return serialized
    
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
        
    def __init__(self, *args):
        super().__init__("trigger", "triggered")
        for arg in args:
            self.add_argument(arg)
        
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


if __name__ == "__main__":
    print("## uC Commands")
    
    ping = PingCommand()
    ping.serialize()
    
    trigger = TriggerCommand()
    trigger.add_argument("1")
    trigger.add_argument("2")
    trigger.serialize()
    
    trigger2 = TriggerCommand(1, 2, 3, 4, 5)
    trigger2.serialize()
    
    info = InfoCommand()
    info.serialize()
    
    help = HelpCommand()
    help.serialize()
    