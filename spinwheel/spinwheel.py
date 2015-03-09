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
        if np.abs(self._currentSpeed) < self._staticFriction:
            current_static_friction = 0
        else:
            current_static_friction = self._staticFriction

        self._currentSpeed += input_torque - sign * (self._dynamicFriction *
                                                     np.abs(self._currentSpeed) + current_static_friction)

    def getCurrentWheelSpeed(self):
        return self._currentSpeed

    def setCurrentWheelSpeed(self):
        return self._currentSpeed
