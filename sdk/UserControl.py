import time
import csv
import os
import re
import json

class UserControl:
    def __init__(self):
        self.runNumber = None
        self.takeOff = False
        self.commandList = ["Close", "Takeoff", "State_Polling", "Hover", "Land"]
        self.com_Pattern = "|".join(self.commandList)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.runNumber = self.connect()
        self.CommandFilePath = os.path.join(self.project_root, 'runs', 'RunCommands', f'Run_{self.runNumber}_Commands.csv')
        
    def connect(self):
        ##This Gets the root Directory so this will work on other macchines that downlaod the GitBub repo
        setupFile = os.path.join(self.project_root, 'runs', 'Startup.json')
        ###Read the set up file and get the run number.
        with open(setupFile, 'r') as f:
            setUpInfo = json.load(f)
        ##Get the current Run number
        runNumber = int(setUpInfo.get("RunNumber", 0))
        return runNumber
            
    
    def save_Command(self, command, Duration):
        current_Date = time.asctime(time.localtime())
        Command_message = f"{current_Date},{command},{Duration}"
        ##This will save the command to the run file and close it after the command is saved
        ##Open Commadn file(Create if it doesnt exist)
        with open(self.CommandFilePath, 'a') as f:
            f.write(Command_message + "\n")
        
    
    def Input_Command(self):
        ##Accept a users command then send it to save_command
        command = None
        while command == None:
            inputCommand = input("Enter Command: ")
            command, duration = self.verify_Command(inputCommand)
            if duration < 0:
                print("Duration must be a positive integer or empty. Please try again.")
                command = None
            elif command not in self.commandList:
                print(f"Command must be one of the following: {', '.join(self.commandList)}. Please try again.")
                command = None
            elif command == "Close()":
                self.close()
            elif command == "Takeoff" or command == "Land":
                if command == "Takeoff":
                    if self.takeOff:
                        print("Drone is has already taken off.")
                    else:
                        self.takeOff = True
                elif command == "Land":
                    if not self.takeOff:
                        print("Drone is not in the air.")
                    else:
                        self.takeOff = False
        self.save_Command(command, duration)
                
         
        
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