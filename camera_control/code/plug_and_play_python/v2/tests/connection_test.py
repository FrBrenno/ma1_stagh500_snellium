import pytest

from uC_Connection import *

class Test_Connection_Functions:
    response = [
            ("Success|PONG", None, None, None), # Not correctly delimited
            ("||Success|PONG", None, None, None), # Correctly formatted
            ("||Success||", None, None, None), # Not enough tokens: missing message
            ("||Success|PONG||", "Success", "PONG", None), # Correctly formatted without debug message
            ("||Error|PONG_ERROR||", "Error", "PONG_ERROR", None), # Correctly formatted with error
            ("||CONGRATULATIONS|PONG||", None, None, None), # Correctly formatted without debug message but wrong status
            ("||Success|PONG|DEBUG||", "Success", "PONG", "DEBUG"), # Correctly formatted with debug message
            ("||Error|PONG|DEBUG||", "Error", "PONG", "DEBUG"), # Correctly formatted with error and debug message
            ("||Success|PONG|DEBUG||||Success|PONG|DEBUG||", None, None, None) # Too many tokens
        ]
    def setup_method(self):
        self.uC = uC_Connection("/dev/ttyUSB0", 9600)
        
    
    def test_deserialize_response(self):
        for i, response in enumerate(self.response):
            status, message, debug_message = self.uC.deserialize_response(response[0])
            assert status == response[1], f"({i}) Expected: {response[1]} | Received: {status}"
            assert message == response[2], f"({i}) Expected: {response[2]} | Received: {message}"
            assert debug_message == response[3], f"({i}) Expected: {response[3]} | Received: {debug_message}"
        
class Test_BAD_Connection:
    def setup_method(self):
        self.uC = uC_Connection("/dev/ttyUSB1", 9600)
        
    def test_is_connected(self):
        assert self.uC.is_connected == False
        
    def test_connection(self):
        self.uC.connect_to_port()
        assert self.uC.is_connected == False
        self.uC.disconnect()
        assert self.uC.is_connected == False
        
    def test_verify_connection(self):
        assert self.uC.verify_connection() == False
        self.uC.connect_to_port()
        assert self.uC.verify_connection() == False
        self.uC.disconnect()
        assert self.uC.verify_connection() == False
        
    
class Test_GOOD_Connection:
    def setup_method(self):
        self.uC = uC_Connection("/dev/ttyUSB0", 9600)
        
    def test_is_connected(self):
        assert self.uC.is_connected == True
        
    def test_connection(self):
        self.uC.connect_to_port()
        assert self.uC.is_connected == True
        self.uC.disconnect()
        assert self.uC.is_connected == False
        
    def test_verify_connection(self):
        self.uC.connect_to_port()
        assert self.uC.verify_connection() == True
        self.uC.disconnect()
        assert self.uC.verify_connection() == False
        
    def test_send_command(self):
        response = self.uC.send_command(PingCommand())
        status, _, _ = self.uC.deserialize_response(response)
        assert status == "Success"
        response = self.uC.send_command(InfoCommand())
        status, _, _ = self.uC.deserialize_response(response)
        assert status == "Success"
        response = self.uC.send_command(DebugCommand())
        status, _, _ = self.uC.deserialize_response(response)
        assert status == "Success"
        self.uC.send_command(DebugCommand())
        
    def test_handling_SerialException(self):
        self.uC.disconnect()
        response = self.uC.send_command(PingCommand())
        assert response == None
        
        