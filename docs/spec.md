<!-- req projection: generator=req render | rules_v=9 | selection=none | claims=133 | identity=sha256:0c862beca0719a270eb1966858a28b7c721e174004302a2c965bce3670fa7a10 -->
# Selection: (no context: nothing is decided by the caller)
applies 133, undecided 2, outside the selection 0 (an undecided claim is never reported as excluded)

## Applies (133)
- REQ-0002  1e0649c34f67  UNSTRUCTURED  Control algorithm robust against uncertainties of the brake dynamics model and disturbances. Performance maintained under friction coefficient variations (µ=0.2 to µ=1.0).
    selector: (none — applies to every variant)
    -> derives_from REQ-0080
    -> derives_from REQ-0081
- REQ-0003  639fca267587  UNSTRUCTURED  Fail-operational design of brake controller. Independent brake circuits with separate power supplies. Each circuit capable of achieving minimum 0.3g deceleration.
    selector: (none — applies to every variant)
    -> derives_from REQ-0080
    -> derives_from REQ-0081
- REQ-0004  dad561538f95  UNSTRUCTURED  Monitoring of operational state of brake controller and process and report to superordinate controller. Status reported every 10ms with fault detection <100ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0080
    -> derives_from REQ-0081
- REQ-0005  09467d92f5ea  SHALL  Brake controller must recognize brakes operating beyond design limits and react appropriately. Maximum pressure, temperature, duty cycle monitoring with protective actions.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0080
    -> derives_from REQ-0081
- REQ-0006  9013caa7faf7  UNSTRUCTURED  Monitoring of electrical and mechanical brake components with reporting to VDC. Pad wear, fluid level, actuator health, sensor status monitored continuously.
    selector: (none — applies to every variant)
    -> derives_from REQ-0080
    -> derives_from REQ-0081
- REQ-0007  c047b29fe82d  UNSTRUCTURED  Control algorithm robust against uncertainties of the drive dynamics model and disturbances. Torque control accuracy ±5% under all conditions.
    selector: (none — applies to every variant)
    -> derives_from REQ-0078
    -> derives_from REQ-0079
- REQ-0008  49918fe80762  SHALL  Sufficiently precise and validated drive dynamics model. Process variables must comply with the physical process state. Model verified across full speed and torque range.
    selector: (none — applies to every variant)
    -> derives_from REQ-0078
    -> derives_from REQ-0079
- REQ-0009  4c755a869a95  UNSTRUCTURED  Fail-operational design of drive controller. Graceful degradation to limp-home mode with minimum 20% torque capability maintained.
    selector: (none — applies to every variant)
    -> derives_from REQ-0078
    -> derives_from REQ-0079
- REQ-0010  2797894fa63b  UNSTRUCTURED  Monitoring of electrical/mechanical drive components and report to WRDC. Motor temperature, inverter status, gear health monitored at 50Hz.
    selector: (none — applies to every variant)
    -> derives_from REQ-0072
    -> derives_from REQ-0073
    -> derives_from REQ-0078
    -> derives_from REQ-0079
- REQ-0011  573a037762c7  SHALL  Drive controller must recognize drive operating beyond design limits and react appropriately. Overspeed, overcurrent, overtemperature protection active.
    selector: (none — applies to every variant)
    -> derives_from REQ-0078
    -> derives_from REQ-0079
