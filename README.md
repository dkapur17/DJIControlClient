# DJI Control Client

A Python Wrapper over the API Calls to the DJI Control Server.

### Classes

1. `DJIControlClient`: Main class with all control methods on it.
2. `VelocityProfile`: Enum for velocity profile with options `CONSTANT`, `TRAPEZOIDAL` and `S_CURVE`.
3. `ControlMode`: Enum for control mode with options `POSITION` and `VELOCITY`.

### Return Types

Following are the possible (non-primitive) return types from each method. Which of these is returned by the method can be found in the API reference:

1. `CommandCompleted`: A dictionary of the shape: `{completed: bool, errorDescription: Union[str|None]}`. Generally returned by methods that cause the drone to change state or perform an action. If `completed` is `True`, the action was completed successfully. In this case, `errorDescription` would be `None`. If `completed` is `False`, the action wasn't successfully executed, and the reason shows up as a string in `errorDescription`.

2. `VelocityCommand`: A dictionary of the shape `{velX: float, velY: float, velZ: float, yawRate: float}`. The X, Y and Z velocities are in $m/s$ and the Yaw rate is in $deg/s$.

3. `IMUState`: A dictionary of the shape `{velX: float, velY: float, velZ: float, roll: float, pitch: float, yaw: float}`. The X, Y and Z velocities are in $m/s$ and roll, pitch and yaw are in `degrees`.

### `DJIControlClient`:

* `DJIControlClient(ip: str, port: int)`: Takes server IP and Port as parameters and initiates connection. All subsequent methods must be called on the initiated instance.

* `takeOff()`: Sends takeoff signal to the drone. Returns a response **ONCE TAKEOFF IS INITIATED, NOT COMPLETED** (thus make sure to add a sufficient delay after the takeoff call before making any other calls). Returns a dict with completion status, and error message if any.

* `land()`: Sends land signal to the drone. Returns a response **ONCE LANDING IS INITIATED, NOT COMPLETED**` (thus make sure to add a sufficient delay after the landing call before making any other calls). If landing protection is enabled, this will cause the drone to descent to 0.3m off the ground and wait for user confirmation to completed landing. If landing protection is disabled, then it causes the drone to land immidiately.

* `confirmLanding()`: Sends landing confirmation to the drone. Returns a response **ONCE LANDING CONFIRMATION IS INITIATED, NOT COMPLETED** (thus make sure to add sufficient delay after the landing call before making any other calls). This to be called after calling `land()` only if landing protection is enabled.

* `getLandingProtectionState()`: Returns `True` if landing protection is enabled, `False` if it isn't and `CommandCompleted` with error description if it is unabled to fetch.

* `setLandingProtectionState(enabled: bool)`: `enabled=True` enables landing protection and `enabled=False` disables landing protection. Returns `CommandCompleted`.

* `getVelocityProfile()`: Returns `VelocityProfile.CONSTANT`, `VelocityProfile.TRAPEZOIDAL` or `VelocityProfile.S_CURVE` based on the value set on the server. Returns `CommandCompleted` in case of an error.

* `setVelocityProfile(profile: VelocityProfile)`: Sets the given velocity profile on the server. Returns `CommandCompleted`.

* `getControlMode()`: Returns `ControlMode.POSITION` or `ControlMode.VELOCITY` based on the value set on the server. Returns `CommandCompleted` in case of an error.

* `setControlMode(mode: ControlMode)`: Sets the given control mode on the server. Returns `CommandCompleted`.

* `getMaxSpeed()`: Returns the max speed set on the server in $m/s$ (used for positional control) as a float. Returns `CommandCompleted` in case of an error.

* `setMaxSpeed(speed: float)`: Sets the max speed on the server in $m/s$ (used for positional control) based on the given speed. Returns `CommandCompleted`.

* `getMaxAngularSpeed()`: Returns the max angular speed set on the server in $deg/s$ (used for positional control) as a float. Returns `CommandCompleted` in case of an error.

* `setMaxAnglularSpeed(speed: float)`: Sets the max angular speed on the server in $deg/s$ (used for positional control) based on the given speed. Returns `CommandCompleted`.

* `startVelocityControl()`: Starts a coroutine on the server that makes the drone continuously follow the currently set velocity command. *Can only be called in VELOCITY control mode*. Returns `CommandCompleted`.

* `setVelocityCommand(xVel: float, yVel: float, zVel: float, yawRate: float)`: Sets the current velocity command based on the input X, Y and Z velocities and Yaw Rate. *Can only be called after calling `startVelocityControl()` and when in VELOCITY control mode*. Returns `CommandCompleted`.

* `stopVelocityControl()`: Stops the coroutine on the server that makes the drone continuously follow the currently set velocity command. *Can only be called in VELCOITY control mode*. Returns `CommandCompleted`.

* `getCurrentVelocityCommand`: Returns the current velocity command that the drone is following if `startVelocityControl()` was already called, or will follow once `startVelocityControl()` is called, as `VelocityCommand`. Returns `CommandCompleted` in case of an error.

* `moveUp(distance: float)`: Makes the drone move up the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered.

* `moveDown(distance: float)`: Makes the drone move down the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered. **Careful while using this method, since there is no ground checking done if the distance > altitude of the drone**.

* `moveForward(distance: float)`: Makes the drone move forward the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered.

* `moveBackward(distance: float)`: Makes the drone move backward the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered.

* `moveLeft(distance: float)`: Makes the drone move left the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered.

* `moveRight(distance: float)`: Makes the drone move right the given distance in metres. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone covers the given distance, or an error is encountered.

* `rotateClockwise(angle: float)`: Makes the drone rotate clockwise the given angle in degrees. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone rotates the given angle, or an error is encountered.

* `rotateCounterClockwise(angle: float)`: Makes the drone rotate counter clockwise the given angle in degrees. *Can only be called in POSITION control mode*. Returns `CommandCompleted` either when the drone rotates the given angle, or an error is encountered.

* `startCollectingIMUState(interval: int)`: Starts a coroutine on the server that records the IMU state every `interval` milliseconds. Returns `CommandCompleted`.

* stopCollectingIMUState()`: Stops the coroutine on the server that records the IMU states. Returns `CommandCompleted`.

* `getCollectedIMUStates()`: Returns a list of `IMUState` collected between the calls to `startCollectingIMUState` and `stopCollectingIMUState`. Returns `CommandCompleted` in case of an error.

* `clearCollectedIMUStates()`: Clears the collected IMU states on the server.

* `getCurrentIMUState()`: Returns the current IMU states as `IMUState`. Returns `CommandCompleted` in case of an error.

* `getHeading()`: Returns the current heading from true north in degrees. Returns `CommandCompleted` in case of an error.