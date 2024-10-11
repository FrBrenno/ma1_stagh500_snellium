# Project Documentation - Serial Microcontroller

The aim of this document is to explain the structure of the microcontroller's code and the important concepts that are
not easy to learn about Renesas IDE e² studio and its Smart Configurator.

## The Project

The project consists in creating a control module powered by a microcontroller that would execute command based on
communication with the main software. This command-response architecture implies that the microcontroller is always
waiting for the command of the main software and whenever it arrives, it should:

1. Receives a command from the daemon.
2. Parses the serialized string into tokens and fills a command structure.
3. Identifies the command and executes the corresponding task with the provided arguments.
4. Constructs the response message during task execution.
5. Sends the response message back to the daemon upon task completion.

## Renesas Components

**PORTS**: for triggering the cameras we need to send a trigger signal via GPIO.

The component instatiate is `PORTS`.

The choice of the port depends on which pin we want to set for triggering. Considering triggering all cameras
simultaneous, all cameras are going to be connected in parallel and linked to only one GPIO. As almost all ports are
GPIO, the choice becomes arbitrary.

**SCI - Serial Communication Interface** : for establish communication, send and receive messages through it.

The component instatiate is `SCI/SCIF Asynchronous Mode`.

To configure this component, we just need to make sure that the `bit rate` is set to `9600`, which the default bit rate
considered in the communication protocol establish between the software and the microcontroller.

Once configured, you can right click the `Config_SCI` component in the `Components` list and go to `Change resource`.
This allows you to select which SCI you want to use and this affect which pins are going ot be used. For example, SCI0
uses pins 17 and 18 for RX and TX, respectively while SCI11 uses pins 54 and 53.

After configuring both components, click on `Generate Code` and build the project once.

## Project Structure

The entire code for the project is organized in a single main file called `rtk5rx65n_firmware.c`, complemented by a project configuration header, which defines key project-related information, and a communication protocol header, which defines important protocol symbols.

The decision to use this monolithic architecture was driven by its simplicity and to avoid the build and linking errors that a more modular approach was causing.

## Code

### Macro Definitions

The code begins with macro definitions, which set GPIO states, buffer sizes for string handling, and macro functions to simplify GPIO operations.

It’s important to note that, for this project, the ON state of a GPIO (referred to as "Pin" in Renesas terminology) is represented by 0. This might be confusing if you're not familiar with it.

### Struct Declarations

In this section, key structs are defined, such as the `command` struct, along with some status enums.

The `command` struct is filled by the parser when it receives a message through serial communication and is also used by the command functions to send responses back to the computer.

The command status indicates success or errors during parsing or command execution.

The `ParserState` enum defines the possible states of the parser, as command parsing is based on a finite-state machine (FSM).

### Function Declarations

This section lists all the function declarations, grouped by functionality:
- The first group is related to code execution.
- The second group handles serial communication and the communication protocol.
- The final group contains the command-related functions.

The function definitions follow the same order described here.

### Global Variables

This part defines the global variables, which primarily consist of the buffers used for receiving and sending messages.

### Function Definitions

The `main` function is the entry point of the code and is structured similarly to Arduino's architecture. It includes a `setup` function, where components are initialized (e.g., starting the serial interface and resetting GPIO values). Following that, an infinite loop runs the `loop` function, with a `R_BSP_SoftwareDelay` ensuring that the microcontroller executes this loop periodically. 

It’s worth noting that this approach isn’t optimal, as the microcontroller is blocked during the delay, preventing it from reacting to other events. However, without the delay, some features won't function properly.

> A non-blocking delay could be implemented by checking conditions to determine if it's time to run the `loop` function. This approach is similar to Arduino's [Blink Without Delay example](https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay), which can be adapted for Renesas IDE.

The `loop` function is tailored to the project's needs (see [Project Requirement](#the-project)). In each iteration, it receives a message via serial, creates a `command` struct, fills it with the `parse_command` function, executes the corresponding command with `execute_command`, builds the response, and frees any allocated resources. Finally, it sends the response back through serial communication.

#### Parsing

Parsing is done using an FSM. The parser reads the input and, when it encounters a protocol symbol, changes state and stores the preceding string in the appropriate attribute of the `command` struct.

Initially, the parser starts in the `COMMAND` state, as it looks for the command name. The input buffer is the global variable `receive_buffer`, and `idx` indicates the parser’s current position in the input. The parser processes each character, accumulating them into `str_buffer` to construct the token, with `buf_idx` tracking the token's position in the buffer.

Upon encountering the first special character (`BLOCK_SEPARATOR_CHAR`), the parser transitions to the `ARGUMENT` state and copies the token into the `command` attribute. The buffer is then cleared, and the buffer index is reset. In this state, the parser handles two error cases: if the command is empty, execution stops, and the token size is checked to avoid buffer overflow.

In the `ARGUMENT` state, the parser constructs a token for each `ELEMENT_SEPARATOR_CHAR` it encounters. The arguments are stored in an array of size `MAX_ARG_NUMBER`, and memory is dynamically allocated to store each token string. After allocation, the string is copied, and the buffer and index are reset. Error cases include a full argument list, empty arguments, memory allocation errors, and buffer overflows.

The final argument, which is not followed by an `ELEMENT_SEPARATOR_CHAR`, receives special handling.

After parsing the entire input, the buffer is freed, and the parser completes.

#### Executing a Command

Once parsing is finished, the `command` struct contains the command to execute. The `execute_command` function compares the token in the struct to the expected command string defined in `protocol_symbols.h` and dispatches the appropriate function.

The command function performs the task and sets the response message in the `command` struct, which will be sent back to the software.

#### Serial Communication

This section contains basic communication functions that encapsulate the components’ API. For instance, the `serial_start`, `serial_receive`, and `serial_send` functions wrap the API calls for the SCI component, which was initialized earlier using the Smart Configuration tool. These functions also handle buffer management.

The `build_response` function constructs a response string as required by the communication protocol, inserting the message accordingly.

Currently, debug messages are ignored and left blank, as the debug mode is not yet implemented.

## TO DO

Although the code structure is in place, some functionalities are still missing, including the `trigger_camera` and `set_mode` commands. Additionally, the code has not been thoroughly tested.

- [ ] Implement `trigger_camera` command
- [ ] Implement `set_mode` command
- [ ] Add debug messages
- [ ] Avoid software delay
- [ ] Complete debugger parsing
- [ ] Test the entire system + software interaction