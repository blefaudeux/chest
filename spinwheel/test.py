import spinwheel
import numpy as np
import matplotlib.pyplot as plot

# Create a given spinning wheel
static_friction = 0.1
dynamic_friction = 0.01
wheel = spinwheel.SpinWheel(static_friction, dynamic_friction)

# Craft a simulated behaviour
iterations = 300
times = np.arange(iterations)
wheelspeed = np.zeros(iterations)
torque_input = np.zeros(iterations)

period = 40
for i in range(period):
    torque_input[i] = np.sin(float(i/period * 3.14))

for i in range(period):
    torque_input[3*period+i] = -np.sin(float(i/period * 3.14))


# Simulate
for time in times:
    # Feed the wheel with an input
    wheel.update(torque_input[time])

    # Record the subsequent speed
    wheelspeed[time] = wheel.getCurrentWheelSpeed()

# Plot this stuff
plot.figure()
plot.plot(times, wheelspeed, label='wheelspeed')
plot.plot(times, torque_input, label='inputs')
plot.legend()
plot.grid()
plot.show()



