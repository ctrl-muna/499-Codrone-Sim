import time
import csv
import os
import re
import json
import asyncio
import math
from turtle import speed

from projectairsim import ProjectAirSimClient, Drone, World
from projectairsim.utils import projectairsim_log


class UserControl:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.CommandFilePath = None
        self.TelemetryFilePath = None
        ##Create the client that connects to the Airsim Host, the world ,and spawn drone object 
        self.client = ProjectAirSimClient() 
        self.runNumber = None
        self.takeOff = False
        self.commandList = ["Reset","Close", "Takeoff", "State_Polling","Land", "Forward", "Backward", "Left", "Right", "Up", "Down", "Yaw_Left", "Yaw_Right"]
        self.com_Pattern = "|".join(self.commandList)
        self.world = None
        self.drone = None 
        self.latest_pose = None
        self.collision = False
        self.safeCollisionObjects = ["StaticMeshActor1"]


        self.Kill_z_up = -100
        self.kill_z_down = 0.5

        # store the scene config name so resetSimulator() can reload it
        self.scene_config_name = "scene_basic_drone.jsonc"

    def connect(self):
        try:
            setupFile = os.path.join(self.project_root, 'runs', 'Startup.json')
            self.client.connect()
            try:
                self.world = World(self.client, self.scene_config_name, delay_after_load_sec=2)
            except Exception as e:
                projectairsim_log().error(f"Error creating world: {e}")

            self.drone = Drone(self.client, self.world, "Drone1")
            self._subscribe_drone_topics()  # <-- replaces the two client.subscribe calls
       
        ###Read the set up file and get the run number.
        except Exception as e:
            projectairsim_log().error(f"Error during connection and setup: {e}")    

        try:
            with open(setupFile, 'r') as f:
                setUpInfo = json.load(f)
            ##Get the current Run number
            self.runNumber = int(setUpInfo.get("RunNumber"))
            self.CommandFilePath = os.path.join(self.project_root, 'runs', 'RunCommands', f'Run_{self.runNumber}_Commands.csv')
            self.TelemetryFilePath = os.path.join(self.project_root, 'runs', 'RunTelemetry', f'Run_{self.runNumber}_Telemetry.csv')
        except Exception as e:
            projectairsim_log().error(f"Error reading setup file: {e}")
        ##Arm drone and let it be controlled through api
        projectairsim_log().info(f"Connected to AirSim with run number: {self.runNumber}")    
        self.drone.enable_api_control()
        self.drone.arm()
        
    def _subscribe_drone_topics(self):
    ###Subscribe to pose and collision topics for the current drone object.
        self.client.subscribe(
            self.drone.robot_info["actual_pose"],
            lambda _, pose: setattr(self, 'latest_pose', pose)
        )
        self.client.subscribe(
            self.drone.robot_info["collision_info"],
            lambda _, collision: self._on_collision(collision)
        )

    def save_Command(self, command, Duration, status="ok", notes=""):
        current_Date = time.asctime(time.localtime())
        Command_message = f"{current_Date},{command},{Duration},{status},{notes}"
        with open(self.CommandFilePath, 'a') as f:
            f.write(Command_message + "\n")
    
    def save_Telemetry(self, telemetry_data):
        with open(self.TelemetryFilePath, 'a', newline='') as f:
            f.write(f"{telemetry_data['timestamp']},{telemetry_data['position']['x']},{telemetry_data['position']['y']},{telemetry_data['position']['z']},"
                    f"{telemetry_data['orientation']['w']},{telemetry_data['orientation']['x']},{telemetry_data['orientation']['y']},{telemetry_data['orientation']['z']},{self.collision}\n")
    
    def resetSimulator(self):
    ### Send a reset to the simulator by reloading the scene config.
    ###This is the protocol-level reset: the sim discards all object state
    ###and returns everything to its initial pose, equivalent to a fresh launch.
        projectairsim_log().info("resetSimulator: sending LoadScene request to simulator...")

        try:
            # Disarm safely before reloading
            try:
                self.drone.disarm()
                self.drone.disable_api_control()
            except Exception:
                pass

            # This is the actual sim-side reset message.
            # world.load_scene() calls client.request({ "method": "/Sim/LoadScene", ... })
            # which tells the simulator to destroy and rebuild the entire scene.
            self.world.load_scene(
                self.world.get_configuration(),
                delay_after_load_sec=2
            )
            projectairsim_log().info("resetSimulator: scene reloaded successfully.")

        except Exception as e:
            projectairsim_log().error(f"resetSimulator: failed to reload scene — {e}")
            return

        # Re-initialize the drone object against the fresh scene
        try:
            self.drone = Drone(self.client, self.world, "Drone1")
            self._subscribe_drone_topics()
            self.drone.enable_api_control()
            self.drone.arm()
            self.takeOff = False
            self.collision = False
            self.latest_pose = None
            projectairsim_log().info("resetSimulator: drone re-initialized. Ready to fly.")
        except Exception as e:
            projectairsim_log().error(f"resetSimulator: drone re-initialization failed — {e}")
    
    ##need to add an array of velocities
    async def commandParse(self, com, dur):
        ## Commands to be implemented "Foward, backward, left, up, down, right, yaw_left, yaw_right, hover, pitch_foward, pitch_back, roll_left, roll_right"
        ##Duration measured in seconds however i may need to add speed/velocity values
        if com == "Close":
            self.close()
        elif com == "Reset":
            projectairsim_log().info("Reset: initiating simulator-level scene reload...")
            self.resetSimulator()
        elif com == "Takeoff" or com == "Land":
            if com == "Takeoff":
                if self.takeOff:
                    projectairsim_log().info("Drone is has already taken off.")
                else:
                    try:
                        projectairsim_log().info("takeoff_async: starting")
                        takeoff_task = await self.drone.takeoff_async()
                        await takeoff_task
                        projectairsim_log().info("takeoff_async: completed")
                        self.takeOff = True
                        await self.statePoll(1)
                    except Exception as e:
                        projectairsim_log().error(f"takeoff_async: FAILED — {e}")
                        self.save_Command(com, dur, status="failed", notes=str(e))
                        return
            elif com == "Land":
                if not self.takeOff:
                    projectairsim_log().info("Drone is not in the air.")
                else:
                    try:
                        projectairsim_log().info("land_async: starting")
                        land_task = await self.drone.land_async()
                        await land_task
                        projectairsim_log().info("land_async: completed")
                        self.takeOff = False
                        await self.statePoll(1)
                    except Exception as e:
                        projectairsim_log().error(f"land_async: FAILED — {e}")
                        self.save_Command(com, dur, status="failed", notes=str(e))
                        return
        elif com == "State_Polling":
            projectairsim_log().info("State Polling: Started")
            await self.statePoll(dur)
            projectairsim_log().info("State Polling: Completed")
        elif com in ["Yaw_Left", "Yaw_Right"]:
            if not self.takeOff:
                projectairsim_log().info("Drone is not in the air.")
            else:
                try:
                    speed = 5
                    Degrees = 90
                    yaw_velocity = 30  # degrees per second
                    if com == "Yaw_Left":
                        Degrees = 90
                    elif com == "Yaw_Right":
                        Degrees = -90
                    heading_45_task = await self.drone.rotate_to_yaw_async(
                        yaw=math.radians(Degrees), timeout_sec=dur, margin=0, callback=None
                    )
                    projectairsim_log().info(f"{com} Invoked")
                    await heading_45_task
                    projectairsim_log().info(f"{com} Completed")
                    await self.statePoll(1)
                except Exception as e:
                    projectairsim_log().error(f"{com}: FAILED — {e}")
                    self.save_Command(com, dur, status="failed", notes=str(e))
                    return
        elif com in ["Forward", "Backward", "Left", "Right", "Up", "Down"]:
            if not self.takeOff:
                projectairsim_log().info("Drone is not in the air.")
            else:
                try:
                    velocity = 5  # Default velocity value
                    if com == "Forward":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=velocity, v_east=0.0, v_down=0.0, duration=dur
                        )
                        projectairsim_log().info("Move-Forward Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Forward Completed")
                    elif com == "Backward":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=-velocity, v_east=0.0, v_down=0.0, duration=dur
                        )
                        projectairsim_log().info("Move-Backward Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Backward Completed")
                    elif com == "Left":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=0.0, v_east=-velocity, v_down=0.0, duration=dur
                        )
                        projectairsim_log().info("Move-Left Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Left Completed")
                    elif com == "Right":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=0.0, v_east=velocity, v_down=0.0, duration=dur
                        )
                        projectairsim_log().info("Move-Right Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Right Completed")
                    elif com == "Up":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=0.0, v_east=0.0, v_down=-velocity, duration=dur
                        )
                        projectairsim_log().info("Move-Up Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Up Completed")
                    elif com == "Down":
                        move_down_task = await self.drone.move_by_velocity_async(
                            v_north=0.0, v_east=0.0, v_down=velocity, duration=dur
                        )
                        projectairsim_log().info("Move-Down Invoked")
                        await move_down_task
                        projectairsim_log().info("Move-Down Completed")
                    await self.statePoll(1)
                except Exception as e:
                    projectairsim_log().error(f"{com}: FAILED — {e}")
                    self.save_Command(com, dur, status="failed", notes=str(e))
                    return
                
    def _on_collision(self, collision):
        if not collision.get("has_collided", False):
            return
        
        object_name = collision.get("object_name", "").lower()
        position = collision.get("position", {})

        if object_name in self.safeCollisionObjects:
            return
        if not self.takeOff:
            return
        projectairsim_log().warning(f"Collision detected with object: {object_name} at position: {position}. Initiating emergency landing.")
        self.collision = True
       
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(
            lambda:asyncio.ensure_future(self._emergency_land()))

    async def _emergency_land(self):
        if not self.takeOff:
            return  # already landed, ignore
        
        projectairsim_log().warning("Emergency landing initiated.")
        
        # Stop all movement first
        try:
            stop_task = await self.drone.move_by_velocity_async(
                v_north=0.0, v_east=0.0, v_down=0.0, duration=0.1
            )
            await stop_task
        except Exception as e:
            projectairsim_log().error(f"Failed to stop movement: {e}")

        # Then land
        try:
            land_task = await self.drone.land_async()
            await land_task
            self.takeOff = False
            projectairsim_log().info("Emergency land complete.")
        except Exception as e:
            projectairsim_log().error(f"Emergency land failed: {e}")     


    async def statePoll(self,dur):
        start_time = time.time()
        while time.time() - start_time < dur:
            if self.latest_pose is not None:
                pos = self.latest_pose.get("position", {})
                orientation = self.latest_pose.get("orientation", {})
                z = pos.get("z", 0)
                if z < self.Kill_z_up or z > self.kill_z_down:
                    projectairsim_log().warning(f"Drone has exceeded safe altitude limits (z={z:.3f}). Initiating emergency landing.")
                    try:
                        land_task = await self.drone.land_async()
                        await land_task
                        projectairsim_log().info("Emergency landing completed successfully.")
                    except Exception as e:
                        projectairsim_log().error(f"Error during emergency landing: {e}")
                    break
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
                TelemetryData = {
                    "timestamp": time.asctime(time.localtime()),
                    "position": pos,
                    "orientation": orientation
                }
                self.save_Telemetry(TelemetryData)
            else:
                projectairsim_log().info("Waiting for pose data...")

            await asyncio.sleep(1)

    async def Input_Command(self):
        ##Accept a users command then send it to save_command
        command = None
        while command == None:
            projectairsim_log().info("Valid Commands: ")
            for com in self.commandList:
                projectairsim_log().info(f"{com}")
            projectairsim_log().info("\n")
            inputCommand = input("Enter Command: ")
            command, duration = self.verify_Command(inputCommand)
            if command is None:
                projectairsim_log().error("Invalid command format. Please enter a command in the format 'Command(Duration in seconds)'. For example: 'Takeoff()' or 'State_Polling(5)'.")
            elif duration < 0:
                projectairsim_log().error("Duration must be a positive integer or empty. Please try again.")
                command = None
            elif command not in self.commandList:
                projectairsim_log().error(f"Command must be one of the following: {'| '.join(self.commandList)}. Please try again.")
                command = None
        
        self.save_Command(command, duration, status="ok", notes="")
        await self.commandParse(command, duration)
    
    
    def close(self):
        projectairsim_log().info("Closing User Control")
        projectairsim_log().info(f"Run number {self.runNumber}, has been closed and saved. Thank you.")
        setupFile = os.path.join(self.project_root, 'runs', 'Startup.json')
        with open(setupFile, 'r') as f:
            setUpInfo = json.load(f)
            RunNumberIncrement = self.runNumber + 1
            setUpInfo["RunNumber"] = RunNumberIncrement
        with open(setupFile, 'w') as f:
            json.dump(setUpInfo, f)
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

        finally:
            projectairsim_log().info("User Control Closed Successfully.")
            projectairsim_log().info(f"Run number {setUpInfo['RunNumber']} has been closed and saved to {self.CommandFilePath} and {self.TelemetryFilePath}. Thank you.")

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


