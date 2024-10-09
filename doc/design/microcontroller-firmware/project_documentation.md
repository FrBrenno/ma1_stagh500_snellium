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

## Main Code

<!-- I need to finish the code before writing about the project because I am still not sure of the right architecture -->