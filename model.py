import numpy as np
from scipy import stats
from matplotlib import pylab as pl

GRAVITY = 9.81
AIR_DENSITY = 1.205
ROLLING_RESIS = 0.004
WEIGHT_BICYCLE = 8
MECHANICAL_RESIS = 0.025

FATIGUE_FACTOR = 0.25

CDA_TYPE = 1  # 0:tt 1:std

weight = 0
height = 0
ftp = 0
energy = 0
length = 0
profile_index = 0
power_data = []
slope_data = []
hdg_data = []
wind_data = []


# weight = 70
# height = 1.814
# ftp = 5.15
# energy = 10000
# length = 22.1
# power_data =[[0, 0], [5.857647058823529, 902.0771513353116], [7.784705882352941, 765.5786350148368], [10.476470588235294, 973.293768545994], [13.137647058823529, 813.0563798219584], [16.303529411764707, 1578.635014836795], [18.031764705882352, 1145.40059347181], [21.151764705882353, 1732.9376854599404]]
#
# slope_data = [[0, 0]]
# hdg_data =[[0, 0]]
# wind_data = [[0, 0, 0]]

def initialize(_weight, _height, _ftp, _energy, _length, _profile_index, _power, _slope,
               _hdg, _wind):
    global weight
    global height
    global ftp
    global energy
    global length
    global profile_index
    global power_data
    global slope_data
    global hdg_data
    global wind_data

    weight = _weight
    height = _height
    ftp = _ftp
    energy = _energy
    length = _length
    profile_index = _profile_index
    power_data = _power
    slope_data = _slope
    hdg_data = _hdg
    wind_data = _wind

    # print(weight)
    # print(height)
    # print(ftp)
    # print(energy)
    # print(length)
    # print(profile_index)
    # print(power_data)
    # print(slope_data)
    # print(hdg_data)
    # print(wind_data)


# x param all in km
def power(x):
    for i in range(len(power_data) - 1, -1, -1):
        if power_data[i][0] <= x:
            if i + 1 < len(power_data):
                return np.interp(x, [power_data[i][0], power_data[i + 1][0]],
                                 [power_data[i][1], power_data[i + 1][1]])
            else:
                return power_data[i][1]


def slope(x):
    for i in range(len(slope_data) - 1, -1, -1):
        if slope_data[i][0] <= x:
            # no interp
            return slope_data[i][1]


# positive for tail wind
def wind(x):
    current_hdg = 0
    for i in range(len(hdg_data) - 1, -1, -1):
        if hdg_data[i][0] <= x:
            if i + 1 < len(hdg_data):
                current_hdg = np.interp(x, [hdg_data[i][0], hdg_data[i + 1][0]],
                                        [hdg_data[i][1], hdg_data[i + 1][1]])
            else:
                current_hdg = hdg_data[i][1]
            break

    current_wind_hdg = 0
    current_wind_speed = 0
    for i in range(len(wind_data) - 1, -1, -1):
        if wind_data[i][0] <= x:
            # no intercept required
            current_wind_hdg = wind_data[i][1]
            current_wind_speed = wind_data[i][2]
            break

    return current_wind_speed * -np.cos(np.deg2rad(current_wind_hdg - current_hdg))


# requires calibrated wind
def v(x):
    CdAs = [
        0.7 * (0.0293 * np.power(height, 0.725) * np.power(weight, 0.425) + 0.0604),
        0.88 * (0.0267 * np.power(height, 0.725) * np.power(weight, 0.425) + 0.1674)]

    current_wind = wind(x)
    current_slope = slope(x)

    a = 0.5 * AIR_DENSITY * CdAs[CDA_TYPE]
    b = 2 * 0.5 * AIR_DENSITY * CdAs[CDA_TYPE] * current_wind
    c = 0.5 * AIR_DENSITY * CdAs[CDA_TYPE] * (current_wind ** 2) \
        + ROLLING_RESIS * (weight + WEIGHT_BICYCLE) * GRAVITY * np.cos(
        np.arctan(current_slope / 100)) \
        + (weight + WEIGHT_BICYCLE) * GRAVITY * np.sin(
        np.arctan(current_slope / 100))

    d = power(x) * (1 - MECHANICAL_RESIS)

    # added manually to avoid sqrt with negative number and respond NaN
    if c < 0:
        c = 0

    v = np.cbrt(
        ((-b ** 3) / (27 * a ** 3) + (b * c) / (6 * a ** 2) - d / (2 * a)) + np.sqrt(
            ((-b ** 3) / (27 * a ** 3) + (b * c) / (6 * a ** 2) - d / (2 * a)) ** 2 + (
                    c / (3 * a) - (b ** 2) / (9 * a ** 2)) ** 3)) \
        + np.cbrt(
        ((-b ** 3) / (27 * a ** 3) + (b * c) / (6 * a ** 2) - d / (2 * a)) - np.sqrt(
            ((-b ** 3) / (27 * a ** 3) + (b * c) / (6 * a ** 2) - d / (2 * a)) ** 2 + (
                    c / (3 * a) - (b ** 2) / (9 * a ** 2)) ** 3)) \
        - b / (3 * a)

    return np.abs(v)