- REQ-0012  f96be1110219  UNSTRUCTURED  Continuous and sufficient power supply for all safety-critical actuators. Redundant power sources with automatic failover. Minimum hold-up time: 500ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0078
    -> derives_from REQ-0079
    -> derives_from REQ-0080
    -> derives_from REQ-0081
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0013  a41e8ab0256c  UNSTRUCTURED  Continuous and sufficient power supply for VDC and WRDC. Independent power domains with galvanic isolation. Voltage monitoring and brown-out protection.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
- REQ-0014  9c6e6c2513e0  SHALL  Control actions of the vehicle dynamics controller must target the same vehicle motion. Coordination logic prevents conflicting brake/drive commands. Maximum conflict resolution time: 10ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0015  501439f6e9ce  UNSTRUCTURED  Exclusion of drive and brake actuation with conflicting targets. Hardware interlocks prevent simultaneous brake and drive application >10% torque.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
- REQ-0016  e3347f5d22d8  UNSTRUCTURED  Control algorithm must be robust against uncertainties of the steering dynamics model and disturbances. Algorithm shall maintain stability and performance under model parameter variations of ±20%.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0017  e1b85c4b19b3  SHALL  Sufficiently precise and validated steering dynamics model. Model accuracy shall be verified through physical testing with maximum error <5% across the operational envelope.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0018  26ffdc51b1bd  SHALL-NOT  Fail-operational design of steering controller. Single-point failures shall not cause loss of steering control. Redundant execution paths required.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0019  c77b6d3d093b  SHALL  Operation must be provided in required cycle time and jitter. Control loop execution time: 10ms ± 1ms. Maximum jitter: 500µs.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0020  7dd2c173de88  UNSTRUCTURED  Electrical and mechanical design according to state of the art. Components shall meet automotive standards (ISO 26262, ISO 16750).
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0021  2e0fd98f9053  UNSTRUCTURED  Monitoring of electrical and mechanical components and report to superordinate controller. Motor current, temperature, position sensor health monitored at 100Hz.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0022  f8b5dda6950c  SHALL  Inadequate or missing feedback must be recognized and compensated for. Sensor plausibility checks with redundant measurements. Timeout detection: 50ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0023  fc7e8993a1eb  UNSTRUCTURED  Continuous and sufficient power supply for steering-internal sensors. Redundant power supply with automatic switchover <10ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0024  e4a3cdddbee4  UNSTRUCTURED  Sufficient measurement accuracy for steering operation. Position accuracy: ±0.5°, velocity accuracy: ±1°/s.
    selector: (none — applies to every variant)
    -> derives_from REQ-0082
    -> derives_from REQ-0083
    -> derives_from REQ-0084
    -> derives_from REQ-0085
- REQ-0025  cd5c6e70761d  UNSTRUCTURED  Control algorithm robust against uncertainties of the vehicle dynamics model and disturbances. Trajectory tracking error <0.5m at speeds up to 130 km/h.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0026  97aba263b9a6  SHALL  Sufficiently precise and validated vehicle dynamics model. Process variables must comply with the physical process state. Model validated through hardware-in-the-loop testing.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0027  973fe78615ec  UNSTRUCTURED  Fail-operational design of vehicle dynamics controller. Dual-redundant processing with diverse algorithms. Cross-checking every cycle.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0028  2e9c47d747a0  UNSTRUCTURED  Fault-tolerant vehicle dynamics control algorithm capable of handling degraded actuation (e.g., loss of one steering actuator or brake circuit).
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0029  15eb47b4f64a  SHALL  Inadequate or missing feedback must be recognized. Sensor fusion from multiple sources (IMU, wheel speeds, GNSS). Fault detection within 100ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0030  07a1468942c3  UNSTRUCTURED  Sufficient measurement accuracy for vehicle dynamics control. Lateral acceleration: ±0.1 m/s², yaw rate: ±0.5°/s, velocity: ±0.1 m/s.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0031  0fe5c3bfe552  UNSTRUCTURED  Updated feedback available in required cycle time and jitter. Sensor data age <10ms, synchronized across all sensors with <1ms skew.
    selector: (none — applies to every variant)
    -> derives_from REQ-0066
    -> derives_from REQ-0067
    -> derives_from REQ-0068
    -> derives_from REQ-0069
- REQ-0032  91273e24a19f  SHALL  Inadequate or missing wheel speed feedback must be recognized and compensated. Redundant sensing per wheel with plausibility checking against vehicle sensors.
    selector: (none — applies to every variant)
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0033  dd2a547f776d  UNSTRUCTURED  Continuous and sufficient power supply for wheel motion sensors. Battery-backed power during transients. Voltage regulation ±5%.
    selector: (none — applies to every variant)
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0034  233962c71350  SHALL  Fault-tolerant wheel rotational dynamics control algorithm. Algorithm shall detect and compensate for single wheel actuator failures while maintaining vehicle stability.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0035  4b569181d65f  UNSTRUCTURED  Fail-operational design of wheel rotational dynamics controller. Redundant processing elements with cross-monitoring. Switchover time <20ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0036  434da8bfbf6c  UNSTRUCTURED  Sufficiently precise and validated wheel rotational dynamics model. Tire friction estimation accuracy ±10% across all surface conditions.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0037  d2b46d57181f  SHALL  Operation must be provided in required cycle time and jitter. Control loop: 5ms ± 0.5ms. Anti-lock/anti-spin response time <20ms.
    selector: (none — applies to every variant)
    -> derives_from REQ-0070
    -> derives_from REQ-0071
    -> derives_from REQ-0072
    -> derives_from REQ-0073
    -> derives_from REQ-0074
    -> derives_from REQ-0075
    -> derives_from REQ-0076
    -> derives_from REQ-0077
