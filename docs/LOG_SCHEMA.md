# Log Schema

**Version:** 1.1 (Week 6)
**Owner:** R5 – Python SDK, QA & Documentation Engineer

---

## Overview

Each run produces two log files written by `UserControl` during `statePoll()`:

```
runs/
  RunCommands/Run_{N}_Commands.csv    <- one row per command issued
  RunTelemetry/Run_{N}_Telemetry.csv  <- one row per second of flight
```

`N` is the run number read from `runs/Startup.json` at connect time.

---

## Commands CSV — `Run_{N}_Commands.csv`

Written by `UserControl.save_Command(command, duration)`.

### Columns

| Position | Name       | Type   | Example                         |
|----------|------------|--------|---------------------------------|
| 1        | `timestamp`| string | `Fri Mar 27 00:00:00 2026`      |
| 2        | `command`  | string | `Forward`                       |
| 3        | `duration` | int    | `2`                             |

No header row is written. Rows are appended in execution order.

---

## Telemetry CSV — `Run_{N}_Telemetry.csv`

Written by `UserControl.save_Telemetry(telemetry_data)` once per second inside
`statePoll()`.

### Week 5 Schema (columns 1–9)

| Position | Name        | Type   | Unit    | Description                        |
|----------|-------------|--------|---------|------------------------------------|
| 1        | `timestamp` | string | —       | `time.asctime()` wall-clock string |
| 2        | `x`         | float  | m       | North position (NED)               |
| 3        | `y`         | float  | m       | East position (NED)                |
| 4        | `z`         | float  | m       | Down position (NED, negative = up) |
| 5        | `w`         | float  | —       | Quaternion w                       |
| 6        | `orient_x`  | float  | —       | Quaternion x                       |
| 7        | `orient_y`  | float  | —       | Quaternion y                       |
| 8        | `orient_z`  | float  | —       | Quaternion z                       |
| 9        | `collision` | bool   | —       | `True` if collision flag is set    |

No header row is written. Values are comma-separated. Rows are appended once
per second while any command is executing.

### Week 6 Additions (columns 10–11)

| Position | Name             | Type        | Unit | Description                                  |
|----------|------------------|-------------|------|----------------------------------------------|
| 10       | `front_range_cm` | float or `` | cm   | FrontRange reading; empty string if no data  |
| 11       | `bottom_range_cm`| float or `` | cm   | BottomRange reading; empty string if no data |

A missing reading (sensor timeout) is written as an empty field, not `None` or `null`,
to keep the CSV parseable by standard tools.

---

## Implementation Notes

- **No CSV header row** is written in the current implementation. Column positions
  are fixed by the write order in `UserControl.save_Telemetry()`.
- **`z` is NED down**, so a drone hovering at 5 m altitude will have `z ≈ -5.0`.
- **`collision`** reflects `UserControl.self.collision` at the moment the row is
  written. Once `True`, it stays `True` for the rest of the session (the flag is
  never reset within a session).
- Week 6 range columns are populated by `range_sensor.get_front_range()` and
  `range_sensor.get_bottom_range()` called during `statePoll()`. If either returns
  `None`, the corresponding column is written as an empty string.

---

## Planned Additions

| Column         | Planned week | Description                         |
|----------------|--------------|-------------------------------------|
| CSV header row | Week 7+      | Optional header for tooling support |
