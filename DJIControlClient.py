from typing import Any, Dict, List, Union
import requests
from enum import Enum


class VelocityProfile(Enum):
    CONSTANT = 1
    TRAPEZOIDAL = 2
    S_CURVE = 3


class ControlMode(Enum):
    POSITION = 1
    VELOCITY = 2


class DJIControlClient:

    def __init__(self, ip: str, port: int) -> None:

        self.ip = ip
        self.port = port

        self.server_addr = f"http://{self.ip}:{self.port}"

        r = requests.get(url=self.server_addr)

        assert r.content == b"Connected"

    def makeReqAndReturnJSON(self, route: str) -> Dict[str, Any]:
        r = requests.get(url=f"{self.server_addr}{route}")
        return r.json()

    # Take off and Land
    def takeOff(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/takeoff')

    def land(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/land')

    def confirmLanding(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/confirmLanding')

    # Landing Protection

    def getLandingProtectionState(self) -> Union[bool, Dict[str, Any]]:
        landingProtectionState = self.makeReqAndReturnJSON(
            '/isLandingProtectionEnabled')
        if 'state' in landingProtectionState:
            return landingProtectionState['state']
        else:
            return landingProtectionState

    def setLandingProtectionState(self, enabled: bool) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/enableLandingProtection' if enabled else '/disableLandingProtection')

    # Velocity Profiles
    def getVelocityProfile(self) -> VelocityProfile:
        profileName = self.makeReqAndReturnJSON('/getVelocityProfile')

        if 'state' in profileName:
            if profileName == 'CONSTANT':
                return VelocityProfile.CONSTANT
            elif profileName == 'TRAPEZOIDAL':
                return VelocityProfile.TRAPEZOIDAL
            else:
                return VelocityProfile.S_CURVE
        else:
            return profileName

    def setVelocityProfile(self, profile: VelocityProfile) -> Dict[str, Any]:
        if profile == VelocityProfile.CONSTANT:
            profileName = 'CONSTANT'
        elif profile == VelocityProfile.TRAPEZOIDAL:
            profileName = 'TRAPEZOIDAL'
        elif profile == VelocityProfile.S_CURVE:
            profileName = 'S_CURVE'
        else:
            raise AssertionError(
                "Given profile isn't a valid Velocity Profile")
        return self.makeReqAndReturnJSON(f'/setVelocityProfile/{profileName}')

    # Control Mode
    def getControlMode(self) -> ControlMode:
        modeName = self.makeReqAndReturnJSON('/getControlMode')

        if 'state' in modeName:
            if modeName['state'] == 'POSITION':
                return ControlMode.POSITION
            else:
                return ControlMode.VELOCITY
        else:
            return modeName

    def setControlMode(self, mode: ControlMode) -> Dict[str, Any]:
        if mode == ControlMode.POSITION:
            modeName = "POSITION"
        elif mode == ControlMode.VELOCITY:
            modeName = "VELOCITY"
        else:
            raise AssertionError("Given mode isn't a valid Control Mode")

        return self.makeReqAndReturnJSON(f'/setControlMode/{modeName}')

    # Movement Speed

    def getMaxSpeed(self) -> Union[float, Dict[str, Any]]:
        movementSpeed = self.makeReqAndReturnJSON('/getMaxSpeed')

        if 'state' in movementSpeed:
            return movementSpeed['state']
        else:
            return movementSpeed

    def setMaxSpeed(self, speed: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/setMaxSpeed/{speed}')

    def getMaxAngularSpeed(self) -> Union[float, Dict[str, Any]]:
        movementSpeed = self.makeReqAndReturnJSON('/getMaxAngularSpeed')

        if 'state' in movementSpeed:
            return movementSpeed['state']
        else:
            return movementSpeed

    def setMaxAngularSpeed(self, speed: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/setMaxAngularSpeed/{speed}')

    # Velocity Control
    def startVelocityControl(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/startVelocityControl')

    def setVelocityCommand(self, xVel: float, yVel: float, zVel: float, yawRate: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/setVelocityCommand/{xVel}/{yVel}/{zVel}/{yawRate}')

    def stopVelocityControl(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/stopVelocityControl')

    def getCurrentVelocityCommand(self) -> Dict[str, Any]:
        velocityCommand = self.makeReqAndReturnJSON(
            '/getCurrentVelocityCommand')

        if 'state' in velocityCommand:
            return velocityCommand['state']
        else:
            return velocityCommand

    # Positon Control
    # Vertical Movement
    def moveUp(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveUp/{distance}')

    def moveDown(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveDown/{distance}')

    # Rotational Movement
    def rotateClockwise(self, angle: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/rotateClockwise/{angle}')

    def rotateCounterClockwise(self, angle: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/rotateCounterClockwise/{angle}')

    # Planar Movement
    def moveForward(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveForward/{distance}')

    def moveBackward(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveBackward/{distance}')

    def moveLeft(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveLeft/{distance}')

    def moveRight(self, distance: float) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/moveRight/{distance}')

    # IMU State
    def startCollectingIMUState(self, interval: int) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/startCollectingIMUState/{interval}')

    def stopCollectingIMUState(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/stopCollectingIMUState')

    def getCurrentIMUState(self) -> Dict[str, Any]:
        imuState = self.makeReqAndReturnJSON('/getCurrentIMUState')
        if 'state' in imuState:
            return imuState['state']
        else:
            return imuState

    def getCollectedIMUStates(self) -> Union[List[Dict[str, float]], Dict[str, Any]]:
        imuStates = self.makeReqAndReturnJSON('/getCollectedIMUStates')
        if 'state' in imuStates:
            return imuStates['state']
        else:
            return imuStates

    def clearCollectedIMUStates(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/clearCollectedIMUStates')

    # Heading

    def getHeading(self) -> Dict[str, Any]:
        heading = self.makeReqAndReturnJSON('/getHeading')
        if 'state' in heading:
            return heading['state']
        else:
            return heading

    # Camera Actions

    def captureShot(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/captureShot')

    def fetchThumbnailFromIndex(self, index: int) -> Dict[str, Any]:
        thumbnail = self.makeReqAndReturnJSON(
            f'/fetchThumbnailFromIndex/{index}')
        if 'state' in thumbnail:
            return thumbnail['state']
        else:
            return thumbnail

    def fetchPreviewFromIndex(self, index: int) -> Dict[str, Any]:
        preview = self.makeReqAndReturnJSON(f'/fetchPreviewFromIndex/{index}')
        if 'state' in preview:
            return preview['state']
        else:
            return preview

    def fetchMediaFromIndex(self, index: int) -> Dict[str, Any]:
        media = self.makeReqAndReturnJSON(f'/fetchMediaFromIndex/{index}')
        if 'state' in media:
            return media['state']
        else:
            return media
