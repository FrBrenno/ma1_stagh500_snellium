# libraries: privileged

The privileged library implement operations that requires additional user rights
or accesses. 

For security reasons, it is better to run a program with the least access rights
as possible, to avoid that any bug or malicious attack damages the system. 
The privileged library concentrates the code required elevated privileges, 
allowing the rest of the software to implement only user code.

Since the user rights and access systems depend on the platform, this library
provide as consequence different implementation for each supported platform.

## Interface

This library provide a platform-independent interface, consisting of a 
singleton `Context` instance that can execute *operations*. Each operation
is identified by an enumeration, can take a buffer of bytes as input and
produce a buffer of bytes as output.

The static method `Context::get()` will give access to the context, and 
should be called as soon as possible after the main process start, to remove
eventual privileges as soon as possible from the main process.

In the `operations.hpp` file, top level functions to access the privileged 
operations from the parent process are implemented, providing easy-to-use 
wrappers for the operation mechanism described above.

## Linux

On Linux, the solution chosen is to make the program starts with 
privileged access (using `setuid` bit), then spawn a child process that will
inherits the privileged accesses, and then downgrade the access rights of 
the parent process. 
We then obtain a situation where most of the code runs in the parent process 
with normal user rights, and only the required code runs in the child process 
with privileged rights. Communication between processes is handled using pipes.

The `ForkProcess` class is handling the creation and communication with 
the child process, the operations themselves are implemented in 
`operations.hpp` and user access management in `user_id.hpp`.