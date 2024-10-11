# device-module

The module `device` serves as an abstraction layer on top of the different device abstraction layers, to standardize the
device-related modules. This approach ensures that the new module includes all necessary methods required by the core
module, while also defining a discoverer that is responsible for retrieving and establishing device connections, as well
as managing the required container classes.

# Structure of Device-Related Modules

Each device-related module must include the following components:

- Device Class: This class implements the device_interface, such as Camera or Microcontroller.
    - The Device class serves as the front-end for the request handler, facilitating interaction with a specific device.

- DeviceHandler Class: This class implements the device_handler_interface, such as Backend or Communication.
    - It forms the core of the device functionality and interacts directly with the device API, handling all low-level
      operations and communication with the hardware.

- DeviceDiscoverer Class: This class implements the device_discoverer_interface, such as camera::Discoverer or
  microcontroller::Discoverer.
    - The device_discoverer class already implements the discoverer_interface and sets up all necessary methods for
      discoverer operations.
    - This class is crucial for detecting devices, generating the corresponding DeviceHandler, and configuring it for
      use with the Device class.

# DeviceDiscoveringThread

The device module also defines the DeviceDiscoveringThread, which continuously polls for new device connections. When a
connection becomes available, it instantiates the necessary objects to integrate the device within the daemon. This
ensures that all newly detected devices can be efficiently utilized without manual intervention, enhancing the overall
responsiveness of the system.

# DeviceDiscoverer

Discoverer for all kind of devices will behave essentially the same way. Consequently, `discoverer_interface` is
already implemented inside the device module inside the `DeviceDiscoverer` class. The latter is still abstract because
it let to each module to define device-specific methods since each device has its own method of connection.

# Device Module Container

## Device Set

The type of the `DeviceSet` class should be defined somewhere in the namespace of the new device module. The suggestion
now is to typedef it just after the declaration of the `Device` class. This class is type-safe.

#### Type-safety of DeviceSet

The type-safety is acquired by when taking ownership of an `DeviceInterface` object, it first verifies if it can be
cast as the type of `<Device>`, which defines the DeviceSet. If it can, the `DeviceInterface` object is added to the
container. On the other side, if it fails, the DeviceSet refuses the ownership.

Further, the find methods of these sets will return pointers to the concrete object defined by `<Device>`.

## Discoverer Set

The discoverer set is designed to be completely abstract, as all discoverers share a high degree of similarity and do
not have specific methods unique to individual device types. This abstraction allows a CameraDiscovererSet to be treated
the same way as a MicrocontrollerDiscovererSet.

Each discoverer set includes a reference to the associated DeviceSet, which effectively defines the type of devices
managed by that discoverer. This relationship is essential, as it enables discoverer sets to apply the same operations
and methods uniformly across their respective device sets.

