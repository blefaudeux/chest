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

    def get_current_speed(self):
        return self._currentSpeed

    def set_current_speed(self):
        return self._currentSpeed


# Same principle, but using a manually defined curve shape
class SmoothSpinning:
    def __init__(self, rise_time, stop_time, brake_time):
        self._riseTime = rise_time/2        # The characteristic time for the free wheel acceleration
        self._stopTime = stop_time          # The characteristic time for the free wheel stop
        self._brakeTime = brake_time        # The characteristic time when 'braking' (reversed input)
        self._currentSpeed = 0.             # Speed in the different motions..
        self._stopSpeed = 0.
        self._brakeSpeed = 0.
        self._counterStart = 0.             # Counter for the 'rise/stop/brake' procedures
        self._counterStop = 0.
        self._counterBrake = 0.
        self._stopThreshold = 0.01          # Stop when speed is below this point

    def sigmoid_update(self):
        if (self._counterStop > 0. or self._counterBrake > 0.) and self._currentSpeed > 0.:
            # We were in another procedure, start from here
            self._counterStart = -np.log(max(0.01, -np.log(np.abs(self._currentSpeed)))) * self._riseTime
            self._counterStart += 6*self._riseTime

        self._currentSpeed = 1/(1 + np.exp(-(self._counterStart - 6*self._riseTime)/self._riseTime))
        self._counterStart += 1.

        # Reset the stop & brake procedures
        self._counterStop = 0.
        self._counterBrake = 0.

    def sigmoid_stop(self):
        if self._counterStop == 0.:
            self._stopSpeed = self._currentSpeed

        self._currentSpeed = self._stopSpeed * np.exp(- self._counterStop / self._stopTime)

        if np.abs(self._currentSpeed) < self._stopThreshold:
            self._currentSpeed = 0.

        self._counterStop += 1.

    def sigmoid_brake(self):
        if self._counterBrake == 0.:
            self._brakeSpeed = self._currentSpeed

        self._currentSpeed = self._brakeSpeed * np.exp(- self._counterBrake / self._brakeTime)

        if np.abs(self._currentSpeed) < self._stopThreshold:
            self._currentSpeed = 0.

        self._counterBrake += 1.

    def update(self, direction):

        if np.abs(self._currentSpeed) == 0.:
            # Start a brand new sigmoid
            self._counterStart = 0.
            self.sigmoid_update()
            self._currentSpeed *= np.sign(direction)

        else:
            sign = np.sign(self._currentSpeed)

            if direction == 0.:
                self.sigmoid_stop()

            # Something is already in place
            elif sign * np.sign(direction) > 0:
                # Keep going with the existing sigmoid
                self.sigmoid_update()
                self._currentSpeed *= sign

            else:
                # Brake
                self.sigmoid_brake()

    def get_current_speed(self):
        return self._currentSpeed

    def set_current_peed(self):
        return self._currentSpeed
