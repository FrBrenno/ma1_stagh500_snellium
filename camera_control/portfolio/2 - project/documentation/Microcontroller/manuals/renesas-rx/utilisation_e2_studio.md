# Utilisation of e² studio - Renesas IDE

## Prensetation of the IDE

When opening e² studio, it will always ask which work directory you wish to work on. Just enter the name or browse it
through you files to find the project you want to start.

## Creating a Project

In order to create a new project, you should go into `File > New > C/C++ Project`.

> Pay attention to not create a project with the `Renesas C/C++ Project` because this project will be configured to use
> the CC-RX compiler which is the licensed paid Renesas compiler. We want to use `GCC for Renesas RX` which is the
> compiler package completely free and open-source.

A new box will be open asking you to select the project template you wish. Here, you should choose
`GCC for Renesas RX C/C++ Executable Project`. This will ensure that the project is configured to use GCC compiler.

![Templates for new Projects](./img/creating_project_templates.png)

After that you can give a name to your project and click on next.

The next step is to configure toolchain, device & debug settings. Make to set the right configuration:

- **Language** : C or C++ - preferably C++;
- **Toolchain**: GCC for Renesas RX;
- **Target Board** : `TargetBoardRX65N`;
    - using the wrong board would cause errors at compiling, debugging and execution - since the pins numbers are
      different.
- **Create Hardware Debug Configuration**: make sure it is checked and the debugger to be `E2 Lite (RX)`;

![Project Configuration](/img/creating_project_configuration.png)

On the next step, check `Use Smart Configurator` and on `Finish`.

## Developping a Project

When the project is created, this windows will be open:

![New Project Home Screen](img/new_project_start.png)

At the top left, just below menu bar - `File Edit Navigate ...` - we can see the icons menus that are the most important
in the development:

![Menu Icon Bar](img/menu_icon_bar.png)

- The floppy disk is for saving the file;
- The potentiometer is for managing configurations of the project;
- The hammer is for building the project;
- The bug is for running the debugger;
- The play symbol with the toolcase is for running previous tools, not that used;

> ***Important Note***: Always build the project before running the debugger. The project will not be rebuild even if
> you made changes to the code just for clicking in debug.

On the left side, we can see the `Project Explorer` which presents the project structure and directories.

![Project Explorer](./img/project_explorer.png)

The most important files here are the **main** .c file, that in our example is called `test.c`, and the `test.scfg`
which is the **smart configurator** file.

### e² studio Views

### Smart Configurator

Renesas IDE's Smart Configurator provides a GUI for configuring your board with less code. Indeed, you do not really
need to code each file for each new component you add. You can use the the Smart Configurator to instantiate the
component, configure it and set it up. Once component setup, you need to rebuild the project and the related files will
be **automatically generated** by the Smart Configurator.

Each new component add will provide a interface for using this component inside you main file.

![Smart Configurator Overview Tab](img/smart_configurator_overview.png)

Smart Configurator has several tabs:

- **Overview**: Home page at the Smart Configurator and shows current configuration.
- **Board**: Used to select the device used in the board, but this was already configured in the creation of the
  project. Not very used.
- **Clock**:  allows to change clock configuration. Not used.
- **System**: allows to set debug interface setting. Make sure it is set to `FINE`.
- **Componets**: allows to instatiate components in the project and manage it. Most important one.
- **Pins**: allows to manage and see pins configuration and pins numbers.
- **Interrupts**: allows to manage interruption.

Board, Clock, System tabs have configuration that were set once and should not be changed, so they are not useful for
development. On the other side, tabs Components, Pins and Interrupts are more important specially Components since every
configuration done here, affect and automatically configure the component in the other tabs.

#### Instantiating a component

Open the Smart Configurator file, normally its name has the extension `.scfg`.

On the bottom the GUI, one can find different tabs that are used in the Smart Configurator. The different tabs is
related to different ways to configure your board and the project. Look for `Components` tab.

![Smart Configurator Components Tab](img/smart_configurator_components.png)

Here, one can see all the components set but it can also add or remove components.

The component `r_bsp` is the package that provides a foundation for code to be built on top of. It provides startup
code, iodefines, and MCU information for different boards. For futher explanations about it, read the
`src/smc_gen/r_bsp/readme.txt` file.

