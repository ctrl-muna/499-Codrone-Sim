# Sensors — Range Sensor Specification

**Version:** 1.0
**Week:** 6
**Owner:** R5 – Python SDK, QA & Documentation Engineer

---

## Overview

Week 6 adds two distance sensors to the drone and a Python SDK module
(`sdk/client/range_sensor.py`) that exposes them as simple async functions.

---

## Sensor Hardware Configuration

Sensors are declared in:

```
sdk/client/sim_config/robot_quadrotor_fastphysics.jsonc
```

### FrontRange

| Field          | Value              |
|----------------|--------------------|
| `id`           | `FrontRange`       |
| `type`         | `distance-sensor`  |
| `enabled`      | `true`             |
| `parent-link`  | `Frame`            |
| `max-distance` | 50.0 m             |
| `min-distance` | 0.2 m              |
| `origin xyz`   | `0.1 0 0`          |
| `origin rpy`   | `0 0 0` (forward)  |

### BottomRange

| Field          | Value                 |
|----------------|-----------------------|
| `id`           | `BottomRange`         |
| `type`         | `distance-sensor`     |
| `enabled`      | `true`                |
| `parent-link`  | `Frame`               |
| `max-distance` | 20.0 m                |
| `min-distance` | 0.2 m                 |
| `origin xyz`   | `0 0 0`               |
| `origin rpy`   | `0 -90 0` (downward)  |

---

## Python SDK API

Module: `sdk/client/range_sensor.py`

```python
async def get_front_range(controller, timeout_s=1.0) -> float | None
async def get_bottom_range(controller, timeout_s=1.0) -> float | None
```

Both functions:
- Require a **connected** `UserControl` instance.
- Subscribe to the relevant distance-sensor topic on the drone.
- Poll every 50 ms until a reading arrives or `timeout_s` elapses.
- Return the distance in **metres**, or `None` on timeout.

To convert to centimetres: `distance_m * 100`.

### Usage example

```python
import asyncio
import sys, os
sys.path.insert(0, "sdk/client")

from UserControl import UserControl
from range_sensor import get_front_range, get_bottom_range

async def demo():
    controller = UserControl()
    controller.connect()
    try:
        await controller.commandParse("Takeoff", 0)

        front_m = await get_front_range(controller, timeout_s=1.0)
        bottom_m = await get_bottom_range(controller, timeout_s=1.0)

        print(f"Front  range: {front_m * 100:.1f} cm" if front_m else "Front: no reading")
        print(f"Bottom range: {bottom_m * 100:.1f} cm" if bottom_m else "Bottom: no reading")

        await controller.commandParse("Land", 0)
    finally:
        controller.close()

asyncio.run(demo())
```

---

## Sensor Topic Names

The projectairsim SDK registers topics by sensor ID. After the robot config is
loaded, the topics are available as:

```python
controller.drone.sensors["FrontRange"]["distance_sensor"]
controller.drone.sensors["BottomRange"]["distance_sensor"]
```

The `distance_sensor` payload contains at minimum a `"distance"` key (float, metres).

---

## Integration with Telemetry

When range readings are collected during `statePoll()`, they are written to the
telemetry CSV as two additional columns:

| Column           | Type  | Unit | Notes                              |
|------------------|-------|------|------------------------------------|
| `front_range_cm` | float | cm   | `None` written as empty string     |
| `bottom_range_cm`| float | cm   | `None` written as empty string     |

See `docs/LOG_SCHEMA.md` for the full telemetry CSV column schema.

---

## Integration with Metrics

`min_front_range_cm` is added to `runs/Run_{N}_metrics.json` starting Week 6.
See `docs/METRICS_SPEC.md` for the full metrics schema.

---

## Limitations

- **No timeout retry:** if a reading is missed, `None` is returned rather than retrying.
- **Single reading per call:** each `get_front_range()` call returns the first reading
  that arrives after the subscription is set up; it does not track a running minimum.
  Tracking the minimum over a full mission is handled in `mission_runner.py`.
- **Sensor reset:** the subscription is created fresh on each call. No persistent
  subscription is maintained between calls.
