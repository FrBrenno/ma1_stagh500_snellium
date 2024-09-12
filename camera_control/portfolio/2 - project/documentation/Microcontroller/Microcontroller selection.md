>Cf. Component_for_camera_control_unit.ods
>This document contains the list of found microcontroller boards that were considered for the project and they are order by more suitable to less suitable.

>Cf. Order_of_components_2207.ods
>This document contains the list of components chosen to buy.

I was tasked with finding a _reliable, industry-oriented, powerful, and available_ microcontroller board for the control unit. One of the key requirements was that the chosen microcontroller should support potential future features beyond the current project needs. This was somewhat challenging, as my project itself doesn’t require significant processing power. The main task of the microcontroller is to interpret messages sent by the software and execute simple commands like triggering cameras, which only requires a single GPIO pin since all cameras will trigger simultaneously.

At first, I considered simpler solutions like the Arduino Uno or ESP32, which would have been more than sufficient for the current needs. However, given the request for future-proofing the system, I had to explore more powerful alternatives. After several discussions with Abbas, the electrical-mechanical lead, who emphasized the need for scalability, I defined a set of criteria to guide my selection process.

Through my research into the current state-of-the-art microcontroller platforms, I identified several key aspects that should be considered for this project:

### Key Criteria for Microcontroller Selection


![[img/Pasted image 20240912150431.png]]

1. **Manufacturer**:
    - I had no specific constraint regarding the manufacturer at the outset. However, I came across several manufacturers commonly used in industrial applications, such as STMicroelectronics, Texas Instruments, Infineon Technologies, and Raspberry Pi. 
2. **Processor**:
    - Since future features might require higher computational power, I opted for a microcontroller based on the *ARM Cortex architecture*, known for its performance and flexibility. ARM-based microcontrollers are widely used and offer excellent scalability for industrial applications.
3. **Clock Frequency**:
    - My supervisor requested a higher-than-average clock frequency to ensure the system can handle future demands. This meant selecting a microcontroller with a *high-performance clock* to manage potentially complex tasks efficiently.
4. **Port Number**:
    - For my project, only one GPIO pin is necessary. However, anticipating future features such as motor control for each individual camera (with six cameras, three motors per camera, and multiple signals per motor), we estimated a need for *40+ I/O ports*.
5. **PWM Pins**:
    - I included this criterion to support potential future use of *servo motors*, which require pulse-width modulation (PWM) for precise control. This could be relevant for later system iterations that involve motorized camera positioning.
6. **Communication Interface**:
    - The microcontroller should primarily communicate via *USB*, but it’s important to also support other communication protocols such as *Ethernet* to allow for greater flexibility and to overcome USB length limitations.

### Additional Considerations

![[img/Pasted image 20240912150454.png]]

- **I/O Reliability**:
    - The board should come with a *reliability guarantee* of at least 5–10 years to ensure it can withstand long-term industrial use.
- **Industrial Application**:
    - The microcontroller should be designed for *industrial applications*, with a focus on durability and robust performance. I reviewed documentation and product reviews to ensure this criterion was met.
- **Compatibility with RTOS**:
    - Although not needed for the current phase of the project,*Real-Time Operating System (RTOS)* compatibility could be useful in the future for managing more complex, multitasking operations.
- **Alternative Availability**:
    - The chosen model should have an easily replaceable alternative in case of supply issues or design changes. Having a fallback option helps mitigate risks.
- **Cost Efficiency**:
    - While performance and scalability are important, keeping the *price reasonable* is crucial. There is no need to select a premium component when a more cost-effective solution suffices for the project.
- **Availability/Lead Time**:
    - The *availability* of the board is also a concern. Long lead times could hinder the project, but this could be offset by finding products that are widely stocked.
- **Ease of Implementation**:
    - Lastly, the microcontroller should be *easy to integrate* into the system. Unfortunately, this was a factor I initially neglected, but it is crucial to ensure a smooth development and deployment process.



# Top 3 Microcontrollers Boards

