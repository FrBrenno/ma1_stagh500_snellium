# pipelines

The pipelines module is responsible for algorithms execution. This module
is based on top of the `jobs` module from the `core-library`.

Each algorithmic task has to be defined as a derived class from `Pipeline`.
Each pipeline is retained by the `PipelineManager`, that gives an unique
id to each of them and handle the execution context of jobs.

## Pipeline definition

Each pipeline creates as set of jobs to be executed to complete the given
task they were implemented for. When the pipeline starts, each of those jobs
are sent to the parent class `Pipeline` that will executes them. It waits for
the completion of those jobs to keep track of the advancement of the task.

In addition, the `Pipeline` class provides an universal interface for
querying serialized versions of the input or output data.

## Userdata

Pipeline often needs to run on multiple input data, requires jobs to be
configured with parameters, etc. Having the client send everything through a 
single HTTP request would be tedious.

Instead the pipelines module is built to make the client send first the
input data one by one, then launch the pipeline. These pre-uploaded data are
called _userdata_ and are stored inside the `UserDataManager`, that 
automatically assign an unique id to each of them. This manager handles
the removal of stale data, to avoid unused data to pile up in the memory.

