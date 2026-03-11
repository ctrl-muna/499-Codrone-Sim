import time
import csv
import os
import re
import json
import asyncio

from projectairsim import ProjectAirSimClient, Drone, World
from projectairsim.utils import projectairsim_log
from projectairsim.image_utils import ImageDisplay

class UserControl:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ##Create the client that connects to the Airsim Host, the world ,and spawn drone object 
        self.client = ProjectAirSimClient() 
        self.runNumber = None
        self.takeOff = False
        self.commandList = ["Close", "Takeoff", "State_Polling", "Hover", "Land"]
        self.com_Pattern = "|".join(self.commandList)
        self.CommandFilePath = os.path.join(self.project_root, 'runs', 'RunCommands', f'Run_{self.runNumber}_Commands.csv')
        self.world = None
        self.drone = None 
        self.latest_pose = None

    def connect(self):
        setupFile = os.path.join(self.project_root, 'runs', 'Startup.json')
        self.client.connect()
        self.world = World(self.client, "scene_basic_drone.jsonc", delay_after_load_sec=2)
        self.drone = Drone(self.client, self.world, "Drone1")
        self.client.subscribe(
            self.drone.robot_info["actual_pose"],
            lambda _,pose: setattr(self,'latest_pose',pose)
            )
        ###Read the set up file and get the run number.
        print(f"Project root: {self.project_root}")
        print(f"Looking for: {setupFile}")
        with open(setupFile, 'r') as f:
            setUpInfo = json.load(f)
        ##Get the current Run number
        self.runNumber = int(setUpInfo.get("RunNumber"))
        ##arm drone and let it be controlled through api
        self.drone.enable_api_control()
        self.drone.arm()
        
    
    def save_Command(self, command, Duration):
        current_Date = time.asctime(time.localtime())
        Command_message = f"{current_Date},{command},{Duration}"
        ##This will save the command to the run file and close it after the command is saved
        ##Open Commadn file(Create if it doesnt exist)
        with open(self.CommandFilePath, 'a') as f:
            f.write(Command_message + "\n")
    
    ##need to add an array of velocieties
    async def commandParse(self, com, dur):
        ## Command to b eplemented 
        if com == "Close":
            self.close()
        elif com == "Takeoff" or com == "Land":
            if com == "Takeoff":
                if self.takeOff:
                    print("Drone is has already taken off.")
                else:
                    projectairsim_log().info("takeoff_async: starting")
                    takeoff_task = (await self.drone.takeoff_async())
                    await takeoff_task  # schedule an async task to start the command
                    projectairsim_log().info("takeoff_async: completed")
                    self.takeOff = True
                    await self.statePoll(1)
            elif com == "Land":
                if not self.takeOff:
                    print("Drone is not in the air.")
                else:
                    projectairsim_log().info("land_async: starting")
                    land_task = (await self.drone.land_async())
                    await land_task  # schedule an async task to start the command
                    projectairsim_log().info("land_async: completed")
                    self.takeOff = False
                    await self.statePoll(1)
        elif com == "State_Polling":
            projectairsim_log().info("State Polling: Started")
            await self.statePoll(dur)
            projectairsim_log().info("State Polling: Completed")
  
    async def statePoll(self,dur):
        start_time = time.time()
        while time.time() - start_time < dur:
            if self.latest_pose is not None:
                pos = self.latest_pose.get("position", {})
                orientation = self.latest_pose.get("orientation", {})
                projectairsim_log().info(
                    f"Drone State at {time.asctime(time.localtime())}:\n"
                    f"  Position  -> N: {pos.get('x', 0):.3f}, "
                    f"E: {pos.get('y', 0):.3f}, "
                    f"D: {pos.get('z', 0):.3f}\n"
                    f"  Orientation -> W: {orientation.get('w', 0):.3f}, "
                    f"X: {orientation.get('x', 0):.3f}, "
                    f"Y: {orientation.get('y', 0):.3f}, "
                    f"Z: {orientation.get('z', 0):.3f}"
            )
            else:
                projectairsim_log().info("Waiting for pose data...")
            await asyncio.sleep(1)

    async def Input_Command(self):
        ##Accept a users command then send it to save_command
        command = None
        while command == None:
            print("Valid Commands: ")
            for com in self.commandList:
                print(f"{com}|")
            print("\n")
            inputCommand = input("Enter Command: ")
            command, duration = self.verify_Command(inputCommand)
            if duration < 0:
                print("Duration must be a positive integer or empty. Please try again.")
                command = None
            elif command not in self.commandList:
                print(f"Command must be one of the following: {'| '.join(self.commandList)}. Please try again.")
                command = None

            await self.commandParse(command, duration)
    
    
    def close(self):
        print("Closing User Control")
        setupFile = os.path.join(self.project_root, 'runs', 'Startup.json')
        with open(setupFile, 'r') as f:
            setUpInfo = json.load(f)
            RunNumberIncrement = int(setUpInfo["RunNumber"]) + 1
            setUpInfo["RunNumber"] = RunNumberIncrement
        with open(setupFile, 'w') as f:
            json.dump(setUpInfo, f)
        print(f"Run number {setUpInfo['RunNumber']}, has been closed and saved. Thank you.")
         # Safely shut down drone even if mid-flight
        try:
            self.drone.land()
        except:
            pass
    
        try:
            self.drone.disarm()
            self.drone.disable_api_control()
        except:
            pass
    
        try:
            self.client.disconnect()
        except:
            pass

    def verify_Command(self, command):
        pattern = rf"^({self.com_Pattern})\((\d+|\B)\)$"
        match = re.match(pattern, command)
        
        if match:
            command = match.group(1)
            number = int(match.group(2)) if match.group(2) else 0
            return command,number
        
        return None,None
        
    ##Not sure if this function is neccsassaary
    ##This entirely depends on if the Telemetry.csv file needs processing in the python Sdk
    def ReadCSV(self, filePath):
        ##This will read the csv file and return the data in a list of dictionaries
        ##Open CSV file
        ##Read CSV file and convert to list of dictionaries
        ##Close CSV file
        ##Return list of dictionaries
        pass