- REQ-0038  2a8777bd1a55  UNSTRUCTURED  The system shall detect lane markings and provide corrective steering input to keep the vehicle within the lane.
    selector: (none — applies to every variant)
- REQ-0039  78b46f3db083  SHALL  The system shall automatically adjust the vehicle's speed to maintain a safe distance from the vehicle ahead.
    selector: (none — applies to every variant)
- REQ-0040  cabbae9bbf63  SHALL  The system shall detect potential collisions and apply the brakes autonomously to avoid or mitigate the impact.
    selector: (none — applies to every variant)
- REQ-0041  1749fafc54f2  SHALL  The system shall identify pedestrians in the vehicle's path and issue warnings or initiate braking to prevent collisions.
    selector: (none — applies to every variant)
- REQ-0042  8b8754ab048b  SHALL  The system shall recognize traffic signs, with a focus on posted speed limits, so that downstream driving assistance functions can react appropriately.
    selector: (none — applies to every variant)
- REQ-0043  9f31e333d0f5  SHALL  The system shall monitor zones to the rear and sides of the vehicle that are not directly visible to the driver, and warn the driver when another road user enters those zones while a lane change is intended.
    selector: (none — applies to every variant)
- REQ-0044  790cf3ba68d4  SHALL  The system shall observe driver state via the cabin camera and warn the driver, and optionally suggest a break, when sustained signs of drowsiness or inattention are detected.
    selector: (none — applies to every variant)
- REQ-0045  6b06c1d441e2  SHALL  The system shall identify suitable parallel and perpendicular parking slots and semi-autonomously steer, accelerate, and brake the vehicle into the selected slot under driver supervision.
    selector: (none — applies to every variant)
- REQ-0046  b5acd580c428  SHALL  The lane detection software shall process camera input and accurately identify lane markings under various lighting conditions.
    selector: (none — applies to every variant)
    -> links REQ-0038
- REQ-0047  7d7131c09d5d  UNSTRUCTURED  The steering control software shall provide smooth and precise steering corrections based on detected lane positions.
    selector: (none — applies to every variant)
    -> links REQ-0038
- REQ-0048  91cb60a6cef3  SHALL  The distance measurement software shall measure the distance to the vehicle ahead using radar or LiDAR sensors for adaptive cruise control.
    selector: (none — applies to every variant)
    -> links REQ-0039
- REQ-0049  75cbf03262b2  SHALL  The speed control software shall adjust vehicle speed dynamically while maintaining a safe following distance.
    selector: (none — applies to every variant)
    -> links REQ-0039
- REQ-0050  93743f3bf58b  SHALL  The collision detection software shall identify potential collisions using sensor data and predict the time-to-impact.
    selector: (none — applies to every variant)
    -> links REQ-0040
- REQ-0051  cb9fcb750b72  SHALL  The autonomous braking software shall apply the brakes autonomously when a collision is imminent, based on predictions from the collision detection module.
    selector: (none — applies to every variant)
    -> links REQ-0040
- REQ-0052  b7fcdcb4211b  SHALL  The pedestrian detection software shall detect pedestrians in the vehicle's path using machine learning and sensor fusion.
    selector: (none — applies to every variant)
    -> links REQ-0041
- REQ-0053  fbb29dbbc345  SHALL  The alerting software shall issue audio or visual alerts when pedestrians are detected near the vehicle.
    selector: (none — applies to every variant)
    -> links REQ-0041
- REQ-0054  f37cab3bfe6b  SHALL  The emergency braking software shall initiate emergency braking when a pedestrian is in the collision path.
    selector: (none — applies to every variant)
    -> links REQ-0041
