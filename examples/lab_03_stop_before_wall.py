# examples/lab_03_stop_before_wall.py

#
# Prerequisites:
#   1. Start the Unreal simulator.
#   2. Activate your virtual environment (Python 3.9).
#   3. Run from the repo root:
#        py -3.9 examples/lab_03_stop_before_wall.py
#
# What this does:
#   - Connects to the simulator via UserControl.
#   - Takes off and flies forward.
#   - Polls the FrontRange distance sensor every 0.5 s.
#   - Stops (hovers) automatically when the wall is closer than STOP_THRESHOLD_M.
#   - Lands and disconnects.
#
# Sensor requirement:
#   FrontRange must be configured in
#   sdk/client/sim_config/robot_quadrotor_fastphysics.jsonc (added Week 6).

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "client"))

from UserControl import UserControl        # noqa: E402
from range_sensor import get_front_range   # noqa: E402

STOP_THRESHOLD_M = 2.0   # stop when wall is closer than 2 metres
POLL_INTERVAL_S  = 0.5   # check range every 0.5 seconds
FLY_DURATION_S   = 10.0  # maximum forward flight time (safety cap)


async def main():
    controller = UserControl()
    controller.connect()

    try:
        print("Taking off...")
        await controller.commandParse("Takeoff", 0)

        print(f"Flying forward. Will stop if wall < {STOP_THRESHOLD_M} m away.")
        fly_task = asyncio.create_task(
            controller.commandParse("Forward", FLY_DURATION_S)
        )

        elapsed = 0.0
        while elapsed < FLY_DURATION_S:
            await asyncio.sleep(POLL_INTERVAL_S)
            elapsed += POLL_INTERVAL_S

            distance_m = await get_front_range(controller, timeout_s=0.5)
            if distance_m is None:
                print(f"  [{elapsed:.1f}s] FrontRange: no reading")
                continue

            distance_cm = distance_m * 100
            print(f"  [{elapsed:.1f}s] FrontRange: {distance_cm:.1f} cm")

            if distance_m <= STOP_THRESHOLD_M:
                print(f"  Wall detected at {distance_cm:.1f} cm — stopping.")
                fly_task.cancel()
                # Hover briefly to let the drone decelerate.
                await controller.commandParse("State_Polling", 1)
                break

        # Wait for fly_task to finish if it wasn't cancelled.
        try:
            await fly_task
        except asyncio.CancelledError:
            pass

        print("Landing...")
        await controller.commandParse("Land", 0)
        print("Done.")

    finally:
        controller.close()


if __name__ == "__main__":
    asyncio.run(main())