Check [Bliking LED Sample Project](#led-blinking) to see how LEDs, more specifically ports are instantiated
and [Echo Serial Communication](#echo-serial-communication) for Serial Communication components.

Once you finished configuring and setting up all the components, you can click on `Generate Code` on the top right of
the GUI. After that, all the files will be generated and you can use the interface in order to interact with this
components.

##### Modifying component files

For more custom and specific configuration, you can by yourself modify the files of a certain component. However, you
need to find the right file and you can add your code in the place that the Smart Configurator let for `USER CODE`.
Those spaces look like this:

```C
/* Start user code for include. Do not edit comment generated here */

/* End user code. Do not edit comment generated here */
```

The code that lays between those comments are not going to be erased if you regenerate configuration files.

Also, there is also some user configuration files, that normally ends by `*_user.c`, where it is possible to implement
custom `Init()` functions and other base functions, but these are really dependent on the component.

For straight-forward and simple development, there is no need to change configuration files manually.

#### Pins Tab

The next important tab is the `Pins` tab of the Smart Configurator.

![Smart Configurator Pins Tab](img/smart_configurator_pins.png)

In this tab, one can see all the `hardware resources` on the left side of the panel, the enable `pins` and its function
on the middle and to the left, a representation of the chip and the ports being used and names in the `MCU/MPU Package`.

When selecting a pin, the `MCU/MPU Package` will display the selected pin in red. If the pin is enabled, its color
changes from grey to green.

During development, the components are going to be first configured and setup on the `Components`. Then, you have to
look for pin information in order to make the right connections to the board. However, the first view of `Pins` tab is
not very helpful because it presents every harware resource available. In order to filter it out to only the components
the project has instatiated, we can click at the hierarchy icon just in front of the `Hardware Resource` label. The list
will be reduced and it is possible to see which component is associated to which pin and its pin number.

##### Locating a Pin by its pin number

![RTK5RX65N Board](img/rtk5rx65n_pins.png)

The pins are numbered from the bottom of the board in a zig-zag way where the odd numbers are in the interior of the
board and the even numbers at the exterior. Some dots along the way indicates 10th of pins. There is 50 pins at each
side of the board.

## Debugging a Project

The RTK5RX65N board comes with a built-in E2 Lite debugger. This allows us to run the code on the board and meanwhile,
stop at breaking points, seeing the code execution step-by-step, check memory content and more. To launch debugging, you
just need to click on the bug icon in the menu icon bar.

![E2 Lite Debugger in the RTK5RX65N board](/img/rtk5rx65n_debugger.png)

Once debugging, the software is going to ask for a change of view into `Debug View` and the user should use the menu
debug icons to move forward in the debugging.

![Debug Menu Icons](img/debug_menu_icon.png)

Most of time, you are only use the first button, `Resume`, to move forward in the debugging and the third one,
`Terminate`, to stop debugging. Other relevant buttons to know about are the `Step Into`, which going deeper into
function calls, and `Step Over`, which overpass some functions.

It is possible to set breakpoints to stop the execution in certains parts or method for a more careful inspection of
code execution just like no matter other IDE.

> Note: In order to use the debugger, you need to install the E2 Lite Driver.
> Check [Installation e² studio - E2 Lite Driver](./installation_e2_studio.md#e2-lite-driver-installation) for this.

## Programming RX65N

When working with e² studio, it is possible to run your program in debug mode thanks to the E2 Lite Emulator. However, the microcontroller is not necessarily flash programmed. Indeed, if only by powering up the board will not make the program run, you should run the program in debug mode.

In order to once-for-all program the flash of the microcontroller, you need to use the Renesas Flash Programmer Software. This software uses the E2 Lite as a programmer and put your code inside the microcontroller's memory via USB.

> Cf. [Renesas Flash Programmer Software webpage](www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui)

The documentation provided by Renesas about this software is pretty extensive and easy to read. It present all the main functionalities available, as well as troubleshooting. 

> Cf. [Renesas Flash Programmer Software Manual](https://www.renesas.com/en/document/mat/renesas-flash-programmer-v316-flash-memory-programming-software-users-manual?r=488871)

## References

### Renesas Engineering Community

- [Renesas Engineering Community webpage](https://community.renesas.com/)

The Renesas engineering community is highly responsive and supportive. When solutions are hard to find online, posting a
question on the forum usually yields a detailed, well-referenced answer within a day. It's an invaluable resource when
you're unsure where to find a solution.

#### Asked Questions on the forum

- [e² studio installation problems with swt java library](https://community.renesas.com/tools/e2studio/f/e2studio-forum/33003/e2-studio-installation-error-linux-swt-os-java-error-failed-to-load-swt-pi3-loading-swt-pi4-as-fallback)
- [Newbie at Programming RX65N target board](https://community.renesas.com/mcu-mpu/rx/f/rx-forum/39047/newbie-at-programming-rx65n-target-board)
- [Serial Communication via USB - RTK5RX65N](https://community.renesas.com/mcu-mpu/rx/f/rx-forum/39184/serial-communication-via-usb---rtk5rx65n)

### Blinking LED Sample Program

- [LEC Blink Control Program - Sample Code](https://www.renesas.com/en/products/microcontrollers-microprocessors/rx-32-bit-performance-efficiency-mcus/rtk5rx65n0c00000br-target-board-rx65n#design_development)
- [Documentation for RX65N LED Blink Control Program](https://www.renesas.com/en/document/apn/rx65n-group-target-board-rx65n-led-blink-control-program)

This is the sample code provided by Renesas in order to test the board. Although it uses the CC-RX compiler and it is
not up-to-date, you can still create a new project using GCC that has the readapt same code. However, you will have to
use the Smart Configurator by yourself, which could be a really good hands-on exercise.

### Tutorials

- [RX Family Software & Tool Course](https://www.renesas.com/en/rx-family-software-tool-course)
- [RX 32-Bit Performance/Efficiency MCUs - Videos & Training](https://www.renesas.com/en/products/microcontrollers-microprocessors/rx-32-bit-performance-efficiency-mcus#videos_training)
  