from uC_BaseCommands import Command, CommandWithOption, CommandWithOptionsAndArguments
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


class InfoCommand(CommandWithOption):
    """ Info command to get information from the microcontroller.
    Option defines the type of information to get and these are the possible options:
    - "": get all the information
    - id: get the uC id
    - name: get the uC name
    - board: get the uC board
    - mcu: get the uC microcontroller type
    """
    def __init__(self, option=None):
        """Initializes the info command.
        Args:
            option (str): The option to get the information. Default is None and gets all the information.
            
        No expected response message for info command
        """
        super().__init__("info", None, option)
        
        
class TriggerCommand(CommandWithOptionsAndArguments):
    """ Trigger command to trigger cameras controlled by the microcontroller.
    Options are:
    - all: trigger all the cameras (no arguments needed) 
    - select: trigger selected cameras (arguments needed)
    
    Arguments are the camera numbers to trigger.
    """        
    def __init__(self, trigger_option="all", *args):
        """Initializes the trigger command.

        Args:
            trigger_type (str, optional): Option of triggering. Defaults to "all".
        """
        expected_response_msg = "trigger " + trigger_option
        # add arguments too in he expected response like: "trigger select 1 2 3"
        for arg in args:
            expected_response_msg += " " + str(arg)
               
        super().__init__("trigger", expected_response_msg, trigger_option)
        for arg in args:
            self.add_argument(str(arg))       
        

class DebugCommand(Command):
    """ Debug command to debug the microcontroller.
    Sets the microcontroller in debug mode which returns debug messages.
    """
    def __init__(self):
        """Initializes the debug command.
        No expected response message for debug command
        """
        super().__init__("debug", None)

if __name__ == "__main__":
    ping = PingCommand().serialize()
    info = InfoCommand().serialize()
    info_id = InfoCommand("ucid").serialize()
    info_board = InfoCommand("board").serialize()
    info_mcu = InfoCommand("mcu_type").serialize()
    info_device_name = InfoCommand("custom_name").serialize()
    trigger_all = TriggerCommand().serialize()
    trigger_select = TriggerCommand("select", 1, 2, 3).serialize()
    debug = DebugCommand().serialize()
    
    assert ping == "||ping||"
    assert info == "||info||"
    assert info_id == "||info-ucid||"
    assert info_board == "||info-board||"
    assert info_mcu == "||info-mcu_type||"
    assert info_device_name == "||info-custom_name||"
    assert trigger_all == "||trigger-all||"
    assert trigger_select == "||trigger-select|3-1-2-3||"
    assert debug == "||debug||"
