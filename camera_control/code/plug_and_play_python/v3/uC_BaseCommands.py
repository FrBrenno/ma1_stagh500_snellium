############################################################################################################
# Base classes for microcontroller commands
############################################################################################################
class Command():
    """ Base class for microcontroller single word commands.
    ||<COMMAND>||
    """
    def __init__(self, command=None, response=None):
        self.delimiter = '|'
        self.separator = '-'
        self.command_str = command
        self.expected_response = response
        
    def __str__(self) -> str:
        return self.serialize()
        
    def on_success(self):
        """Function to be executed when the command is successful.
        """
        print(f"Command {self.command_str} was successful.")
        return True
    
    def on_failure(self):
        """Function to be executed when the command fails.
        """
        print(f"Command {self.command_str} failed.")
        return False
    
        
    def serialize(self):
        """Serializes the command to be sent to the microcontroller.
        """
        serialized = f"{self.delimiter*2}{self.command_str}{self.delimiter*2}"
        return serialized

class CommandWithOption(Command):
    """ Base class for microcontroller commands with an option.
     ||<COMMAND>-<OPTION>||
    """
    def __init__(self, command=None, response=None, option=None):
        super().__init__(command, response)
        self.option = option
        
    def set_option(self, option):
        """Sets the option for the command."""
        self.option = option
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}"
        if self.option is not None:
            serialized += f"{self.separator}{self.option}"
        serialized += f"{self.delimiter*2}"
        return serialized
        
class CommandWithArguments(Command):
    """ Base class for microcontroller commands with arguments.
    ||<COMMAND>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
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
    
class CommandWithOptionsAndArguments(CommandWithOption, CommandWithArguments):
    """ Base class for microcontroller commands with options and arguments.
    ||<COMMAND>-<OPTION>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
    """
    def __init__(self, command=None, response=None, option=None, *args):
        super().__init__(command, response, *args)
        self.option = option
        
    def serialize(self):
        serialized = f"{self.delimiter*2}{self.command_str}"
        if self.option is not None:
            serialized += f"{self.separator}{self.option}"
        if len(self.arguments) > 0:
            serialized += f"{self.delimiter}{len(self.arguments)}{self.separator}"
            serialized += f"{self.separator.join(self.arguments)}"
        serialized += f"{self.delimiter*2}"
        return serialized