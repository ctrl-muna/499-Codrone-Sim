# Week 4: M1.1 – Movement + Collision Events

## Objective

Movement primitives work reliably and collisions are detectable and logged.  
Students can run a square path demo.

---

## Required Demo

`examples/03_square_path.py`  
Owner: R5 @MunachimsoAni

---

## Required Documents / Artifacts

- `docs/COMMANDS_SPEC.md` v1  
  Owner: R4 @NburtonII

- `docs/Sprints/W04/*`  
  Owner: R1 @Aalbana20

- `docs/presentations/W04.pptx`  
  Owner: R1 @Aalbana20

---

## Minimum Tests Required This Week

- `test_square_path_sequence.py`  
  Owner: R5 @MunachimsoAni

---

## Telemetry Requirements

Minimum fields expected:

- Week 3 telemetry columns
- `collided` (boolean)
- optional `vx`
- optional `vy`
- optional `vz`

Owner: R4 @NburtonII

---

# Role Checklists (Deliverables)

## R1 – Sprint Lead & Integrator

Owner: @Aalbana20

- [ ] Update `demo_current.py` to run the square path demo
- [ ] Define what counts as a **collision**
- [ ] Ensure collision events appear in `events.csv`
- [ ] Coordinate Week 4 sprint planning
- [ ] Run integration check and document results

---

## R2 – Build & Release Engineer

Owner: @itzmesuccess

- [ ] Ensure build/deploy still works after movement changes
- [ ] Update `BUILD_STATUS.md`
- [ ] Document any configuration needed to enable collision reporting

---

## R3 – 3D World & UX Engineer

Owner: @sopuru-ani

- [ ] Add a wall or obstacle
- [ ] Add a clear boundary
- [ ] Add a floor grid for motion visibility
- [ ] Ensure spawn point is not too close to walls

---

## R4 – Simulator API & Networking Engineer

Owner: @NburtonII

- [ ] Implement movement commands on simulator side
- [ ] Enforce max speed
- [ ] Enforce altitude limits
- [ ] Expose collision flag/event
- [ ] Implement reset behavior for collision state

---

## R5 – Python SDK, QA & Documentation Engineer

Owner: @MunachimsoAni

- [ ] Implement `move_forward`, `move_back`, `move_left`, `move_right`
- [ ] Implement `turn_left`, `turn_right`
- [ ] Make movement commands blocking with timeouts
- [ ] Create square path lab script with progress printouts
- [ ] Log `events.csv` entries for collisions and timeouts

---

# Story Breakdown

## Story 1

Task: Sprint planning and integration coordination for Week 4

Owner: R1 @Aalbana20  
Finished Criteria: Week 4 sprint plan is documented and all owners are assigned  
Evidence: `docs/Sprints/W04/PLAN.md`

---

## Story 2

Task: Update demo workflow to use square path demo and define collision behavior

Owner: R1 @Aalbana20  
Finished Criteria: `demo_current.py` points to square path demo and collision definition is documented  
Evidence: updated demo script and integration notes

---

## Story 3

Task: Verify build and deployment workflow after movement changes

Owner: R2 @itzmesuccess  
Finished Criteria: Build still runs successfully and build status is updated  
Evidence: `docs/BUILD_STATUS.md`

---

## Story 4

Task: Document collision-reporting configuration for build/runtime

Owner: R2 @itzmesuccess  
Finished Criteria: Any required settings for collision reporting are documented  
Evidence: `docs/BUILD_STATUS.md`

---

## Story 5

Task: Update world with obstacle, boundary, and floor grid

Owner: R3 @sopuru-ani  
Finished Criteria: Scene shows obstacle, visible boundary, and floor grid  
Evidence: screenshot/video of updated scene

---

## Story 6

Task: Adjust spawn point for safe movement testing

Owner: R3 @sopuru-ani  
Finished Criteria: Spawn point allows square path demo without immediate wall collision  
Evidence: screenshot/video of spawn location

---

## Story 7

Task: Implement simulator-side movement commands and safety constraints

Owner: R4 @NburtonII  
Finished Criteria: Movement commands execute with speed and altitude enforcement  
Evidence: simulator-side test / console output

---

## Story 8

Task: Expose collision events and reset behavior

Owner: R4 @NburtonII  
Finished Criteria: Collision flag/event is generated and resets correctly on start/reset  
Evidence: collision event logs / simulator output

---

## Story 9

Task: Implement Python movement commands and square path script

Owner: R5 @MunachimsoAni  
Finished Criteria: Square path script runs movement sequence successfully  
Evidence: `examples/03_square_path.py`

---

## Story 10

Task: Log collision and timeout events to `events.csv`

Owner: R5 @MunachimsoAni  
Finished Criteria: `events.csv` records collisions and timeouts during demo/test runs  
Evidence: generated `events.csv`

---

# Common Pitfalls and Quick Fixes

- Movement that depends on frame rate  
  → Use fixed timestep or time-based integration

- Commands that never return  
  → Always enforce timeouts and safe fallbacks
