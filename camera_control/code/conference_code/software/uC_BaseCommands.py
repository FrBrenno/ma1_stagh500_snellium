############################################################################################################
# Base classes for microcontroller commands
############################################################################################################
class Command:
    """Base class for microcontroller single word commands.
    """

    def __init__(self, command=None, response=None):
        self.command_name = command
        self.expected_response_msg = response

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self):
        """Serializes the command to be sent to the microcontroller."""
        serialized = f"{self.command_name}"
        return serialized