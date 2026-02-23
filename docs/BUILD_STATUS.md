# Golden Machine : Muna's Laptop
Windows 11
16GB RAM
AMD Ryzen 7 8840HS w/ Radeon 780M

## Must find out Unreal and python Versions for setup steps
//Partly done blind. I would have to confirm this with a lab system
Anything in ** is to be confirmed or expanded on.

Installations:
1. Install Visual Studio Code Version: 1.109.4
2. Install Python Version 3.14.0
3. Install Epic Game Launcher
4. Create and Login into an Epic Games Account
5.** Install Unreal Engine version 5.7 from the Epic Games Launcher
6.** It's a blur to me (literally dont know)

Repository Cloning: Once done with all the installation,
7. Created a local folder titled "CSDP_499_Research" on Desktop
8. Launch Visual Studio Code 
9. Open "CSDP_499_Research" on Visual Studio Code
10. Open Terminal on this folder
11. in the terminal line ending in "...\Desktop\CSDP_499_Research>", run "git clone https://github.com/NburtonII/499-Codrone-Sim
12. Afterwards, run the following commands:
    1. cd 499-Codrone-Sim
    2. git fetch origin
    3. git pull
13. You should now have cloned the Github repository unto "CSDP_499_Research"

**Launching the Unreal Project: To open the Basic Arena, the template for our virtual simulation space:
14. Open the "CSDP_499_Research" local folder
15. Locate the CodroneSim.uproject file, following the file path ending with "...\CSDP_499_Research\499-Codrone-Sim\sim\CodroneSim"
***Need to add the next steps here on opening the file on Unreal
**This could be after some steps from above:
16. Rebuild Missing Modules (Crucial) Since GitHub repositories usually exclude "Binaries" and "Intermediate" folders to save space, Unreal will likely tell you: "The following modules are missing or built with a different engine version. Would you like to rebuild them now?"
17. Click Yes
18.** Verify the project in the Epic Games Launcher:
    1.
    2.
    3.
    4.
19.
