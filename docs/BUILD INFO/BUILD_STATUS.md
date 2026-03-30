# Build Info

This document is meant to give infomration on what machine and hardware the project was initially developed on, and to provide instructions on how to set up the project on other machines.

## Golden Machine

A goleden machine is the computer that this project was required to run on. at the end of everysprint or stories were not considered complete until it coudl run without unexpected issue on this machine. The specifiactions of the machine are as follows:

- Operating System: Windows 11
- Processor: Intel(R) Xeon (R) w3-2435
- Memory - 32 GB Ram
- NVIDIA RTX A4000

## Minimum Requirements

We have to test what the minimum requirements for the project are but will try our best to test this in the future.

##  Set Up Instructions

The following are steps to set up the airsim dependecies in the project.

### Unreal

these instructions assume a fresh install of everything.

1. Make sure you install the following:

    - Install Python 3.14, and
  
    - Unreal 5.7

    - Visual Studio with 2022 build tools.
      - [Download](https://visualstudio.microsoft.com/vs/older-downloads/)
      - Navigate to link above open the 2022 tab and click Download.
      - Sign into to your Microsoft App.
      - Downlaod the latest Build Tools for Visual Studio 2022
      - Proced with Vs studio installer instructions.
        - Make sure you include "MSVC v143 - VS 2022 C++ x64/x86 build tools"

2. Navigate to your prefered Directory and clone the repo using:

```bash
    Git clone https://github.com/NburtonII/499-Codrone-Sim.git
```

3. In addition you must clone the IAMAI's project airsim repo. you can clone it into the sdk directory of the project using:

```bash
cd <Directorylocation>/sdk
git clone https://github.com/iamaisim/ProjectAirSim.git
```

4. The simLibs from the airsim repo must be build do that by running the build.cmd. Open "x64 Nativ Tools Command Prompt for 2022". Navitgate to the projects directory and open  /sdk/projectairsim. Then run build.cmd in the command line.

```bash
cd PathtoClone/sdk/ProjectAirSim
set VSCMD_ARG_TGT_ARCH=x64
set VSCMD_ARG_HOST_ARCH=x64
set UE_ROOT=C:\Program Files\Epic Games\UE_5.7
build.cmd -Wno-dev simlib_release
```

5. Navigate to sdk\ProjectAirSim\unreal\Blocks. Run: blocks_genprojfiles_vscode.bat

  >[!Note]
  >Ensure that the UE_ROOT is set, running this will cause errors if it isnt.

1. Once finished with the last step. Copy sdk/ProjectAirSim\unreal\Blocks\Plugins to the sim folder in the main directory. It is fine to replace the current plugins directory.

2. Launch the unrela project in the sim directory. Click build when the unreal messages popsup. The system will be ready once finished.

### Python SDK
1. Navigate to the python client directory
  >>sdk\ProjectAirSim\client\python\projectairsim

2. Now install python libraries using:

  ```cmd
  pip install .
  ```
