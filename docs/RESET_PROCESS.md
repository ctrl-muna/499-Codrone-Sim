# Reset Process

**Version:** 1.0
**Week:** 5
**Owner:** R5 – Python SDK, QA & Documentation Engineer

---

## Overview

This document describes how to reset the drone and repeat mission runs without
manually restarting the Unreal simulator.

Two reset modes are available:

| Mode | Method | Use when |
|---|---|---|
| In-session soft reset | `controller.resetDrone()` | You want to re-run without changing the run number or log files |
| Full session restart | `controller.close()` + reconnect | You want a clean run number, fresh log files, and a reset collision flag |

---

## In-Session Soft Reset

`UserControl.resetDrone()` resets the drone object within the current session:

1. Disarms the current drone.
2. Disables API control.
3. Deletes the drone object.
4. Re-creates the `Drone` object on the same `world` and `client`.
5. Re-enables API control and re-arms.

After `resetDrone()`, the drone is back at its spawn position and ready for another run.
The session (`client`, `world`, `runNumber`, log file paths) is **preserved**.

```python
controller.resetDrone()
# drone is at spawn; same runNumber; same log files (appended, not overwritten)
```

**Limitation:** `self.collision` is **not** reset by `resetDrone()`. If a collision
occurred in the previous run, `metrics["collisions"]` will still be `1` in the next run.
Use a full session restart for a clean collision state.

---

## Full Session Restart

To start a completely new session (new run number, new log files, reset collision flag):

```python
# End the current session
controller.close()          # increments RunNumber in runs/Startup.json, safely lands drone

# Start a new session
controller = UserControl()
controller.connect()        # reads the new RunNumber; creates new log file paths
```

---

## Run Numbering

Each session uses a run number read from `runs/Startup.json` at connect time.
`close()` increments the counter so the next session gets a fresh number.

| File | Description |
|---|---|
| `runs/Startup.json` | `{"RunNumber": N}` — incremented by `close()` |
| `runs/RunCommands/Run_{N}_Commands.csv` | Commands logged during run N |
| `runs/RunTelemetry/Run_{N}_Telemetry.csv` | Telemetry logged during run N |
| `runs/Run_{N}_metrics.json` | Mission metrics written at end of run N |

---

## Repeating a Mission (Examples)

### Option A: Full restart between runs (cleanest state)

```python
import asyncio
from UserControl import UserControl
from mission_runner import run_mission

async def main():
    # Run 1
    controller = UserControl()
    controller.connect()
    metrics1 = await run_mission("missions/square_path.json", controller)
    controller.close()
    print("Run 1:", metrics1)

    # Run 2 — new run number, fresh logs, collision flag reset
    controller = UserControl()
    controller.connect()
    metrics2 = await run_mission("missions/square_path.json", controller)
    controller.close()
    print("Run 2:", metrics2)

asyncio.run(main())
```

### Option B: Soft reset between runs (same session, faster)

```python
import asyncio
from UserControl import UserControl
from mission_runner import run_mission

async def main():
    controller = UserControl()
    controller.connect()

    metrics1 = await run_mission("missions/square_path.json", controller)
    print("Run 1:", metrics1)

    # Soft reset: drone back to spawn, same run number, same log files
    controller.resetDrone()

    metrics2 = await run_mission("missions/square_path.json", controller)
    print("Run 2:", metrics2)

    controller.close()

asyncio.run(main())
```

> **Note:** With Option B, both runs share the same `runNumber` and append to the same
> CSV log files. If run 1 had a collision, `metrics2["collisions"]` will also be `1`.
> Use Option A if clean per-run collision state is required.

---

## Common Issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Drone not at spawn on second run | `resetDrone()` not called between runs | Call `resetDrone()` before the second `run_mission()` |
| Run number not incrementing | `close()` not called at end of session | Always call `close()` to finalize a session |
| `collisions: 1` on second run despite no crash | `self.collision` flag not reset | Use Option A (full restart) to get a clean collision state |
| Log files missing for a run | `connect()` not called before `run_mission()` | Always call `connect()` before running a mission |
