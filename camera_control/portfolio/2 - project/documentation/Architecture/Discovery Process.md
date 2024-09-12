 
![[portfolio/2 - project/documentation/Architecture/doc/microcontroller_module_sequence_diagram_discovery.png| Discovery Sequence Diagram]]

This discovery process is simple. 

Each communication interface is responsible for maintaining a list of connected devices. When the **discovering thread** requests it, the **discoverer** will scan this list and attempt to establish a connection with each device. Upon a successful connection, the discoverer issues a **ping command** to the device. If the response is incorrect or no response is received, the device is considered not to be a microcontroller and is subsequently discarded.

This approach is reliable due to the strict nature of the communication protocol. By adhering to the protocol, only a valid microcontroller can respond correctly to the ping command. If the discoverer receives the correct response, it confirms that the device is indeed a microcontroller. The discoverer will then return a **communication object** related to the detected device, which contains all necessary information for further interaction.

Once the discoverer completes the scan of the entire device list, it notifies the thread that new devices have been detected. The thread then extracts the relevant communication objects and instructs the discoverer to associate them with new **microcontroller objects**. These microcontroller objects are subsequently placed into the **microcontroller_set**, where they can be retrieved and utilized by the handler.