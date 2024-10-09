# camera-virtual

The virtual camera module provides a way to test functionalities that use 
cameras, both for the daemon and client software. 

Virtual cameras are instantiated with black images of a given size or from 
given image files. The virtual backend is able to simulate effects of 
the exposure time on the image, as well as supporting the software trigger.

This module also expose HTTP endpoints for the clients to interactively 
add and remove virtual cameras.