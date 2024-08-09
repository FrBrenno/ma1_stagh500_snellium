############################################################################################################
# Base classes for microcontroller commands
############################################################################################################
class Command:
    """Base class for microcontroller single word commands.
    ||<COMMAND>||
    """

    def __init__(self, command=None, response=None):
        self.delimiter = "|"
        self.separator = "-"
        self.command_name = command
        self.expected_response_msg = response

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self):
        """Serializes the command to be sent to the microcontroller."""
        serialized = f"{self.delimiter*2}{self.command_name}{self.delimiter*2}"
        return serialized


class CommandWithOption(Command):
    """Base class for microcontroller commands with an option.
    ||<COMMAND>-<OPTION>||
    """

    def __init__(self, command=None, response=None, option=None):
        super().__init__(command, response)
        self.option = option

    def set_option(self, option):
        """Sets the option for the command."""
        self.option = option

    def serialize(self):
        if self.option is None:
            return super().serialize()

        # ||<COMMAND>-<OPTION>||
        return f"{self.delimiter*2}{self.command_name}{self.separator}{self.option}{self.delimiter*2}"


class CommandWithArguments(Command):
    """Base class for microcontroller commands with arguments.
    ||<COMMAND>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
    """

    def __init__(self, command=None, response=None, *args):
        super().__init__(command, response)
        self.arguments = list(args)

    def add_argument(self, argument):
        self.arguments.append(str(argument))

    def serialize(self):
        if len(self.arguments) == 0:
            return super().serialize()

        # ||<COMMAND>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
        return f"{self.delimiter*2}{self.command_name}{self.delimiter}{len(self.arguments)}{self.separator}{self.separator.join(self.arguments)}{self.delimiter*2}"


class CommandWithOptionsAndArguments(CommandWithOption, CommandWithArguments):
    """Base class for microcontroller commands with options and arguments.
    ||<COMMAND>-<OPTION>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
    """

    def __init__(self, command=None, response=None, option=None, *args):
        CommandWithOption.__init__(self, command, response, option)
        CommandWithArguments.__init__(self, command, response, *args)

    def serialize(self):
        if self.option is None and len(self.arguments) == 0:
            # print super type
            spr = super()
            print(spr)
            return super().serialize()
        elif self.option is not None and len(self.arguments) == 0:
            return CommandWithOption.serialize(self)
        elif self.option is None and len(self.arguments) > 0:
            return CommandWithArguments.serialize(self)

        # ||<COMMAND>-<OPTION>|<ARGNUMBER>-<ARGUMENT>-...-<ARGUMENT>||
        return f"{self.delimiter*2}{self.command_name}{self.separator}{self.option}{self.delimiter}{len(self.arguments)}{self.separator}{self.separator.join(self.arguments)}{self.delimiter*2}"