- REQ-0055  e35ec2f66a78  SHALL  The speed limit recognition software shall detect posted speed limit signs from camera input and provide the extracted limit to driver assistance functions.
    selector: (none — applies to every variant)
    -> links REQ-0042
- REQ-0056  57e1ef349217  SHALL  The blind spot detection software shall detect vehicles, motorcycles, and bicycles entering the blind spot zones using rear-corner radar sensors and side-view cameras.
    selector: (none — applies to every variant)
    -> links REQ-0043
- REQ-0057  5749e2a85dd3  SHALL  The blind spot warning software shall issue a driver warning when the turn signal is engaged toward a blind spot zone that is currently occupied by another road user.
    selector: (none — applies to every variant)
    -> links REQ-0043
- REQ-0058  2da62c743409  SHALL  The drowsiness monitoring software shall estimate driver eye-aspect ratio and gaze direction from the cabin camera at the cadence required for drowsiness scoring.
    selector: (none — applies to every variant)
    -> links REQ-0044
- REQ-0059  b0f2cf6ba6c5  SHALL  The drowsiness alerting software shall issue progressive driver alerts and propose a break when the drowsiness score exceeds the configured threshold for longer than the calibrated dwell time.
    selector: (none — applies to every variant)
    -> links REQ-0044
- REQ-0060  5f3e4afc1c3a  SHALL  The parking slot detection software shall detect parallel and perpendicular parking slots from ultrasonic distance sensors fused with the surround-view camera system.
    selector: (none — applies to every variant)
    -> links REQ-0045
- REQ-0061  7858dfe83413  UNSTRUCTURED  The parking control software shall plan a feasible park trajectory into the chosen slot and command steering, throttle, and braking actuators to follow it within configured speed and clearance bounds.
    selector: (none — applies to every variant)
    -> links REQ-0045
- REQ-0062  7ddf4ebe8eed  SHALL  The coffee machine shall be able to brew coffee with user-selected strength (weak, medium, strong).
    selector: (none — applies to every variant)
- REQ-0063  c13f8aa41cde  SHALL  The coffee machine shall heat water to the appropriate temperature (85-95°C) for brewing coffee.
    selector: (none — applies to every variant)
- REQ-0064  69959998bf08  SHALL  The coffee machine shall automatically shut down if the water temperature exceeds 100°C or if no water is detected.
    selector: (none — applies to every variant)
- REQ-0065  d19b92b17803  SHALL  The coffee machine shall provide a user interface with buttons for selecting coffee strength and starting the brewing process.
    selector: (none — applies to every variant)
- REQ-0066  ec64c7f0198e  SHALL  The Vehicle Dynamics Controller must set a new target wheel torque when required for safe trajectory following. Failure to provide necessary torque commands can result in trajectory deviation.
    selector: (none — applies to every variant)
- REQ-0067  231efee24405  SHALL  The Vehicle Dynamics Controller must set a new target wheel torque only when required. Unintended torque changes can cause unexpected vehicle behavior.
    selector: (none — applies to every variant)
- REQ-0068  1a1473d86027  SHALL  The Vehicle Dynamics Controller must set a new target steering angle when required for trajectory execution. Missing steering commands prevent proper path following.
    selector: (none — applies to every variant)
- REQ-0069  1d01b28157c3  SHALL  The Vehicle Dynamics Controller must set a new target steering angle only when required. Unintended steering changes are hazardous to vehicle control.
    selector: (none — applies to every variant)
- REQ-0070  c54496ed7f4c  SHALL  The Wheel Rotational Dynamics Controller must change target brake torque when required for proper vehicle speed control along the trajectory.
    selector: (none — applies to every variant)
- REQ-0071  f6febc50112f  SHALL  The Wheel Rotational Dynamics Controller must change target brake torque only when required. Unintended braking can cause trajectory deviation or collision.
    selector: (none — applies to every variant)
- REQ-0072  3258da6fc385  SHALL  The Wheel Rotational Dynamics Controller must change target drive torque when required for maintaining the planned velocity profile.
    selector: (none — applies to every variant)
- REQ-0073  450028835863  SHALL  The Wheel Rotational Dynamics Controller must change target drive torque only when required to prevent unintended acceleration or deceleration.
    selector: (none — applies to every variant)
