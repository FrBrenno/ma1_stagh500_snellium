# microcontroller-virtual

Just as the `camera-virtual` module, the `microcontroller-virtual` module provides a way to test functionalities that
use microcontrollers, both for the daemon and client software.

Virtual Microcontrollers are instantiated with default values for the pins connections. The virtual communication is
able to simulate a proper communication, without errors, with the microcontroller and the client software. All the
responses generated are correct accordingly to the communication protocol, although the values are not real.

Virtual microcontrollers can be added and removed using the HTTP endpoints provided by the module.

## Program Options

When the program is built using this module, it is possible to run it with the following options:

- `snelliumd` : no option is set, the program will start with no virtual microcontrollers.
- `snelliumd --virtual-microcontroller` : the program will start with a virtual microcontroller with default values.
- `snelliumd --virtual-microcontroller ./gpio-settings.json` : the program will start with a virtual microcontroller
  with
  the values set in the file `gpio-settings.json`.

