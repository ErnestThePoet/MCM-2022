from matplotlib import pylab as pl
import numpy as np

import scipy.optimize as op

time_trial_profile = {
    "durations": np.array([5, 1 * 60, 5 * 60, 40 * 60]),
    "std_weight": [70, 60.1],
    "std_height": [181.4, 170.0],
    "relative_power": [
        np.array([15.88, 8.40, 5.53, 5.15]),
        np.array([15.11, 8.29, 5.31, 4.70])]
}

sprinter_profile = {
    "durations": np.array([5, 1 * 60, 5 * 60, 40 * 60]),
    "std_weight": [71.5, 59.8],
    "std_height": [178.4, 168.0],
    "relative_power": [
        np.array([19.96, 8.28, 4.08, 3.73]),
        np.array([16.19, 7.75, 3.93, 3.31])]
}

plot_colors = [
    (np.array([228, 26, 28]) / 255).reshape((1, -1)),
    (np.array([55, 126, 184]) / 255).reshape((1, -1))
]

fit_functions=[
    lambda x:811.2*np.exp(-0.02346*x)+390.2*np.exp(-3.302e-05*x),
    lambda x:652*np.exp(-0.02186*x)+323.7*np.exp(-5.673e-05*x),
    lambda x:1279*np.exp(-0.02426*x)+294.5*np.exp(-4.127e-05*x),
    lambda x:811.1*np.exp(-0.02135*x)+239.3*np.exp(-7.903e-05*x),
]

pl.scatter(
    np.log10(time_trial_profile["durations"]),
    time_trial_profile["std_weight"][0] * time_trial_profile[
        "relative_power"][0],
    c=plot_colors[0])

pl.scatter(
    np.log10(time_trial_profile["durations"]),

    time_trial_profile["std_weight"][1] * time_trial_profile[
        "relative_power"][1],
    c=plot_colors[0])

pl.scatter(
    np.log10(sprinter_profile["durations"]),

    sprinter_profile["std_weight"][0] * sprinter_profile[
        "relative_power"][0],
    c=plot_colors[1])

pl.scatter(
    np.log10(sprinter_profile["durations"]),
    sprinter_profile["std_weight"][1] * sprinter_profile[
        "relative_power"][1],
    c=plot_colors[1])

x_densitive=np.arange(1,2501,1)

pl.plot(
    np.log10(x_densitive),
    fit_functions[0](x_densitive),
    label=f"Time Trial Specialist (men; {time_trial_profile['std_weight'][0]}kg)",
    c=plot_colors[0])

pl.plot(
    np.log10(x_densitive),
    fit_functions[1](x_densitive),
    label=f"Time Trial Specialist (women; {time_trial_profile['std_weight'][1]}kg)",
    ls="--", c=plot_colors[0])

pl.plot(
    np.log10(x_densitive),
    fit_functions[2](x_densitive),
    label=f"Sprinter (men; {sprinter_profile['std_weight'][0]}kg)",
    c=plot_colors[1])

pl.plot(
    np.log10(x_densitive),
    fit_functions[3](x_densitive),
    label=f"Sprinter (women; {sprinter_profile['std_weight'][1]}kg)",
    ls="--", c=plot_colors[1])

pl.title("Power Profile")

pl.legend()

pl.ylim(0,1500)

pl.xlabel("log10( Duration/s )")
pl.ylabel("Max. Power/Watts")

pl.grid()

pl.show()
