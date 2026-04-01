##Imports for airsim
import asyncio

from projectairsim import ProjectAirSimClient, Drone, World
from projectairsim.utils import projectairsim_log



###imports for user Control
import time
import csv
import os
import re
import json
import asyncio
from UserControl import UserControl
from DroneSquare import fly_square

async def main():
    DroneController = UserControl()
    DroneController.connect()
    Running  = True
    ###Intro
    try:
        projectairsim_log().info("Welcome to to Class 499's Codrone Simulator!\n We will begin the connecting process now.")
        while Running:
            await DroneController.Input_Command()
            Input = input("Continue Flying? (y/n): ")
            if Input.lower() == "n":
                Running = False
    except KeyboardInterrupt:
        DroneController.close()
        projectairsim_log().info("\nInterrupted by user.")
        
    except Exception as e:
        DroneController.close()
        projectairsim_log().error(f"An error occurred: {e}")

    finally:
        DroneController.close()
        projectairsim_log().info("Exiting Drone Control. Goodbye!\n")
        


if __name__ == "__main__":
    asyncio.run(main())