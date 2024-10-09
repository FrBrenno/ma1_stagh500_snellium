# libraries: hardware-queries

This library is used to fetch various information about the computer hardware. 
It is built on top of the privileged module for access to restricted 
information (as serial numbers, for instance).

Each queried component (`Baseboard`, `Product`, `NetworkController`, `GPU`, etc) 
is implemented as a struct for information storage and an abstract `xxxQuery` 
class to fetch the information. 
The abstract mechanism allows subclassing for different platforms and OSes, 
as well as making mock-ups for tests.

The `Fingerprint` class is a construction on top of the other component classes,
aiming to generate an unique identifier for a computer, used for licencing. 