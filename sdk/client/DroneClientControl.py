##Imports for airsim
import asyncio

from projectairsim import ProjectAirSimClient, Drone, World
from projectairsim.utils import projectairsim_log
from projectairsim.image_utils import ImageDisplay


###imports for user Control
import time
import csv
import os
import re
import json
import asyncio
from UserControl import UserControl

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
        projectairsim_log().info("\nInterrupted by user.")
    except Exception as e:
        projectairsim_log().error(f"An error occurred: {e}")

    finally:
        projectairsim_log().info("Exiting Drone Control. Goodbye!\n")
        DroneController.close()


if __name__ == "__main__":
    asyncio.run(main())