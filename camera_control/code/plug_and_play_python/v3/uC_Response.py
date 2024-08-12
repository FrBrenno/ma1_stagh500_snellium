

class uC_Response:
    """This class manages uC response string.
    """
    def __init__(self, serialized_response=None):
        self.status = None
        self.message = None
        self.debug_message = None
        self.ser_response = serialized_response
        
        if self.ser_response != None:
            self.deserialize()
        
    def set_serialized_response(self, response):
        self.ser_response = response
        
    def deserialize(self):
        """Deserialize the response from the microcontroller.
        Response Format:
        ||<STATUS>|<MESSAGE> or <ERROR_MESSAGE>[|<DEBUG_MESSAGE>] if debug mode on||
        """
        if self.ser_response is None or (not (self.ser_response.startswith("||") and self.ser_response.endswith("||"))):
            return

        response_content = self.ser_response[2:-2]
        tokens = response_content.split("|")
        if not (len(tokens) == 2 or len(tokens) == 3) or tokens[0] not in {"Success", "Error"}:
            return

        self.status, self.message = tokens[0], tokens[1]
        if len(tokens) == 3:
            self.debug_message = tokens[2]
       
    def deserialize_info_message(self, response):
        """Deserialize the info response from the microcontroller.
        Info Response Format:
        "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
        """
        info_tokens = response.split("-")
        if len(info_tokens) == 4:
            # info response format: "<uC_id>-<uC_name>-<uC_board>-<uC_mcu_type>"
            uC_id, uC_name, uC_board, uC_mcu_type = info_tokens
            return uC_id, uC_name, uC_board, uC_mcu_type
        elif len(info_tokens) == 1:
            return info_tokens[0], None, None, None
        else:
            return None, None, None, None
        
        
        
if __name__ == "__main__":
    resp = uC_Response("||Success|pong||")
    
    resp.deserialize()
    
    print(resp.status)
    print(resp.message)
    print(resp.debug_message)