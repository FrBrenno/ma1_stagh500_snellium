import uC_BaseCommands
############################################################################################################
# Command classes
############################################################################################################

class PingCommand(uC_BaseCommands.Command):
    """ Ping command to check if the communication is active.
    """
    def __init__(self):
        super().__init__("ping", "pong")


class InfoCommand(uC_BaseCommands.CommandWithOption):
    """ Info command to get information from the microcontroller.
    """
    def __init__(self, option=None):
        super().__init__("info", None, option)
        
        
class TriggerCommand(uC_BaseCommands.CommandWithOptionsAndArguments):
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
        

class DebugCommand(uC_BaseCommands.Command):
    """ Debug command to debug the microcontroller.
    """
    def __init__(self):
        super().__init__("debug", None)

    
# TODO: Unit tests