### Renesas RX65N review

![[img/Pasted image 20240912152354.png]]
**_Pros_**  
- **Excellent construction quality.**
- **Firmware and Support**
	- Dual-bank flash memory allows seamless firmware updates and rollback.
	- Comprehensive e-Learning modules for the RX family of MCUs.
	- Active support forum with generally quick response times.
- **Development Tools**
	- e2Studio IDE based on widely-used Eclipse CDT, offering flexibility and plugin support.
	- Choice between CCRX (60-day free trial) and GCC (free) compilers.
	- Helpful utilities and sample programs aid development.
- **Smart Configurator**
	- Simplifies the configuration of FIT modules, ports, and pins.
	- Intuitive interface that accelerates development.
	- Significantly reduces the amount of handwritten code needed.
- **Value for Money**
	- Priced under 50€, offering a cost-effective solution for HMI development.
	- Comprehensive set of features, including the MCU, LCD, debugger, and emWin software.
- **Filled most of the criteria defined**

**_Cons_**  
- **User Fit Parts Issues**
	- Some parts are obsolete or difficult to source, causing potential roadblocks.
- **Segger emWin Software**
	- Initial setup is tricky due to limited documentation and outdated samples.
	- Requires adapting samples from other sources to work correctly.
- **USB/Serial Interface Challenges**
	- USB UART cannot be used for serial communication and debugging simultaneously.
	- Bug in the Serial Communications Interface FIT module remains unresolved.
- **Documentation is extensive and can be overwhelming (over 2700 pages).**
- **Board Design and Mounting**
	- No mounting points, making it difficult to encase the board.
	- Ports and headers positioned on the edge, limiting mounting options.

### STM32 Nucleo and Tiva LaunchPad

![[img/Pasted image 20240912152339.png]]

This was my first top 2 solutions. STM32 seemed a really good candidate with its high-performance capabilities, high number of ports, high clock frequency, USB communication and realibilty. Also, an important factor was compatibility with Arduino IDE meaning that I could exploit already existing Arduino libraries which could improve development quality and pace.

However, for both of these components the lead time was too high. STM32 have a 51 weeks leading time while Tiva Launchpad have a 12 weeks. Snellium could not take the risk of waiting this long in order to implement the control module in case scenario where there is no in-stock component. This is why i did new research and where I found Renesas RX65N with a lead time of 4 weeks.

# Personal Reflection about Microcontroller Board

I did a mistake. I chose a microcontroller that is extremely powerful and professional but which has a extremely steep learning curve. Indeed, the provided IDE is not clear and the documentation is overwhelming. Testing this board when it arrived was a nightmare. The most simple program of making some LEDs blink took me two whole days. All of this because their environment is too complicated and you have to know what you are doing. With my poor experience, I was not able to do anything without help of the Renesas Engineering Community Forum, which is fast and provide great help. I believe that the difficulty comes from the fact that the board is far too powerful. 

If I could redo my choice, I would stick with STM32 Nucleo which seems to have a more user-friendly environment and it is compatible with Arduino IDE, with which I am used to. I could have same me some many time and stress. The decisive element that made us choose the other one, leading time, is a factor that is strongly damped by the stock availability. Indeed, the leading time was long, 51 weeks, almost one year but there are more the 5000 exemplars distributed over Europe ready to deliver. Also, compatibility with Arduino Environment would allow to abstract the board from the code and would allow eventually to replace the board with any other Arduino compatible device. With Renesas board, I am stuck to their environment and once they decide to move to another board, the microcontroller firmware would need a refactoring or worst, a complete re-implementation.

I wish I could stick with simple products too like Arduino or a more elegant one as ESP32. I think that planning too ahead could be a problem too. The future-proof margin should be enough to allow stability for two to three years. When the device starts to become overwhelmed, the whole sytem needs to pass to an update, refactoring code to improve performance and eventually upgrade the microcontroller board for a more powerful one. It is better to take several little steps than to overestimate our needs and be confronted to complex solution when it is not yet needed.
