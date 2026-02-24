# Week 2 Stories
Defenition of Done for Week 2: 
- Simulatior runs on golden machines, when following setup instructions.
- Python script examples/01_connect_read_pose.py reads telemetry data
- A new folder exists under `/runs/W02/<run_id>/` containing `run.json` and `telemetry.csv`
-  the telemetry.csv includes columns: t_s, x_m, y_m, z_m, roll_deg, pitch_deg, yaw_deg (roll/pitch may be 0.0 for now).
    - T_s => Time: What time stamp the telemetry data was taken
    - X_m => Drone postion in the x axis Foward/Backwards or North/South
    - Y_m => Drone Postion in the Y axis left/Right or West/East
    - Z_m => Drone postion in the z axos Up/Down
    - Roll_deg => Rotation around the x axis
    - Pitch_deg => Rotation around the y axis
    - Yaw_deg => Rotation around the z axis

### Notes
- There was no rotation of rolls for this second "Week" of work. We wanted to recover from the chaotic first week where little was accomplished. It seemed best to start the rotation on week 3.

- Due to difficulties with the microsoft airsim SDK we may need to create our own solution.

## Story 1
Task: Update Start guide
- Verify the start guide with golden machine and that the instructions are clear and work without any guess work from the user from a fresh install.

Owner: R2 - @MunachimsoAni 

Finished Criteria: Following the Start guide the Project can be set up and run on the golden machine.

Evidence: BUID_STATUS.MD contains instructions and can be followed.

## Story 2
Task: Implement a connect message and get_state message.
- messages are sent between Unreal to the Python SDK.
- Connect Message begins the connection between Script and Unreal
- get_state message sends telemetry data to a the sdk.
- update docs/Sim_INTERFACE.md and docs/PROTOCOL.md with new messages that record behavior.


Owner: R4 @Itzmesuccess 

Finished Criteria:
- Unreal is able to send data to telemetry.csv when the connection is run.

Evidence: Connecte messages retunr ACK or a clear error.
- ACK => acknowledge/understanding message

## Story 3
Task: IMplementing drone.pair() and Done.close() as well as loop that writes to the telemetry.csv.

Owner: R5 @sopuru-ani

Finished Criteria: 
- Using the Drone.pair() commands connects python SDK to Unreal drone object
- While is paired paired the python script is able to record telemetry data into the csv
    - The telemetry.csv should be a created new for each run.
    - The instruction: Every demo run automatically creates `/runs/W02/<run_id>/run.json` and telemetry.csv.
- Drone.close() ends connection and recording to the teleetry.csv

Evidence: examples/01_connect_read_pose.py that when run runs both commands and preforms actions.

## Story 4
Task: Integration Check

Owner: R1 @NburtonII

Finished Criteria: intregration test has run and causes no issues with the system. 
 - integration test = mide-week test: start Sim -> run the demo -> verify Logs

Evidence: docs/sprints/wo2/integration_check.md records pass and fails.

# Submission list for Week 2: 
1. docs/PROTOCOL.md (updated to match implemented messages)
2. docs/SIM_INTERFACE.md (host/port + how to start sim + notes if known)
3. docs/sprints/W02/plan.md + review.md + retro.md + integration_check.md
4. docs/presentations/W02.pdf (or W02.pptx)
5. examples/01_connect_read_pose.py
6. A run folder under runs/W02/<run_id>/ containing run.json + telemetry.csv
7.  sdk/tests/test_connect_mock.py