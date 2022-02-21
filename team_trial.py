import json

import numpy as np
from model import initialize, calculate_data_team, v

GRAVITY = 9.81
AIR_DENSITY = 1.205
ROLLING_RESIS = 0.004
WEIGHT_BICYCLE = 8
MECHANICAL_RESIS = 0.025

CDA_TYPE = 1  # 0:tt 1:std

weight = 70
height = 1.814
ftp = 5.15
energy = 10000
length = 100

PROFILE_INDEX = 0

power_data = [[0, 0]]

slope_data = [[0, 0]]
hdg_data = [[0, 0]]
wind_data = [[0, 0, 0]]

initialize(weight, height, ftp, energy, length, PROFILE_INDEX, power_data, slope_data,
           hdg_data,
           wind_data)

calculate_data_team()