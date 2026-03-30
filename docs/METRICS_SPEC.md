# Metrics Specification

**Version:** 1.0
**Week:** 5
**Owner:** R5 – Python SDK, QA & Documentation Engineer

---

## Overview

After each mission run, `run_mission()` in `sdk/client/mission_runner.py` automatically
writes a `metrics.json` file capturing the outcome of the run.

---

## File Location

Metrics files follow the existing run-numbering convention in `runs/`:

```
runs/
  Startup.json                       <- current run counter  {"RunNumber": N}
  RunCommands/Run_{N}_Commands.csv   <- command log for run N
  RunTelemetry/Run_{N}_Telemetry.csv <- telemetry log for run N
  Run_{N}_metrics.json               <- mission metrics for run N  (Week 5+)
```

`N` is read from `runs/Startup.json` at connect time and incremented by `controller.close()`.

---

## Week 5 Schema (minimum required fields)

```json
{
  "success": true,
  "completion_time_s": 12.4,
  "collisions": 0,
  "failure_reason": null
}
```

### Field definitions

| Field              | Type           | Required | Description                                                    |
|--------------------|----------------|----------|----------------------------------------------------------------|
| `success`          | bool           | **Yes**  | `true` if all steps completed without collision or exception   |
| `completion_time_s`| float (>= 0)   | **Yes**  | Wall-clock seconds from first step start to last step end     |
| `collisions`       | int (0 or 1)   | **Yes**  | `1` if a collision was detected during the mission, else `0`  |
| `failure_reason`   | string or null | No       | Human-readable reason when `success` is `false`; null on pass |

---

## Implementation Notes

- **`collisions` is 0 or 1**, not a running count. The underlying
  `UserControl._on_collision()` sets a boolean flag (`self.collision`), not a counter.
  Multi-collision counting is planned for a future week.

- **`completion_time_s`** is Python-side wall-clock time. It includes both command
  execution time and time waiting for the simulator to respond.

- **`failure_reason`** is set to `"collision"` if a collision terminates the mission
  early, or to the exception message string if a Python exception is raised.
  It is `null` on a successful run.

- The `collision` flag is **not reset** by `resetDrone()` in the current implementation.
  To get a clean `collisions: 0` on a repeat run, start a new session via `close()` +
  reconnect. See `docs/RESET_PROCESS.md`.

---

## Planned Additions (future weeks)

| Field               | Planned week | Description                                 |
|---------------------|--------------|---------------------------------------------|
| structured failure codes | Week 10 | e.g. `collision`, `out_of_bounds`, `timeout`|

---

## Week 6 Schema (full fields)

```json
{
  "success": true,
  "completion_time_s": 12.4,
  "collisions": 0,
  "failure_reason": null,
  "min_front_range_cm": 180.0
}
```

### New Week 6 field

| Field               | Type              | Required | Description                                                         |
|---------------------|-------------------|----------|---------------------------------------------------------------------|
| `min_front_range_cm`| float (>= 0) or null | No   | Minimum FrontRange reading in cm during the run; null if no readings collected |

- **`min_front_range_cm`** is `null` if `get_front_range()` returned `None` for every
  poll during the mission (e.g. sensor not connected, or very short mission with no
  statePoll cycles).
- Values are in **centimetres** (metres × 100) to match telemetry column units.

---

## Validation

`tests/test_metrics_schema_min.py` provides unit tests that validate any metrics dict
against the Week 5 minimum schema without requiring a simulator connection.

`tests/test_range_columns_present.py` provides unit tests that validate the Week 6
metrics fields and telemetry columns.

Run with:

```bash
pytest tests/test_metrics_schema_min.py
pytest tests/test_range_columns_present.py
```
