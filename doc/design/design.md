# Daemon

The daemon is a program that is meant to be run in background, providing a 
universal interface to clients. It exposes hardware and algorithmic related 
features, from machine control to measurement computation.

The interface is build as a REST API, using HTTP and JSON. 
This has the following advantages:

- Compatible with most languages and tools, including web technologies.
- Accessible from remote computers using the exact same interface. This is
  particularly useful for building system with multiple computers, 
  or for debugging.

The daemon source code is separated in three folders: `libraries`, `daemon`, 
and `modules`. 

- The `libraries` folder contains the source code of basic building blocks 
  that are used in different parts of the project. 
- The `daemon` folder contains the main architecture and control classes. 
- The `modules` folder contains all modular functionalities, each subfolder in 
  `modules/` can be enabled or disabled from build using CMake options.

[[_TOC_]]

## Libraries

- [common](libraries/common.md)
- [http](libraries/http.md)
- [serialization](libraries/serialization.md)
- [privileged](libraries/privileged.md)
- [hardware-queries](libraries/hardware-queries.md)
- [licence](libraries/licence.md)

## Daemon

- [camera](daemon/camera.md)
- [pipelines](daemon/pipelines.md)
- [core](daemon/core.md)
- [licence-generator](daemon/licence-generator.md)

## Modules

- [camera-virtual](modules/camera-virtual.md)

## Targets

Targets are final executables to be created from the project. 
This includes the daemon itself, that will be distributed, 
and a licence forging executable for internal use.

## Packaging 

The Packaging folder contains scripts to generate packages out of the project. 
As for the build, it is recommended to run these scripts from a different folder 
than the source tree.

Executables needs to embed the public key for licence managing, so the 
packaging tools ask for this file to be provided.


