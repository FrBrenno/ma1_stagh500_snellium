############################################################################################################
# Base classes for microcontroller commands
############################################################################################################
class Command():
    """ Base class for microcontroller single word commands.
    """
    def __init__(self, command=None, response=None):
        self.delimiter = '|'
        self.separator = '-'
        self.command_str = command
        self.expected_response = response
        
    def on_success(self, uC):
        pass
    
    def on_failure(self, uC):
        pass
    
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}{self.delimiter*2}"
        return serialized

class CommandWithOption(Command):
    """ Base class for microcontroller commands with an option.
    """
    def __init__(self, command=None, response=None, option=None):
        super().__init__(command, response)
        self.option = option
        
    def set_option(self, option):
        self.option = option
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}"
        if self.option is not None:
            serialized += f"{self.separator}{self.option}"
        serialized += f"{self.delimiter*2}"
        return serialized
        
class CommandWithArguments(Command):
    """ Base class for microcontroller commands with arguments.
    """
    def __init__(self, command=None, response=None):
        super().__init__(command, response)
        self.arguments = []
        
    def __init__(self, command=None, response=None, *args):
        super().__init__(command, response)
        self.arguments = list(args)
    
    def add_argument(self, argument):
        self.arguments.append(str(argument))
    
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}"
        if len(self.arguments) > 0:
            serialized += f"{self.delimiter}{len(self.arguments)}{self.separator}"
            serialized += f"{self.separator.join(self.arguments)}"
        serialized += f"{self.delimiter*2}"
        return serialized
    
class CommandWithOptionsAndArguments(Command):
    """ Base class for microcontroller commands with options and arguments.
    """
    def __init__(self, command=None, response=None):
        super().__init__(command, response)
        self.option = None
        self.arguments = []
    
    def __init__(self, command=None, response=None, option=None):
        super().__init__(command, response)
        self.option = option
        self.arguments = []
        
    def __init__(self, command=None, response=None, option=None, *args):
        super().__init__(command, response)
        self.option = option
        self.arguments = list(args)
        
    def set_option(self, option):
        self.option = option
        
    def add_argument(self, argument):
        self.arguments.append(str(argument))
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}"
        if self.option is not None:
            serialized += f"{self.separator}{self.option}"
        if len(self.arguments) > 0:
            serialized += f"{self.delimiter}{len(self.arguments)}{self.separator}"
            serialized += f"{self.separator.join(self.arguments)}"
        serialized += f"{self.delimiter*2}"
        return serialized
    
############################################################################################################
# Command classes
############################################################################################################

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

class InfoCommand(CommandWithOption):
    """ Info command to get information from the microcontroller.
    """
    def __init__(self, option=None):
        super().__init__("info", None, option)
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Info command failed")
        return False 
        
class TriggerCommand(CommandWithOptionsAndArguments):
    """ Trigger command to trigger cameras controlled by the microcontroller.
    """        
    def __init__(self, trigger_type="all", *args):
        expected_response = "trigger " + trigger_type
        # add arguments too in he expected response like: "trigger selective 1 2 3"
        for arg in args:
            expected_response += " " + str(arg)
               
        super().__init__("trigger", expected_response, trigger_type)
        for arg in args:
            self.add_argument(str(arg))       
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Trigger command failed")
        return False

class DebugCommand(Command):
    """ Debug command to debug the microcontroller.
    """
    def __init__(self):
        super().__init__("debug", None)
        
    def on_success(self, uC):
        return True
    
    def on_failure(self, uC):
        print("Debug command failed")
        return False
    
if __name__ == "__main__":
    print("## uC Commands")
    
    ping = PingCommand()
    ping.serialize()
    
    trigger = TriggerCommand()
    trigger.serialize()
    
    trigger_sel = TriggerCommand("selective", 1, 2, 3)
    trigger_sel.serialize()
        
    info = InfoCommand()
    info.serialize()
    
    info_mcu_type = InfoCommand("mcu_type")
    info_mcu_type.serialize()
    
    info_hello = InfoCommand("hello")
    info_hello.serialize()
    
    debug = DebugCommand()
    debug.serialize()