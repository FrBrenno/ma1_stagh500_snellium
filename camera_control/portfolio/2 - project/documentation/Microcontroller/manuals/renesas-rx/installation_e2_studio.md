# Installation of e² studio - Renesas IDE

## Introduction

The microcontroller we use is the *RX65N*, which means it is from the *RX Family* brand line of Renesas. The software
tool to develop for this microcontroller is **e² studio**, a proprietary Eclipse-based IDE.

## Installation

First, you need to download the software on the Renesas official
webpage : [Renesas e² studio](https://www.renesas.com/en/software-tool/e-studio).

You need to have a Renesas account and to login before download the software. The software is available for all main
platforms: Linux, Windows and macOS.

### Linux - Ubuntu 24.04.1 LTS

Further in the e² studio webpage, we can find a documentation section containing start guides and other documents about
the software. The guides are pretty comprehensive and dense showing a lot of aspects about the installation and
utilisation of the software. References are located in the end of this document.

Once downloading the installer, it is time to install the required libraries. The libraries are:

- Python library version 2.7
- Python library version 3.10
  (when executing the e² studio 2023-07 or a later version under Ubuntu LTS 20.24)
- New curses library version 5

Install the libraries by entering this command on the terminal:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install libpython2.7 libncurses5 libncurses5:i386
sudo apt install libpython3.10
```

After the installation of the libraries, run the e² studio installer.

### Installer not allowed to run

If the installer does not run immediately, ensure that the installer file has permission to be executed. If not, enter:

`chmod u+x <e²_studio_installer_path>`.

### Installer crashing

Another problem that could happen is the installer crashing when trying to open it. The **recommendation** is trying *
*run the installer through the bash terminal** because it will display to you the execution error traceback.

One of the errors encoutered was :

```
java.lang.UnsatisfiedLinkError: Could not load SWT library. Reasons: 
no swt-gtk-3740 in java.library.path
no swt-gtk in java.library.path
Can't load library: /home/tom/.swt/lib/linux/x86_64/libswt-gtk-3740.so
Can't load library: /home/tom/.swt/lib/linux/x86_64/libswt-gtk.so
``` 

Here the swt library was not found although it was installed. In order to solve this problem, first we need to ensure
that the libraries are really installed and updated. Then, we should copy the files to the path where the installer is
looking for it. Finally, we need to rename a file because the installer was always looking for the wrong one. Here are
the commands lines used:

```bash
# Installing libraries
sudo apt install libswt-gtk-4-java libswt-gtk-4-jni
# Copying swt library to right path
cp /usr/lib/jni/* ~/.swt/lib/linux/x86_64/
# Renaming the file pi3 mentioned in the log file to pi4
mv ~/.swt/lib/linux/x86_64/libswt-pi3-gtk-4963r5.so ~/.swt/lib/linux/x86_64/libswt-pi4-gtk-4963r5.so
```

After this, another error happened and it was a missing library that the error traceback pointed out. Easy solved by
apt-installing it: `sudo apt install libpcre3`.

Here are the sources that helped solve this problem:

- https://stackoverflow.com/questions/10165693/eclipse-cannot-load-swt-libraries
- https://stackoverflow.com/questions/10970754/cant-open-eclipse-in-ubuntu-12-04-java-lang-unsatisfiedlinkerror-could-not-l
- https://stackoverflow.com/questions/76956123/could-not-load-swt-library-error-no-swt-pi4-in-in-java-library-path
- https://community.renesas.com/tools/e2studio/f/e2studio-forum/33003/e2-studio-installation-error-linux-swt-os-java-error-failed-to-load-swt-pi3-loading-swt-pi4-as-fallback

### Running the installer

When running the installer, pay attention to setup the right set of configurations:

1. **Installation Type**:  Go to a `Lite Install` for a simpler and reduced installation of the software;
2. **Welcome Section**: Click on `Next >`.
3. **Device Families**: Select `RX`. All the others can be disabled;
4. **Extra Feature**: Select any extra features you wish, but this are not compulsory.
5. **Components** : All the required components will be automatically selected by the choice of device family.
6. **Addition Software**: enable only the `GCC Toolchain && Utilities`. All the others softwares can be disabled.
7. **Licenses**: Agree with the license agreement.
8. **Shortcuts**: Select to add an application launcher.
9. **Summary & Install**: Click on `Install`.
10. **Results**: Click on `OK`.

Open the terminal and run:

```bash
cd ̣~/renesas/e2_studio/eclipse
./e2studio
```

And the software should run successfully.

#### Important note before installing

e2 studio has two different types of toolchain for compilation of the code: CC-RX C Compiler Package for RX Family and
GCC for Renesas RX. The first one is a licensed compiler used by Renesas and the second one is a free open-source
toolchain. Thus, always select GCC than CC-RX.

The quick start guide tells about installing and registering the GCC for Renesas RX for a custom installation. If for
some reason, the GCC is not installed correctly, please refer to this document at section
6.3.2:  [Quick Start Guide for the Linux Hosted Version of the e² studio](https://www.renesas.com/en/document/mat/quick-start-guide-linux-hosted-version-e-studio?r=488826)

### E2-Lite Driver Installation

The board used in the development is the RTK5RX65N Targert board from Renesas. It comes with a built-in
Emulator/Debugger called E2-Lite that needs driver installation.

First, go
to [Renesas E2 Emulator Lite official webpage](https://www.renesas.com/en/software-tool/e2-emulator-lite-rte0t0002lkce00000r).
Once there, navigate through the page to find the `Downloads` section. In there, search for
`E2 emulator, E2 emulator Lite Linux Driver` and download it. Extract the files and read the `e2studio_setup.md` file
that explain how to install it.

## Reference

- [Quick Start Guide for the Linux Hosted Version of the e² studio](https://www.renesas.com/en/document/mat/quick-start-guide-linux-hosted-version-e-studio?r=488826)
- [e² studio - Integrated Development Environment - User’s Manual: Quick Start Guide](https://www.renesas.com/en/document/mat/e-studio-quick-start-guide-rxrl78rh850risc-v-mcu-family?r=488826)