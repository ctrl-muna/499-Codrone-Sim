# examples/04_run_mission_from_json.py

#
# Prerequisites:
#   1. Start the Unreal simulator.
#   2. Activate your virtual environment.
#   3. Run from the repo root:
#        python examples/04_run_mission_from_json.py
#
# What this does:
#   - Connects to the simulator via UserControl.
#   - Reads missions/square_path.json and executes each step.
#   - Prints a summary and writes runs/Run_{N}_metrics.json on completion.

import asyncio
import os
import sys

# Allow import of sdk/client modules when running from the repo root or examples/.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "client"))

from UserControl import UserControl          # noqa: E402
from mission_runner import run_mission       # noqa: E402


MISSION_FILE = os.path.join(
    os.path.dirname(__file__), "..", "missions", "square_path.json"
)


async def main():
    mission_path = os.path.abspath(MISSION_FILE)
    print(f"Mission file : {mission_path}")

    controller = UserControl()
    controller.connect()

    try:
        print("Running mission ...\n")
        metrics = await run_mission(mission_path, controller)

        print("--- Mission Complete ---")
        print(f"  Success          : {metrics['success']}")
        print(f"  Completion time  : {metrics['completion_time_s']} s")
        print(f"  Collisions       : {metrics['collisions']}")
        if metrics["failure_reason"]:
            print(f"  Failure reason   : {metrics['failure_reason']}")
        print(f"\n  metrics.json written to: "
              f"runs/Run_{controller.runNumber}_metrics.json")
    finally:
        controller.close()


if __name__ == "__main__":
    asyncio.run(main())