- REQ-0074  43bb33e5803a  SHALL  Anti-lock control must be performed only when wheel lock is imminent. Unnecessary ABS activation can reduce braking efficiency and affect trajectory control.
    selector: (none — applies to every variant)
- REQ-0075  841fba423aa2  SHALL  Anti-lock control must be performed when required to prevent wheel lock during braking, maintaining vehicle controllability.
    selector: (none — applies to every variant)
- REQ-0076  2c1f0aa86428  SHALL  Anti-spin control must be performed only when wheel spin is detected. Unnecessary intervention can affect acceleration performance and trajectory execution.
    selector: (none — applies to every variant)
- REQ-0077  043aceec7ab9  SHALL  Anti-spin control must be performed when required to prevent excessive wheel spin during acceleration, ensuring stable trajectory following.
    selector: (none — applies to every variant)
- REQ-0078  f5b5912cdc78  SHALL  The Drive Controller must apply drive torque when required to execute the commanded velocity profile along the trajectory.
    selector: (none — applies to every variant)
- REQ-0079  df0b67b6c46e  SHALL  The Drive Controller must apply drive torque only when required. Unintended drive torque can cause dangerous acceleration.
    selector: (none — applies to every variant)
- REQ-0080  1bb497146259  SHALL  The Brake Controller must engage brake when required for deceleration or emergency stopping to prevent collision.
    selector: (none — applies to every variant)
- REQ-0081  38c2686ac206  SHALL  The Brake Controller must engage brake only when required. Unintended braking can cause loss of vehicle control or rear-end collisions.
    selector: (none — applies to every variant)
- REQ-0082  cfefff9da879  SHALL  The Steering Controller must change steering angle when required to follow the commanded path. Failure prevents proper trajectory execution.
    selector: (none — applies to every variant)
- REQ-0083  7d9a716fd2a9  SHALL  The Steering Controller must change steering angle only when required. Unintended steering changes are extremely hazardous.
    selector: (none — applies to every variant)
- REQ-0084  870848a9dc37  SHALL  The Steering Controller must hold steering angle when required to maintain straight-line travel or constant-radius turns.
    selector: (none — applies to every variant)
- REQ-0085  fb51d499274b  SHALL  The Steering Controller must hold steering angle only when required. Locked steering prevents necessary corrections and causes trajectory deviation.
    selector: (none — applies to every variant)
- REQ-0086  0e12c5dff297  SHALL  The lane detection software shall process camera inputs and accurately identify lane markings under various environmental conditions.
    selector: (none — applies to every variant)
    -> links REQ-0046
- REQ-0087  edb0acb9d93c  SHALL  The lane keeping software shall trigger a warning if the vehicle deviates from its lane without proper signaling.
    selector: (none — applies to every variant)
    -> links REQ-0047
- REQ-0088  bd2903932973  UNSTRUCTURED  The lane keeping software shall calculate and apply corrective steering actions to maintain the vehicle within the detected lane boundaries.
    selector: (none — applies to every variant)
    -> links REQ-0047
- REQ-0089  21b2964fe300  SHALL  The distance measurement software shall process radar inputs and measure the distance to objects ahead with high precision.
    selector: (none — applies to every variant)
    -> links REQ-0048
- REQ-0090  cad2b38f05f8  SHALL  The speed control software shall dynamically adjust the vehicle's speed based on distance measurements and the desired following distance.
    selector: (none — applies to every variant)
    -> links REQ-0049
- REQ-0091  d586db79de55  SHALL  The collision risk software shall estimate collision risk using real-time sensor data and predictive analytics.
    selector: (none — applies to every variant)
    -> links REQ-0050
- REQ-0092  e498d7fe1823  SHALL  The emergency braking software shall autonomously apply the brakes when a collision is imminent.
    selector: (none — applies to every variant)
    -> links REQ-0051
- REQ-0093  bf39fec3c3bc  SHALL  The pedestrian detection software shall detect pedestrians using sensor fusion techniques that combine camera, LiDAR, and radar data.
    selector: (none — applies to every variant)
    -> links REQ-0052
- REQ-0094  c999e8e84c29  SHALL  The alerting software shall issue audio and visual alerts when pedestrians are detected near the vehicle's path.
    selector: (none — applies to every variant)
    -> links REQ-0053
