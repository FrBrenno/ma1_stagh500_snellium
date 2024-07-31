import pytest

from uC_BaseCommands import *
from uC_Commands import *

class Test_BaseCommands:
    class Test_Command:
        class Test_Empty_Command:
            def setup_method(self):
                self.command = Command()
                
            def test_on_success(self):
                assert self.command.on_success() == True
                
            def test_on_failure(self):
                assert self.command.on_failure() == False
                
            def test_serialize(self):
                assert self.command.serialize() == "||None||"

        class Test_Custom_Command:
            def setup_method(self):
                self.command = Command("test", "test")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test||"
                
    class Test_CommandWithOption:
        class Test_Empty_Command:
            def setup_method(self):
                self.command = CommandWithOption()
                
            def test_serialize(self):
                assert self.command.serialize() == "||None||"
                
        class Test_Custom_Command:
            def setup_method(self):
                self.command = CommandWithOption("test", "test", "option")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test-option||"
        
    class Test_CommandWithArguments:
        class Test_Empty_Command:
            def setup_method(self):
                self.command = CommandWithArguments()
                
            def test_serialize(self):
                assert self.command.serialize() == "||None||"
        
        class Test_Custom_Command_No_Args:
            def setup_method(self):
                self.command = CommandWithArguments("test", "test")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test||"
        
        class Test_Custom_Command:
            def setup_method(self):
                self.command = CommandWithArguments("test", "test", "arg1", "arg2")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test|2-arg1-arg2||"
                
            def test_add_argument(self):
                self.command.add_argument("arg3")
                assert self.command.serialize() == "||test|3-arg1-arg2-arg3||"
                
    class Test_CommandWithOptionsAndArguments:
        class Test_Empty_Command:
            def setup_method(self):
                self.command = CommandWithOptionsAndArguments()
                
            def test_serialize(self):
                assert self.command.serialize() == "||None||"
        
        class Test_Custom_Command_No_Option_No_Args:
            def setup_method(self):
                self.command = CommandWithOptionsAndArguments("test", "test")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test||"
                
        class Test_Custom_Command_No_Option:
            def setup_method(self):
                self.command = CommandWithOptionsAndArguments("test", "test", None, "arg1", "arg2")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test|2-arg1-arg2||"
                
            def test_add_argument(self):
                self.command.add_argument("arg3")
                assert self.command.serialize() == "||test|3-arg1-arg2-arg3||"
                
        class Test_Custom_No_Args:
            def setup_method(self):
                self.command = CommandWithOptionsAndArguments("test", "test", "option")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test-option||"
                
        class Test_Custom_Command:
            def setup_method(self):
                self.command = CommandWithOptionsAndArguments("test", "test", "option", "arg1", "arg2")
                
            def test_serialize(self):
                assert self.command.serialize() == "||test-option|2-arg1-arg2||"
                
            def test_add_argument(self):
                self.command.add_argument("arg3")
                assert self.command.serialize() == "||test-option|3-arg1-arg2-arg3||"
                
            def test_set_option(self):
                self.command.set_option("option2")
                assert self.command.serialize() == "||test-option2|2-arg1-arg2||"
                
                
class Test_Commands:
    
    class Test_PingCommand:
        def setup_method(self):
            self.command = PingCommand()
            
        def test_expected_response(self):
            assert self.command.expected_response == "pong"
            
        def test_serialize(self):
            assert self.command.serialize() == "||ping||"
            
    class Test_InfoCommand:
        def setup_method(self):
            self.command = InfoCommand("option")
            
        def test_expected_response(self):
            assert self.command.expected_response == None
            
        def test_serialize(self):
            assert self.command.serialize() == "||info-option||"
            
    class Test_TriggerCommand:
        def setup_method(self):
            self.command = TriggerCommand("all", "arg1", "arg2")
            
        def test_expected_response(self):
            assert self.command.expected_response == "trigger all arg1 arg2"
            
        def test_serialize(self):
            assert self.command.serialize() == "||trigger-all|2-arg1-arg2||"
            
    class Test_DebugCommand:
        def setup_method(self):
            self.command = DebugCommand()
            
        def test_expected_response(self):
            assert self.command.expected_response == None
            
        def test_serialize(self):
            assert self.command.serialize() == "||debug||"
            
    