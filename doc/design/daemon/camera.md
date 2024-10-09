# camera

The daemon includes features to detect, connect, and acquire images through
cameras. These cameras are produced by different manufacturers, use different
communication protocol, etc.
The module `camera` serves as an abstraction layer on top of the different 
camera libraries, to expose a single interface. 

## Architecture

The `Camera` class is the front-end for caller code. 
Each `Camera` hold a reference to a `Backend` instance, which is a inherited 
abstract class implementing all basic access to the hardware 
(connection, acquisition, settings). 
A new derived class from `Backend` is created for each manufacturer, while the 
`Camera` class is universal.

The `Discoverer` is a factory for cameras, it listens to incoming connections
and create the corresponding new `Camera` and `Backend` instances. 
This class must also be inherited for each manufacturer.

## Using cameras

The `Camera` class exposes an interface to query and set the settings of the 
camera, start and stop the image acquisition, and grab the obtained frames.

For ease of use, the module also defines a set of *operations*, that are classes
made to execute a specific sequence of operations. For example, the
`ContinuousImageAcquisition` operation opens the camera, starts the acquisition,
fetches all incoming images, and when asked stops the acquisition.
Operation instances start their own thread, since operations on cameras 
are often blocking.
