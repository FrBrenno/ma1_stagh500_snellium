# Communication Protocol

The communication protocol between the daemon and the microcontroller is a straightforward, text-based format utilizing ASCII characters for both commands and responses.

The design ensures simplicity and ease of implementation on both the daemon and the microcontroller firmware. Commands are categorized into two types: 
- **Command** 
- **CommandWithArguments**.

#### Command Syntax

- **Command**: 
	- `STX <command_name> ETX`
- **CommandWithArguments**: 
	- `STX <command_name> GS <argument_number> US <arg_1> US <arg_2> ... US <arg_n> ETX`

Where:

- **STX**: Start of Text character (0x02), marks the beginning of the command.
- **ETX**: End of Text character (0x03), marks the end of the command.
- **GS**: Group Separator character (0x1D), used as a block delimiter.
- **US**: Unit Separator character (0x1F), used as an element delimiter.
- **command_name**: Name of the command (e.g., “info”, “ping”, “set-mode”, “trigger-all-cameras”).
- **argument_number**: Number of arguments.
- **arg_1, arg_2, ..., arg_n**: Arguments for the command.

#### Response Syntax

The microcontroller replies to each command with a message formatted as follows:

- **Response**: `STX <status> GS <command_name> US <message> GS <debug_message> ETX`

Where:
- **STX**: Start of Text character (0x02).
- **ETX**: End of Text character (0x03).
- **GS**: Group Separator character (0x1D).
- **US**: Unit Separator character (0x1F).
- **status**: Indicates the result of the command execution (e.g., success or error).
- **command_name**: Refers to the command for which the response is sent.
- **message**: Contains the data returned by the command or an error message if an internal error occurs.
- **debug_message**: Optional field providing additional debugging information, present only when in debug mode.

# Example Commands and Responses

- *Command*: `STX info ETX`
- *Response*: `STX success GS info US 12345 US microcontroller_name US board_name US microcontroller_unit_type GS ETX` 

- *Command*: `STX ping ETX `
- *Response*: `STX success GS ping US pong GS ETX` 

- *Command*: `STX set-mode GS 1 US debug ETX` 
- *Response*: `STX success GS set-mode US mode set debug GS debug_message ETX` 

- *Command*: `STX trigger-all-cameras ETX` 
- *Response*: `STX success GS trigger-all-cameras US triggered-all-cameras GS ETX` 

- *Command*: `STX invalid-command ETX` 
- *Response*: `STX internal error GS invalid-command US unknown command GS ETX`