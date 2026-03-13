# Command Specifications

## Command List
This is a list of the currently implemented commands and references for them
The main interface is run through the DroneClientControl.py. It creates a UserControl object that creates the client and then connects it to the Airsim Unreal server.

### Command Format
All current Commands are either in the format:
- CommandName()
or
- CommandName(DurationInSeconds)

The system will give an error if commands are sent through the terminal that are not in this format.

#### Command Reference
##### Takeoff
- Syntax Example: Takeoff()
- Description: This command takes  puts the drone in the air after about a second.
- Parameters: No parameters required here. If a duration is given it will simply do nothing. 
- Preconditions: The Drone has to be on the ground/landed. If it is in the air the takeoff method will return an error.
- The Command Log will store takeoff Commands like so: 
    - DayofTheWeek Month Date Time year,Takeoff,0
    > The 0 at the end is returned for all commands that do not accept a duration.

##### Land
- Syntax Example: Land()
- Description: This command lands the drone on the ground of the scene
- Parameters: No parameters required here. If a duration is given it will simply do nothing. 
- Preconditions: The Drone has to be in the air. If it is air-born then the  land method will return an error.
- The Command Log will store takeoff Commands like so: 
    - dayofTheWeek Month Date Time year,Land,0
##### State_Polling
- Syntax Example: State_Polling(Duration)
- Description: This Commands reports on the location and status of the drone both in the terminal and the telemetry log for the run.
- Parameters: Duration is required.
- Preconditions: No preconditions required.
- The Command Log will store takeoff Commands like so: 
    - DayofTheWeek Month Date Time year,State_Polling,0
- The telemetry log will store each telemetry data entry like so:
    - dayofTheWeek Month Date Time year,Pos_x,Pos_y,Pos_z,orientation_w,orientation_y,orientation_y,orientation_z

>This command is run internally when ever any command is given as well.

##### Close
- Syntax Example: Close()
- Description: This commands Ends the client Connection to the unreal server.
- Parameters: No parameters required here. If a duration is given it will simply do nothing. 
- Preconditions: the Client has to be connected.
- The Command Log will store takeoff Commands like so: 
    - dayofTheWeek Month Date Time year,Close,0


## State Model
As of now there are only two states the drone can be in but we will add more.
- Takeoff = False
    - Assumed that drone is in on the ground. Takeoff() is valid and Land() is Disabled.
- Takeoff = True
    - Assumed that drone is in the air. Takeoff() is disabled and Land() Valid.
## Data Logging
There are 3 files/folders that store important data.
- Startup.json
- RunTelemetry
- RunCommands
### Startup.json
This file is simple and likely to change it simply stores the incrementing run number permanently so that the run number is saved when the script is no longer running. It only stores file in the format: 
- {"RunNumber": 4}

## RunTelemetry
This folder is where we store telemetry files. These are csv (Comma-Separated Values) files that hold all the telemetry data for each run. Each entry is stored in the format:
- DayofTheWeek Month Date Time year,Pos_x,Pos_y,Pos_z,orientation_w,orientation_y,orientation_y,orientation_z

The files are created and named automatically in the format:
- Run_[runNumber]_Telemetry.csv

## RunCommands
This folder is where we store the command files. These are CSV files that hold a running log of all inputted Commands.

> The format of this may change as we add functionality
Each entry is stored in the format: 
- DayofTheWeek Month Dat TimeStamp Year,Command,Duration

## Run Number System
Each run has is identified by its own unique integer. When the System is closed this number is incremented in preparation for the next run. These numbers are used to create the Run_x_Commands.csv file for storing a log of Commands, and the Run_x_telemetry.csv file for storing the telemetry data. 