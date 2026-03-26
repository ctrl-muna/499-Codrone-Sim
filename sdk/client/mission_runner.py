# sdk/client/mission_runner.py

#
# Reads a JSON mission config and executes each step via UserControl.commandParse().
# Writes runs/Run_{N}_metrics.json on completion using the existing run-numbering
# convention established by UserControl (runs/Startup.json).
#
# Public API:
#   load_mission(json_path)              -> list of step dicts  (pure, sync, testable)
#   run_mission(json_path, controller)   -> metrics dict        (async, requires connected controller)

import asyncio
import json
import os
import time

# Must match UserControl.commandList exactly (case-sensitive).
VALID_COMMANDS = [
    "Reset", "Close", "Takeoff", "State_Polling", "Land",
    "Forward", "Backward", "Left", "Right", "Up", "Down",
    "Yaw_Left", "Yaw_Right",
]


def load_mission(json_path):
    """
    Load and validate a mission JSON file.

    Args:
        json_path (str): Path to the mission JSON file.

    Returns:
        list: Validated list of step dicts, each with 'command' and 'duration'.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError:        If the file structure or step fields are invalid.
    """
    with open(json_path, "r") as f:
        mission = json.load(f)

    if "steps" not in mission:
        raise ValueError(f"Mission file missing 'steps' key: {json_path}")

    steps = mission["steps"]

    if not isinstance(steps, list) or len(steps) == 0:
        raise ValueError(f"Mission 'steps' must be a non-empty list: {json_path}")

    for i, step in enumerate(steps):
        if "command" not in step:
            raise ValueError(f"Step {i} missing required field 'command'")
        if "duration" not in step:
            raise ValueError(f"Step {i} missing required field 'duration'")
        if step["command"] not in VALID_COMMANDS:
            raise ValueError(
                f"Step {i} has unknown command: '{step['command']}'. "
                f"Valid commands: {VALID_COMMANDS}"
            )
        if not isinstance(step["duration"], (int, float)) or step["duration"] < 0:
            raise ValueError(
                f"Step {i} has invalid duration: '{step['duration']}'. "
                f"Must be a non-negative number."
            )

    return steps


async def run_mission(json_path, controller):
    """
    Execute a mission from a JSON config file using a connected UserControl instance.

    Reads steps from the JSON file, executes each via controller.commandParse(),
    and writes a metrics.json file to runs/Run_{N}_metrics.json on completion.

    Args:
        json_path  (str):         Path to the mission JSON file.
        controller (UserControl): A connected, armed UserControl instance.

    Returns:
        dict: Metrics with keys: success, completion_time_s, collisions, failure_reason.
    """
    steps = load_mission(json_path)

    start_time = time.time()
    success = True
    failure_reason = None

    try:
        for step in steps:
            command = step["command"]
            duration = step["duration"]

            controller.save_Command(command, duration)
            await controller.commandParse(command, duration)

            # Stop the mission early if a collision was detected mid-step.
            if controller.collision:
                success = False
                failure_reason = "collision"
                break

    except Exception as e:
        success = False
        failure_reason = str(e)

    completion_time_s = round(time.time() - start_time, 3)

    # collision is a bool in the current UserControl implementation;
    # reported as 0 or 1 here. Multi-collision counting is a future enhancement.
    collisions = 1 if controller.collision else 0

    metrics = {
        "success": success,
        "completion_time_s": completion_time_s,
        "collisions": collisions,
        "failure_reason": failure_reason,
    }

    _write_metrics(metrics, controller)
    return metrics


def _write_metrics(metrics, controller):
    """
    Write the metrics dict to runs/Run_{N}_metrics.json.

    Follows the existing run-file naming convention:
      runs/Run_{N}_Commands.csv
      runs/Run_{N}_Telemetry.csv
      runs/Run_{N}_metrics.json   <- written here
    """
    metrics_path = os.path.join(
        controller.project_root,
        "runs",
        f"Run_{controller.runNumber}_metrics.json",
    )
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
