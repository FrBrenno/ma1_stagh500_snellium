from software.uC_BaseCommands import Command
############################################################################################################
# Command classes
############################################################################################################

class PingCommand(Command):
    """ Ping command to check if the communication is active.
    """
    def __init__(self):
        """Initializes the ping command.
        Expected response message is "pong".
        """
        super().__init__("ping", "pong")
        
class TriggerCommand(Command):
    """ Trigger command to trigger cameras controlled by the microcontroller.
    Options are:
    - all: trigger all the cameras (no arguments needed) 
    - select: trigger selected cameras (arguments needed)
    
    Arguments are the camera numbers to trigger.
    """        
    def __init__(self):
        """Initializes the trigger command.

        Args:
            trigger_type (str, optional): Option of triggering. Defaults to "all".
        """
       
        super().__init__("trigger", "Success: All cameras were triggered")