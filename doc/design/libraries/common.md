# libraries: common

The common library contains basic functionalities such as logging, 
configuration, etc.

## Logging

Different logger classes exists: 

- `Logger` that implements the logging features themselves, with colored headers 
  in front of each message that describe the type of message.
- `SharedLogger` that extends `Logger` with a thread-safe layer making it usable 
  from different threads at the same time. This class should be used instead
  of `Logger` almost everywhere, since the daemon is heavily multi-threaded.
- `PreFilledSharedLogger` is an interface over `SharedLogger` with logging 
  details (colour, source, etc) already set, this is useful to obtain a 
  consistent logging scheme across modules.

## Configuration

The `Configuration` class is an abstract parent to other configuration classes 
through the project, making them compatible with the arguments parsing library
provided by Boost.

