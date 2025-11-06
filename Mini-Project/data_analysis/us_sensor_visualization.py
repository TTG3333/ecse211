#!/usr/bin/env python3

from matplotlib import pyplot as plt

DELAY_SEC = 0.01
DATA_FILES = ["us_sensor_10cm2.csv", "us_sensor_20cm2.csv", "us_sensor_30cm2.csv"]

distances = []
for us_sensor_data_file in DATA_FILES:
    sub = []
    with open(us_sensor_data_file, "r") as f:
        sub.extend([float(d) for d in f.readlines()])
    distances.append(sub)

for i, d in enumerate(distances):
    times = [DELAY_SEC * i for i in range(len(d))]
    plt.plot(times, d, label=f"Set distance: {(i+1)*10} cm")

plt.xlabel("Time (s)")
plt.ylabel("Distance (cm)")
plt.legend()
plt.yticks(range(0, 40, 10))
plt.grid(axis="y")
plt.tight_layout()
plt.show()
