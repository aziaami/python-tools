#!/bin/python

# Script to plot global localisation_poses

import matplotlib.pyplot as plt
import os
import random

# -----------------------
# constants

HOMEDIR = os.environ['HOME']
# -----------------------


def random_color():
    colours = ['red', 'green', 'blue']
    return random.choice(colours)


def get_color(filepath):
    if (filepath == RUN_1):
        return 'green'
    else:
        return 'blue'
# -----------------------

# this was generated offline by replaying BB3 logs.
RUN_1 = "/data/logs/2016-09-02-01-19-50-absoluteaccuracy03-2/logs/udp_publisher/dub4/localisation_poses.txt"
# this was generated live on the HYG forklift truck in the warehouse.
RUN_2 = "%s/data/Hyster-Yale/new_data/2016-07-26-12-13-21-absoluteaccuracy03/logs/udp_publisher/camera_localiser/localisation_poses.txt" % HOMEDIR


legend_labels = ['offline', 'live']
RUNS = [RUN_1, RUN_2]
for filepath in RUNS:
    t = [], dt = []
    x = [], dx = []
    y = [], dy = []

    # add label for legend
    run = filepath.split('/')[-3]
    legend_labels.append(run)

    for line in open(filepath):
        line = line.rstrip('\n')
        e = [l.strip() for l in line.split(',')]

        t_since_start = (float(e[0])-1469531609469617)*(10**-6)     # seconds

        # store all values in dataset
        t.append(t_since_start)
        x.append(float(e[1])*1)     # multiply 100 to get cm, 1000 to get mm
        y.append(float(e[2])*1000)  # multiply 100 to get cm, 1000 to get mm

        # define a time interval
        ts_start = 190    # start time (s) of interval
        ts_end = 240      # end time (s) of interval

        # only store values in the defined time interval
        if ((ts_start < t_since_start) and (t_since_start < ts_end)):
            dt.append(t_since_start)
            dx.append(float(e[1])*1)     # multiply 100 to get cm, 1000 to get mm
            dy.append(float(e[2])*1000)  # multiply 100 to get cm, 1000 to get mm

    #plt.plot(x, y)     # line plot

    # Use scatter to plot points for each datum
    #plt.scatter(x, y, color=get_color(filepath))
    plt.scatter(t, x, color=get_color(filepath))
    #plt.scatter(t, y, color=get_color(filepath))

# final plot stuff
plt.legend(legend_labels, loc='upper left')
plt.xlabel('t(s)')
plt.ylabel('x(m)')
plt.show()