- REQ-0095  d321076dbe0d  SHALL  The emergency braking software shall apply emergency braking when a pedestrian is detected in the collision path.
    selector: (none — applies to every variant)
    -> links REQ-0054
- REQ-0096  02aee12483d2  SHALL  The dashboard software shall provide a visual representation of detected lane markings for driver awareness.
    selector: (none — applies to every variant)
    -> links REQ-0046
    -> links REQ-0086
- REQ-0097  6a23cf67e311  SHALL  The lane detection software shall adapt lane marking detection under challenging conditions, such as rain or fog.
    selector: (none — applies to every variant)
    -> links REQ-0046
- REQ-0098  9a616754a68e  SHALL  The speed control software shall adjust vehicle speed based on detected speed limits and road conditions.
    selector: (none — applies to every variant)
    -> links REQ-0049
- REQ-0099  8fb42db7a0d5  SHALL  The driver alert software shall create alerts when objects come within a critical distance.
    selector: (none — applies to every variant)
    -> links REQ-0048
- REQ-0100  32fb73df3a2a  SHALL  The object tracking software shall track multiple objects simultaneously and evaluate their threat level.
    selector: (none — applies to every variant)
    -> links REQ-0050
- REQ-0101  a81e9f39a709  SHALL  The emergency braking software shall optimize braking force during emergency stops to minimize impact risks.
    selector: (none — applies to every variant)
    -> links REQ-0051
- REQ-0102  d58716b6a5eb  SHALL  The pedestrian detection software shall use machine learning models to predict pedestrian movements and improve detection accuracy.
    selector: (none — applies to every variant)
    -> links REQ-0052
- REQ-0103  41835a0f80a4  SHALL  The alerting software shall combine audio, visual, and haptic alerts into a unified system for enhanced driver awareness.
    selector: (none — applies to every variant)
    -> links REQ-0053
- REQ-0104  6dbd88a17928  SHALL  The emergency braking software shall anticipate emergencies and initiate braking earlier to prevent accidents.
    selector: (none — applies to every variant)
    -> links REQ-0054
- REQ-0105  5569d390a1cd  SHALL  The pedestrian detection software shall identify crosswalks and prioritize pedestrian safety in such zones.
    selector: (none — applies to every variant)
    -> links REQ-0052
- REQ-0106  d8d1785cdd6f  SHALL  The speed limit recognition software shall detect speed limit signs in camera frames and publish the recognized limit.
    selector: (none — applies to every variant)
    -> links REQ-0055
- REQ-0107  88eb0d7a3713  SHALL  The blind spot detection software shall fuse rear-corner radar tracks and side-view camera detections into a single per-zone occupancy state with confidence scoring.
    selector: (none — applies to every variant)
    -> links REQ-0056
- REQ-0108  cd3b4cd2ae11  SHALL  The blind spot warning software shall activate the blind spot warning only when the turn signal points toward an occupied zone, suppressing nuisance alerts otherwise.
    selector: (none — applies to every variant)
    -> links REQ-0057
- REQ-0109  64ee24ce88b6  SHALL  The drowsiness monitoring software shall estimate per-frame eye-aspect ratio and gaze direction from cabin camera input under varying lighting conditions.
    selector: (none — applies to every variant)
    -> links REQ-0058
- REQ-0110  bb757a87c5cc  SHALL  The drowsiness monitoring software shall aggregate per-frame eye-state observations into a smoothed drowsiness score and emit progressive alerts when the score exceeds calibrated thresholds for the required dwell time.
    selector: (none — applies to every variant)
    -> links REQ-0059
- REQ-0111  7cd494f8f0d2  SHALL  The parking slot detection software shall recognize parallel and perpendicular parking slots from fused ultrasonic ranging and surround-view camera input and rank them by feasibility.
    selector: (none — applies to every variant)
    -> links REQ-0060
- REQ-0112  e20106543295  UNSTRUCTURED  The parking control software shall plan and follow a smooth park trajectory into the selected slot, respecting clearance margins, maximum speed, and steering rate limits, with abort behavior on detected obstacles.
    selector: (none — applies to every variant)
    -> links REQ-0061
