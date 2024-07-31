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
        return True
    
    def on_failure(self, uC):
        return False
    
        
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
    