# Mission Config Specification

**Version:** 1.0
**Week:** 5
**Owner:** R5 – Python SDK, QA & Documentation Engineer

---

## Overview

A mission is a JSON file that defines an ordered sequence of drone commands.
The mission runner (`sdk/client/mission_runner.py`) reads this file and executes
each step by calling `UserControl.commandParse()`.

## File Location

Mission files live in the `missions/` directory at the repo root:

```
missions/
  square_path.json      <- Week 5 reference mission
  placeHolder.txt       <- pre-existing placeholder
```

---

## JSON Schema

```json
{
  "mission_id":  "<string>",
  "description": "<string>",
  "version":     "<string>",
  "steps": [
    { "command": "<CommandName>", "duration": <seconds> },
    ...
  ]
}
```

### Top-level fields

| Field         | Type   | Required | Description                          |
|---------------|--------|----------|--------------------------------------|
| `mission_id`  | string | No       | Human-readable identifier            |
| `description` | string | No       | Brief description of the mission     |
| `version`     | string | No       | Mission definition version string    |
| `steps`       | array  | **Yes**  | Ordered list of steps to execute     |

### Step fields

| Field      | Type          | Required | Description                              |
|------------|---------------|----------|------------------------------------------|
| `command`  | string        | **Yes**  | One of the valid command names (below)   |
| `duration` | number (>= 0) | **Yes**  | Duration in seconds; 0 for instant cmds |

---

## Valid Commands

Commands must match `UserControl.commandList` exactly (case-sensitive).

| Command         | Duration | Notes                                         |
|-----------------|----------|-----------------------------------------------|
| `Takeoff`       | 0        | Arms and takes off; ignores duration value    |
| `Land`          | 0        | Lands the drone; ignores duration value       |
| `Forward`       | seconds  | Move forward at fixed velocity for N seconds  |
| `Backward`      | seconds  | Move backward for N seconds                   |
| `Left`          | seconds  | Move left for N seconds                       |
| `Right`         | seconds  | Move right for N seconds                      |
| `Up`            | seconds  | Move up for N seconds                         |
| `Down`          | seconds  | Move down for N seconds                       |
| `Yaw_Left`      | seconds  | Rotate 90° left; duration is timeout          |
| `Yaw_Right`     | seconds  | Rotate 90° right; duration is timeout         |
| `State_Polling` | seconds  | Poll and log drone state for N seconds        |
| `Reset`         | 0        | Reset drone to spawn; ignores duration        |
| `Close`         | 0        | Close the session (avoid inside missions)     |

---

## Example: `missions/square_path.json`

```json
{
  "mission_id": "square_path",
  "description": "Fly a square path: takeoff, four forward legs with right turns, land.",
  "version": "1.0",
  "steps": [
    { "command": "Takeoff",   "duration": 0 },
    { "command": "Forward",   "duration": 2 },
    { "command": "Yaw_Right", "duration": 2 },
    { "command": "Forward",   "duration": 2 },
    { "command": "Yaw_Right", "duration": 2 },
    { "command": "Forward",   "duration": 2 },
    { "command": "Yaw_Right", "duration": 2 },
    { "command": "Forward",   "duration": 2 },
    { "command": "Yaw_Right", "duration": 2 },
    { "command": "Land",      "duration": 0 }
  ]
}
```

---

## Parsing and Validation

`load_mission(json_path)` in `sdk/client/mission_runner.py`:

1. Opens and parses the JSON file.
2. Verifies `steps` key is present and non-empty.
3. Verifies each step has `command` and `duration`.
4. Verifies `command` is in `VALID_COMMANDS`.
5. Verifies `duration` is a non-negative number.
6. Returns the validated steps list on success.
7. Raises `ValueError` (or `FileNotFoundError`) on any violation.

Unit tests: `tests/test_mission_parser.py`

---

## Running a Mission

```python
from mission_runner import run_mission
from UserControl import UserControl
import asyncio

async def main():
    controller = UserControl()
    controller.connect()
    metrics = await run_mission("missions/square_path.json", controller)
    controller.close()

asyncio.run(main())
```

See also: `examples/04_run_mission_from_json.py`
