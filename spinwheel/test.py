import spinwheel
import numpy as np
import matplotlib.pyplot as plot

# Create a given spinning wheel
static_friction = 0.01
dynamic_friction = 0.05
wheel_power = spinwheel.SpinWheelPower(static_friction, dynamic_friction, 2)

# Craft a simulated behaviour
iterations = 100
times = np.arange(iterations)
wheelspeed = np.zeros(iterations)
wheelspeed_power = np.zeros(iterations)
torque_input = np.zeros(iterations)

period = 40
for i in range(period):
    torque_input[i] = 0.7


# Simulate
for time in times:
    # Feed the wheel with an input
    wheel_power.update(torque_input[time])

    # Record the subsequent speed
    wheelspeed_power[time] = wheel_power.getCurrentWheelSpeed()

# Plot this stuff
plot.figure()
plot.plot(times, wheelspeed_power, label='wheelSpeedPower')
plot.plot(times, torque_input, label='inputs')
plot.legend()
plot.grid()
plot.show()



