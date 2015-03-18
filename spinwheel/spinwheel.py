import numpy as np


class SpinWheel:
    def __init__(self, static_friction, dynamic_friction):
        self._inertia = 1                           # Not used, could be played with afterwards
        self._staticFriction = static_friction      # The friction of the wheel against its axe at low speed
        self._dynamicFriction = dynamic_friction    # The friction dependent to the speed
        self._currentSpeed = 0                      # Current state of the wheel

    def update(self, input_torque):
        sign = np.sign(self._currentSpeed)

        # Prevent numerical instability
        overall_friction = (self._dynamicFriction * np.abs(self._currentSpeed) + self._staticFriction )
        overall_friction = min(np.abs(self._currentSpeed), overall_friction)

        self._currentSpeed += input_torque - sign * overall_friction

    def getCurrentWheelSpeed(self):
        return self._currentSpeed

    def setCurrentWheelSpeed(self):
        return self._currentSpeed


# Same principle, but using a power transfer fonction
class SpinWheelPower:
    def __init__(self, static_friction, dynamic_friction, target_speed):
        self._inertia = 1                           # Not used, could be played with afterwards
        self._staticFriction = static_friction      # The friction of the wheel against its axe at low speed
        self._dynamicFriction = dynamic_friction    # The friction dependent to the speed
        self._currentSpeed = 0                      # Current state of the wheel
        self._targetSpeed = target_speed

    def update(self, input_torque):
        sign = np.sign(self._currentSpeed)

        # Prevent numerical instability
        overall_friction = (self._dynamicFriction * np.abs(self._currentSpeed) + self._staticFriction )
        overall_friction = min(np.abs(self._currentSpeed), overall_friction)

        # Modulate the input torque by the transfer function
        delta_speed = self._currentSpeed - self._targetSpeed
        sigma_speed = self._targetSpeed / 2
        input_power = input_torque * np.exp(-delta_speed * delta_speed / (2 * sigma_speed * sigma_speed))

        self._currentSpeed += input_power - sign * overall_friction

    def getCurrentWheelSpeed(self):
        return self._currentSpeed

    def setCurrentWheelSpeed(self):
        return self._currentSpeed
