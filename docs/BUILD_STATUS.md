# Golden Machine : Percision 5860 Tower
Windows 11
Processor	Intel(R) Xeon(R) w3-2435 (3.10 GHz)
Graphics Card: NVIDIA RTX A4000 (16GB)
Installed RAM	32.0 GB (31.3 GB usable)
System type	64-bit operating system, x64-based processor
Unreal Engine Version 5.7.3
Python 3.9.13

Installations:
1. Install Visual Studio Code Version: 1.109.4 for Windows through "https://code.visualstudio.com/download"
2. Install Python Version 3.9.13 through command prompt entry: "winget install Python.Python.3.9"
3. Install Epic Game Launcher through "https://www.unrealengine.com/en-US/download'
4. Create and Login into an Epic Games Account
5. Install Unreal Engine version 5.7.3 from the Epic Games Launcher

Repository Cloning: Once done with all the installation,
6. Created a local folder titled "CSDP_499_Research" on Desktop
7. Launch Visual Studio Code 
8. Open "CSDP_499_Research" on Visual Studio Code
9. Open Terminal on this folder
10. in the terminal line ending in "...\Desktop\CSDP_499_Research>", run "git clone https://github.com/NburtonII/499-Codrone-Sim"
11. You should now have cloned the Github repository unto "CSDP_499_Research"

Launching the Unreal Project: To open the Basic Arena, the template for our virtual simulation space:
12. After installing Unreal Engine, Launch it
13. On the Unreal Engine home page, Select My Projects
14. Navigate to Browse and the bottom right corner of the My Projects window
15. Navigate to the CSDP_499_Research folder and traverse "CSDP_499_Research\499-Codrone-Sim\sim\CodroneSim"
16. Double-click on CodroneSim.uproject to open the file
17. Once the project opens, Click Content Drawer, at the bottom left of the window
18. Next, Click Maps
19. Double-click on BasinArena when it shows up
20. BasicArena acquired

Setting AirSim
21. Repeat this steps(previously mentioned) if necessary(closed your instance of Visual Studio Code etc):
    1. Launch Visual Studio Code 
    2. Open "CSDP_499_Research" on Visual Studio Code
    3. Open Terminal on this folder
22. in the terminal line ending in "...\Desktop\CSDP_499_Research>", run the following:
    1. "git clone https://github.com/microsoft/AirSim.git"
    2. "cd AirSim"
23. Press the Windows button and in the search bar, search "x64 Native Tools Command Prompt for VS 2022". This leads to the Visual Studio 2022 Developer Command Prompt v17.14.17
24. On the Visual Studio 2022 Developer Command Prompt v17.14.17, run the following:
    1. "cd C:\Users\animu\OneDrive\Desktop\CSDP_499_Research\AirSim"
    2. "build.cmd"
28. Ran into errors : Couldn't find the GenerateProjectFiles.bat

Setting Up Python Environment
