import asyncio
import math
from projectairsim import Drone
from projectairsim import projectairsim_log

async def fly_square(drone, side_length=10, duration_per_side=5, takeoff_height=5):
    """
    Makes the drone fly in a square path.

    Args:
        drone: The Drone object from ProjectAirSim.
        side_length: Length of each side in meters.
        duration_per_side: Time to fly each side in seconds.
        takeoff_height: Height to takeoff to if not already in air.
    """
    # Check if drone is taken off; if not, takeoff
    if not drone.is_flying():
        projectairsim_log().info("Taking off...")
        await drone.takeoff_async()
        await drone.move_to_position_async(0, 0, -takeoff_height, 5)  # Hover at height
        projectairsim_log().info("Takeoff complete.")

    velocity = side_length / duration_per_side  # Calculate velocity

    for side in range(4):
        projectairsim_log().info(f"Flying side {side + 1}...")
        # Move forward (north)
        await drone.move_by_velocity_async(v_north=velocity, v_east=0, v_down=0, duration=duration_per_side)
        # Turn right 90 degrees
        await drone.rotate_to_yaw_async(yaw=math.radians(-90 * (side + 1)), timeout_sec=5)
        projectairsim_log().info(f"Side {side + 1} complete.")

    # Land after square
    projectairsim_log().info("Landing...")
    await drone.land_async()
    projectairsim_log().info("Square flight complete.")