# tt-men,women; sp-men,women
def durlim(index, p, x):
    stdwt = 0
    profile = None

    if index == 0:
        stdwt = 70
        profile = [[5.15 * stdwt, 40 * 60], [5.53 * stdwt, 5 * 60],
                   [8.40 * stdwt, 1 * 60], [15.88 * stdwt, 5]]

    elif index == 1:
        stdwt = 60.1
        profile = [[4.70 * stdwt, 40 * 60], [5.31 * stdwt, 5 * 60],
                   [8.29 * stdwt, 1 * 60], [15.11 * stdwt, 5]]

    elif index == 2:
        stdwt = 71.5
        profile = [[3.73 * stdwt, 40 * 60], [4.08 * stdwt, 5 * 60],
                   [8.28 * stdwt, 1 * 60], [19.96 * stdwt, 5]]

    elif index == 3:
        stdwt = 59.8
        profile = [[3.31 * stdwt, 40 * 60], [3.93 * stdwt, 5 * 60],
                   [7.75 * stdwt, 1 * 60], [16.19 * stdwt, 5]]

    # profile power does not begin from 0
    if p < profile[0][0]:
        return np.interp(p, [0, profile[0][0]], [30000, profile[0][1]])

    for i in range(len(profile) - 1, -1, -1):
        if profile[i][0] <= p:
            if i + 1 < len(profile):
                return (1 - FATIGUE_FACTOR * (x / length)) * np.interp(p, [profile[i][0],
                                                                           profile[i + 1][
                                                                               0]],
                                                                       [profile[i][1],
                                                                        profile[i + 1][
                                                                            1]])
            else:
                # for above highest profiled power,interp towards 0
                return (1 - FATIGUE_FACTOR * (x / length)) * np.interp(p, [profile[i][0],
                                                                           2500],
                                                                       [profile[i][1], 0])


