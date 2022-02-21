import json

import numpy as np
from model import initialize, calculate_data, v

GRAVITY = 9.81
AIR_DENSITY = 1.205
ROLLING_RESIS = 0.004
WEIGHT_BICYCLE = 8
MECHANICAL_RESIS = 0.025

CDA_TYPE = 1  # 0:tt 1:std

weight = 60.1
height = 1.70
ftp = 4.7
energy = 10000
length = 22.1

PROFILE_INDEX = 1

power_data = [[0, 580.078125]]

slope_data = [[0, 0]]
hdg_data = [[0, 0]]
wind_data = [[0, 0, 0]]

low = 100
high = 1500
mid = (high + low) / 2
power_data[0][1] = mid

initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data, slope_data,
           hdg_data,
           wind_data)

while abs(3.6 * v(0,0) - 44.2) > 1e-3:
    if 3.6 * v(0,0) > 44.2:
        high = mid
        mid = (high + low) / 2
        power_data[0][1] = mid
        initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data,
                   slope_data,
                   hdg_data, wind_data)
    else:
        low = mid
        mid = (high + low) / 2
        power_data[0][1] = mid
        initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data,
                   slope_data,
                   hdg_data, wind_data)

print(f"p={mid}")

low = 1
high = 100
mid = (high + low) / 2
length = mid

initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data, slope_data,
           hdg_data,
           wind_data)
while abs(calculate_data()["timeConsumptionS"] - 1800) > 1e-3:
    if calculate_data()["timeConsumptionS"] > 1800:
        high = mid
        mid = (high + low) / 2
        length = mid
        initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data,
                   slope_data,
                   hdg_data, wind_data)
    else:
        low = mid
        mid = (high + low) / 2
        length = mid
        initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data,
                   slope_data,
                   hdg_data, wind_data)

print(mid)
print(calculate_data())