- REQ-0114  5c67f1268ada  SHALL  The software shall process button inputs with debouncing and trigger appropriate actions (strength selection, start brewing, stop/cancel).
    selector: (none — applies to every variant)
    -> reqs REQ-0065
- REQ-0115  0482a6ed0499  SHALL  The software shall continuously monitor water temperature and trigger an emergency shutdown within 100ms if temperature exceeds 100°C to prevent boiling and potential hazards.
    selector: (none — applies to every variant)
    -> reqs REQ-0063
    -> reqs REQ-0064
- REQ-0116  bb661117882c  UNSTRUCTURED  The temperature control software shall monitor the water temperature sensor and regulate the heating element to maintain temperature between 85-95°C using PID control.
    selector: (none — applies to every variant)
    -> reqs REQ-0063
- REQ-0117  a2d88b0bc7e4  SHALL  The software shall continuously monitor the water level sensor and prevent brewing operations when water level is below minimum threshold.
    selector: (none — applies to every variant)
    -> reqs REQ-0064
- REQ-0118  a12db3376292  UNSTRUCTURED  The brake system shall implement X-split dual hydraulic circuits (FL-RR, FR-RL) with independent pressure generation and control. Each circuit shall be capable of achieving minimum 0.3g deceleration independently. Electronic control units are dual-redundant with independent power supplies.
    selector: (none — applies to every variant)
    -> implements REQ-0003
- REQ-0119  3aa37482d4ba  SHALL  The brake controller shall adapt pressure modulation strategy based on estimated surface friction coefficient across full range µ=0.2 (ice) to µ=1.0 (dry asphalt). Adaptation includes: brake force distribution, pressure ramp rates, and ABS threshold tuning. Transition time between friction regimes: <100ms.
    selector: (none — applies to every variant)
    -> implements REQ-0002
- REQ-0120  ca022cb4b682  SHALL  The brake system shall continuously monitor: brake pad wear (thickness sensors), hydraulic fluid level and pressure, brake disc temperature (IR sensors), actuator health (current, position feedback, response time). Monitoring cycle: 100ms. Fault detection and reporting to VDC within 200ms.
    selector: (none — applies to every variant)
    -> implements REQ-0006
- REQ-0121  83983d3db1ff  UNSTRUCTURED  The drive controller shall maintain torque control accuracy ±5% of commanded value across full speed-torque envelope: 0-200 km/h, -100% to +100% torque (regen to full power). Control bandwidth: 20Hz. Response time from command to 90% torque achievement: <150ms.
    selector: (none — applies to every variant)
    -> implements REQ-0007
- REQ-0122  191bd7ba5a5b  SHALL  The drive system shall implement fail-operational architecture with graceful degradation to limp-home mode upon component failure. Limp-home mode capabilities: minimum 20% of maximum torque, maximum speed 30 km/h, sufficient power to reach safe stopping location. Mode transition time: <500ms.
    selector: (none — applies to every variant)
    -> implements REQ-0009
- REQ-0123  cee2eba14ffc  UNSTRUCTURED  The drive controller shall implement protection systems: (1) Overspeed: limit at 210 km/h with soft cutoff; (2) Overcurrent: inverter current limit with 10µs response time; (3) Overtemperature: motor 180°C, inverter 125°C with thermal derating starting at 80% limits. All limits shall trigger safe state transition and fault reporting.
    selector: (none — applies to every variant)
    -> implements REQ-0011
- REQ-0124  903bed7fb18e  UNSTRUCTURED  The steering controller shall implement H-infinity robust control algorithm with guaranteed stability and performance under parameter variations of ±20% from nominal values. Parameters include: steering inertia, friction, assist motor torque constant, and rack geometry. Control bandwidth: 10Hz minimum.
    selector: (none — applies to every variant)
    -> implements REQ-0016
- REQ-0125  e9bf854733ba  UNSTRUCTURED  The steering system shall use physics-based dynamics model validated through physical testing with maximum modeling error <5% across operational envelope: steering angle ±540°, steering rate ±200°/s, vehicle speed 0-130 km/h, lateral acceleration ±8 m/s².
    selector: (none — applies to every variant)
    -> implements REQ-0017
