import spinwheel
import numpy as np
import matplotlib.pyplot as plot

# Create a given spinning wheel
rise_time = 5
stop_time = 5
brake_time = 2

wheel = spinwheel.SmoothSpinning(rise_time, stop_time, brake_time)

# Craft a simulated behaviour
iterations = 200
times = np.arange(iterations)
wheelspeed = np.zeros(iterations)
torque_input = np.zeros(iterations)

period = int(iterations/10)
for i in range(period*3):
    torque_input[10+i] = 1

for i in range(period):
    torque_input[period*4 + i] = 1

for i in range(period):
    torque_input[period*6 + i] = -1


# Simulate
for time in times:
    # Feed the wheel with an input
    wheel.update(torque_input[time])

    # Record the subsequent speed
    wheelspeed[time] = wheel.get_current_speed()

# Plot this stuff
plot.figure()
plot.plot(times, wheelspeed, label='wheel speed')
plot.plot(times, torque_input, label='inputs')
plot.legend()
plot.grid()
plot.show()