def calculate_data():
    # distances, in km
    xs = np.linspace(0, length, 1000)
    # speeds, in m/s ;ys[0]=0
    vs = np.array([0.0] * len(xs))
    for i in range(1, len(xs)):
        vs[i] = 1 / v(xs[i])

    ################## Calculating ts (time) at each x using integral ##################
    # times, in s
    ts = [0.0] * len(xs)

    # from km to m
    lap = (xs[len(xs) - 1] - xs[0]) * 1000

    for i, ie in enumerate(xs):
        ts[i] = np.sum(vs[0:i + 1] * lap / len(xs))

    ################## Calculating power limit at each x ##################

    # 2500 is the sign for non-set
    plims_sparse = [2500] * len(xs)

    is_previous_exceeded = False
    prev_barrier_time = -1
    prev_barrier_power = 0

    # power_data guaranteed to have length>=2
    for i in range(0, len(power_data) - 1):
        is_ascending_or_hold = True

        if power_data[i][1] > power_data[i + 1][1]:
            is_ascending_or_hold = False

        x_index_l = 0
        x_index_r = 0

        for j in range(len(xs) - 1, -1, -1):
            if xs[j] <= power_data[i][0]:
                x_index_l = j
                break

        for j in range(len(xs) - 1, -1, -1):
            if xs[j] <= power_data[i + 1][0]:
                x_index_r = j
                break

        print(
            f"[PD-SECTION {i}] PrevExceeded={is_previous_exceeded} IsAscendingHold={is_ascending_or_hold} x=({power_data[i][0]},{power_data[i + 1][0]})")

        # clear all plims above this descent bottom after current x.
        # requires all descents dive below plim if previously exceeded
        if not is_ascending_or_hold:
            print("    Enter Branch 1 (Descend)")
            print("        Power Limits Removed At: ", end="")
            for j in range(x_index_r, len(plims_sparse)):
                if plims_sparse[j] > power_data[i + 1][1] and plims_sparse[j] != 2500:
                    # should not clear last point
                    if j == len(plims_sparse) - 1:
                        plims_sparse[j] = power(xs[x_index_r])
                        print(f"{j}(x={xs[j]})(Last, Set={plims_sparse[j]}),", end="")
                    else:
                        plims_sparse[j] = 2500
                        print(f"{j}(x={xs[j]}),", end="")

            # update barrier value to nearest plim after current x, if any
            prev_barrier_time = -1
            prev_barrier_power = 0
            for j in range(x_index_r, len(plims_sparse)):
                if plims_sparse[j] != 2500:
                    prev_barrier_power = plims_sparse[j]
                    prev_barrier_time = ts[j]
                    print()
                    print(
                        f"        Reset PrevBarrierT={prev_barrier_time} PrevBarrierP={prev_barrier_power}",
                        end="")
                    break

            print()
            print("        *PrevExceeded Released")
            is_previous_exceeded = False
        elif not is_previous_exceeded:
            print("    Enter Branch 2 (Ascend & Not PrevExceed)")

            for j in range(x_index_l, x_index_r + 1):
                current_power = power(xs[j])
                max_dur = durlim(profile_index, current_power, xs[j])
                dur_end_time = ts[j] + max_dur

                if ts[j] > prev_barrier_time and current_power > prev_barrier_power:
                    print(
                        f"        Exceeded Power Lim: i={i} x={xs[j]} t={ts[j]} power={current_power} PrevBarrierT={prev_barrier_time} PrevBarrierP={prev_barrier_power}")
                    print("        *PrevExceeded Set")
                    is_previous_exceeded = True
                    break

                # update barrier if current duration end is earlier than previous barrier
                if dur_end_time < prev_barrier_time or prev_barrier_time == -1:
                    prev_barrier_time = dur_end_time
                    prev_barrier_power = current_power

                    print(
                        f"        Set PrevBarrierT={prev_barrier_time} PrevBarrierP={prev_barrier_power}",
                        end="")

                    for k in range(len(ts) - 1, -1, -1):
                        if ts[k] <= dur_end_time:
                            plims_sparse[k] = current_power
                            print(
                                f", Add Power Lim: x_orig={xs[j]} x={xs[k]} lim={current_power}")
                            break
        print("    Leave Section")

    plims = []
    for i, ie in enumerate(plims_sparse):
        if ie != 2500:
            plims.append([xs[i], ie])

    ################## Calculating energy consumption at each x ##################
    energy_consumption = 0
    last_x_index = 0

    # power guaranteed to be length>=2
    for i in range(0, len(power_data) - 1):
        x_index_l = 0
        x_index_r = 0
        for j in range(len(xs) - 1, -1, -1):
            if xs[j] <= power_data[i][0]:
                x_index_l = j
                break

        for j in range(len(xs) - 1, -1, -1):
            if xs[j] <= power_data[i + 1][0]:
                x_index_r = j
                break

        last_x_index = x_index_r
        delta_t = ts[x_index_r] - ts[x_index_l]
        if delta_t == 0:
            continue
        p_acce = (power_data[i + 1][1] - power_data[i][1]) / delta_t

        energy_consumption += power_data[i][1] * delta_t + 0.5 * p_acce * delta_t ** 2

    energy_consumption += power_data[len(power_data) - 1][1] * (
            ts[len(ts) - 1] - ts[last_x_index])

    # Do not [[0,0]]*len(xs) here. references will be same
    # xs_plims = []
    #
    # for i, ie in enumerate(xs):
    #     xs_plims.append([ie, plims[i]])

    # slps=[0]*len(xs)
    # for i,ie in enumerate(xs):
    #     slps[i]=slope(ie)
    #
    # pl.plot(xs,slps)
    # pl.show()

    # print(xs)
    # print(ts)
    # regress_results=stats.linregress(xs,ts)
    # print(regress_results)
    # pl.plot(xs,ts,c=(np.array([102,194,165]) / 255).reshape((1, -1)),label="Original")
    # pl.plot(xs,regress_results[0]*xs+regress_results[1],c=(np.array([252,141,98]) / 255).reshape((1, -1)),label="Fitted")
    # pl.title("t-x Curve And Regression")
    # pl.legend()
    # pl.xlabel("x/km")
    # pl.ylabel("t/s")
    # pl.show()

    return {
        "timeConsumptionS": ts[len(ts) - 1],
        "energyConsumptionKj": energy_consumption / 1000,
        "plimData": plims
    }

# x = np.arange(500, 2000)
# y = [0] * len(x)
# for i, ie in enumerate(x):
#     y[i] = durlim(0, ie)
#
# pl.plot(x, y)
# pl.show()
