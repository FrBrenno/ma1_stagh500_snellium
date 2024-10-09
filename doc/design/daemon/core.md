# core

The `core` module defines the top-level structure of the Daemon.

## Architecture

The `ExecutionContext` class stores all "elements" currently available:
cameras, microcontrollers, pipelines, userdata, etc. It also gives access to the user supplied
configuration.

The top-level `Daemon` class stores the execution context and all the different
systems around it:

- Thread to listening to incoming device connection
- The thread that cleans staled data or disconnected devices
- The module manager
- etc.

## Modules

The Daemon works with a system of modules, that can be added or removed during
the execution. The typical case is the licencing: if the license expire,
modules are removed, when the user supply a new valid licence,
modules are added back.

The `ModuleManager` class handles the list of modules.
Each module contains a list of `RequestHandler`s and/or cameras `Discoverer`s,
that are added or removed from the HTTP Server or `DeviceDiscoveringThread`
when a module is loaded or unloaded. The `ModuleManager` is also responsible
for the licence check.

## Devices

The device module serves as the interface between any device-related module and
the core module. Any device that needs to interact with the daemon must implement
the interfaces and abstract classes of the device module. This ensures that
the new module will include all the necessary methods required by the core module,
while also defining a discoverer responsible for retrieving and establishing device
connections, as well as the required container classes.

The device module also defines the `DeviceDiscoveringThread`, which is continuously polling for
new device connections. When a connection becomes available, it creates the necessary
object for the device to be used within the daemon.

## Cameras

The cameras are created from the `DeviceDiscoveringThread`, that used the list
of `camera_discoverers` supplied by the currently active modules in `CameraDiscovererSet`.
Newly connected cameras are added to the `CameraSet`, which allow access
from clients through HTTP requests.

## Microcontroller

Working in a similar way as cameras, microcontrollers are created by the same
`DeviceDiscoveringThread`, which used the list of `microcontroller_discoverers` supplied by the
active modules in `MicrocontrollerDiscovererSet`. The new microcontrollers are added to the
`MicrocontrollerSet`, which allow access from clients through HTTP request.

## Pipelines

The execution context holds the `PipelineManager`. Pipelines are created by
modules, most often at the request of the client from the endpoints defined i
said module.
