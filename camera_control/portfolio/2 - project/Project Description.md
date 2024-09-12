# Project Description

## Introduction

The current setup for one of Snellium's technology implementations consists of a computer running the software, four cameras, and a speckle projector.

The cameras are configured to acquire images through hardware triggering, which involves sending a signal to their trigger inputs. Currently, this is done by connecting all the trigger inputs to a shared bus linked to a 5V USB power source and a manual button. When image acquisition is needed, the software is activated to wait for the image data, and a technician presses the button. This action closes the circuit, allowing the 5V signal to reach the trigger inputs, activating the cameras.

While this setup functions well, it is manual and may not be suitable for industrial applications where automation is preferred. To meet industry demands, Snellium aims to eliminate the need for physical intervention.

## Project Statement

> **GOAL:** Design and implement a control module powered by a microcontroller capable of communicating with the software for automatic image acquisition.

- **Plug-and-Play:** The software should automatically detect and connect to the control module for seamless installation.
- **Extendable:** The project currently focuses on camera triggering, but the module should be designed to support future features, such as motor control.
- **Industry-Oriented:** The system must be robust, professional, and suitable for industrial applications.
- **Reliable:** The system should function correctly and consistently over long periods.
- **Easily Manufactured:** The system should avoid complex processes like soldering or PCB design and be simple to produce and install.
- **User-Friendly:** The system should be easy to use, without requiring specialised technical knowledge.

**Deliverables:**
- Software module to interface with the control unit
- Control unit with components and circuit diagrams
- Microcontroller firmware to receive and execute commands

## Project Strategy

My strategy for this project involves dividing it into distinct phases:

1. **Research on State-of-the-Art:**
    - Investigate existing systems that perform similar functions
    - Identify common hardware components and software designs
2. **Microcontroller Firmware Development:**
    - Microcontroller and components choice
    - Set up the microcontroller for use
    - Develop a command parser
    - Implement each command
3. **Communication Protocol Definition:**
    - Define the communication method between the software and control unit
    - Specify available commands and how they will be serialised
3. **Python Prototype of the Software:**
    - Develop a prototype in Python to test the system and explore the challenges
    - Refine the software architecture for efficiency
4. **Implementation into Snellium's Codebase:**
    - Study the existing codebase and integrate the prototype's architecture
    - Implement the microcontroller module to enable software-control unit interfacing
5. **Install Physical Setup:**
    - Design circuits for camera triggers
    - Establish all physical connections to ensure the system functions as intended

Each step is accompanied by testing and thorough documentation to ensure the project progresses smoothly and meets all technical and functional requirements.