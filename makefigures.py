#! /usr/bin/env python3
import csv
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
import statistics
import argparse





if __name__ == "__main__":

    testFile = "./CS6604Project/test0.csv"
    compareFile = "./CS6604Project/test2.csv"

    testVolts = []
    testAmps = []
    compVolts = []
    compAmps = []
    testSample = []
    compSample = []
    # Read string data values to rpiReadData
    with open(testFile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            testVolts.append(row['volts'])
            testAmps.append(row['current'])
            testSample.append(row['sample'])

    with open(compareFile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            compVolts.append(row['volts'])
            compAmps.append(row['current'])
            compSample.append(row['sample'])



    testPower = []
    compPower = []

    for num1, num2 in zip(testVolts, testAmps):
        testPower.append(float(num1)*float(num2))

    for num1, num2 in zip(compVolts, compAmps):
        compPower.append(float(num1)*float(num2))

    xtestvals = testSample
    xcompvals = compSample
    ylabel = "Power Draw [W]"
    xlabel = "Time [s]"
    title = "rpi3 SQL Sanitization Power Draw Comparison"
    # Use matplotlib to plot data
    plt.locator_params(axis='x', nbins=10)
    fig, ax = plt.subplots()
    ax.plot(xtestvals, testPower, label="No Offloading")
    ax.plot(xcompvals,compPower, label="Offloading")

    ax.set(xlabel=xlabel,ylabel=ylabel,title=title)
    ax.legend(loc="best")
    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.show()