- REQ-0126  e7f56dd9ead2  SHALL  The steering controller shall implement dual-channel architecture with independent power supplies, processors, and motor windings. Each channel capable of providing minimum 50% of maximum steering torque. Channels operate in active-active mode with continuous cross-monitoring. Switchover time <10ms.
    selector: (none — applies to every variant)
    -> implements REQ-0018
- REQ-0127  93d1817b255c  SHALL  The steering system shall provide redundant position and velocity feedback with specifications: position accuracy ±0.5° (absolute), velocity accuracy ±1°/s, update rate 1kHz, latency <1ms. Dual absolute encoders with diverse sensing principles (magnetic + optical).
    selector: (none — applies to every variant)
    -> implements REQ-0024
- REQ-0128  3211b9052e85  SHALL  The VDC shall track the commanded trajectory with maximum lateral error ≤0.5m and longitudinal error ≤0.3m at speeds up to 130 km/h under nominal conditions. Performance degradation allowed under adverse conditions (reduced visibility, low friction surfaces) with notification to supervision layer.
    selector: (none — applies to every variant)
    -> implements REQ-0025
- REQ-0129  3b82fcff5fdc  UNSTRUCTURED  The VDC shall implement dual-redundant processing with two independent processors executing diverse control algorithms. Cross-checking shall occur every control cycle (10ms) with automatic switchover to healthy processor within 20ms upon detection of discrepancy >10%.
    selector: (none — applies to every variant)
    -> implements REQ-0027
- REQ-0130  a47c6b762b00  UNSTRUCTURED  The VDC shall implement sensor fusion combining IMU (6-axis accelerometer/gyro), individual wheel speed sensors, and GNSS/INS using Extended Kalman Filter. System shall detect sensor failures within 100ms and maintain state estimation with degraded accuracy using remaining sensors.
    selector: (none — applies to every variant)
    -> implements REQ-0029
    -> implements REQ-0030
- REQ-0131  5c39698c7d54  SHALL  The VDC shall maintain trajectory control capability with single actuator or sensor failure. Degraded modes: (1) Single wheel actuator failure: redistribute torque to remaining wheels; (2) Steering actuator failure: trajectory control via differential braking; (3) Single sensor failure: continue with reduced accuracy.
    selector: (none — applies to every variant)
    -> implements REQ-0028
- REQ-0132  d31902810df7  UNSTRUCTURED  The WRDC shall compensate for failed wheel actuator through coordinated control of remaining three wheels. System shall detect actuator failure within 50ms (via feedback comparison) and redistribute target torques to maintain yaw stability within ±2° and lateral acceleration within ±0.5 m/s² of commanded values.
    selector: (none — applies to every variant)
    -> implements REQ-0034
- REQ-0133  4d7d1c97b029  UNSTRUCTURED  The WRDC shall implement real-time tire-road friction coefficient (µ) estimation with ±10% accuracy across all surface conditions (dry asphalt µ=1.0 to ice µ=0.2). Estimation algorithm shall use wheel slip ratio, longitudinal/lateral forces, and vehicle dynamics model. Update rate: 100Hz.
    selector: (none — applies to every variant)
    -> implements REQ-0036
- REQ-0134  610675f42b75  SHALL  The WRDC shall implement integrated anti-lock braking (ABS) and anti-slip regulation (ASR) with coordinated control logic. Wheel lock detection threshold: slip ratio >0.15. Wheel spin detection threshold: slip ratio >0.10. Control response time from detection to pressure modulation: <20ms.
    selector: (none — applies to every variant)
    -> implements REQ-0034
- REQ-0135  e92924de16eb  UNSTRUCTURED  The WRDC control loop shall execute with 5ms cycle time and maximum jitter ±0.5ms. Sensor data age shall not exceed 10ms. Anti-lock and anti-spin response time from wheel slip detection to first pressure modulation: <20ms.
    selector: (none — applies to every variant)
    -> implements REQ-0037

## Undecided (2)
- REQ-0113  8fea64370235  SHALL  The turn signal logic for left-hand drive vehicles shall prioritize right-side mirror checks for overtaking maneuvers.
    selector: steering_side == left
- REQ-0136  20e571917ac9  SHALL  The turn signal logic for right-hand drive vehicles shall prioritize left-side mirror checks for overtaking maneuvers.
    selector: steering_side == right

## Outside the selection (0)
(none)
