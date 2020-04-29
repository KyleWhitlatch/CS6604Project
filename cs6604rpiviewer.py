#! /usr/bin/env python3
import csv
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
import statistics
import argparse
class rpiReadData:

    def __init__(self, name):
        self.name = name
        self.sampleNum = []
        self.availibleMem = []
        self.totalMem = []
        self.memPerc = []
        self.cpuTemp = []
        self.cpuLoad = []
        self.processArray = []
        self.rowCnt = 0


def getCPUArrayVals(inputString):

    # inputString = inputString[1:-1]
    inputString = inputString.replace("\'","")
    strArray = list(inputString.split(", "))
    floatArray = []
    for str in strArray:
        floatArray.append(float(str))

    floatAvg = statistics.mean(floatArray) # TEMP, may change in future, used to get single value for plotting

    return floatAvg


def getMemVals(inputString):

    inputString = inputString[6:]
    memString, percString = inputString.split(" ")
    availStr, totalStr = memString.split("/")
    percString = percString.replace("(", "")
    percString = percString.replace(")", "")
    floatArray = [float(percString), float(availStr), float(totalStr)]

    return floatArray



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--testNum",type=int,default=0,help="Test number to process data for...")
    parser.add_argument("--plotTitle",type=str,default="Testing",help="Title to use for plotting...")
    args = parser.parse_args()
    testReadNum = args.testNum
    filename = "piTestRecord" + str(testReadNum) + ".csv"
    fullFileName = "./rpidata/" + filename
    processFileName = "piTestRecord"+ str(testReadNum) + "pl.csv"
    fullProcessName = "./rpidata/" + processFileName

    ###########################
    # Change name for plotting here:
    name = args.plotTitle
    rpiRead = rpiReadData(name)


    # Read string data values to rpiReadData
    with open(fullFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            rpiRead.sampleNum.append(row['SN'])
            rpiRead.cpuTemp.append(getCPUArrayVals(row['CPU Temp. [C]']))
            rpiRead.cpuLoad.append(getCPUArrayVals(row['CPU % Load']))

            memArray = getMemVals(row['Virtual Memory [mB] (%)'])
            rpiRead.memPerc.append(memArray[0])
            rpiRead.availibleMem.append(memArray[1])
            rpiRead.totalMem.append(memArray[2])

    # Use matplotlib to plot data

    plotArray = [rpiRead.cpuTemp, rpiRead.cpuLoad,rpiRead.availibleMem, rpiRead.totalMem, rpiRead.memPerc]
    numFeatures = len(plotArray)
    titleName = rpiRead.name + "Data"
    titleArray = [titleName, titleName,titleName,titleName,titleName]
    ylabels = ["CPU Temp [C]", "CPU Load (%)", "Memory Used [MB]", "Total Memory [MB]", "Used Memory (%)"]
    figList = [0] * numFeatures
    axList = [0] * numFeatures

    for i in range(len(plotArray)):
        figList[i] = plt.figure()
        axList[i] = figList[i].add_subplot(111)
        workingArray = plotArray[i]
        axList[i].plot(rpiRead.sampleNum, workingArray)
        axList[i].set_xlabel("Time [s]")
        axList[i].set_ylabel(ylabels[i])
        axList[i].set_title(titleArray[i])

    # Read number of processes in process log and how often each process is run
    processArray = []

    with open(fullProcessName, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) # skip header
        for row in csv_reader:
            processArray.append(row)

    # Plot total number of processes for each sample on bar graph
    xTotalList = []
    yTotalList = []

    for i in range(len(processArray)):
        yTotalList.append(len(processArray[i]))
        xTotalList.append(i+1)

    totalFig = plt.figure()
    totalAx = totalFig.add_subplot(111)
    totalAx.bar(xTotalList, yTotalList)
    totalAx.set_xlabel("Sample Number")
    totalAx.set_ylabel("Total Number of Processes")
    totalAx.set_title("Bar Graph of Total System Processes")
    totalAx.set_ylim(min(yTotalList) - 10, max(yTotalList) + 10)

    # Plot number of occurances of each system process
    longProcessList = []
    workingList = []
    cleanedArray = []
    for sublist in processArray:
        workingList = []
        for entry in sublist:
            mysplit = entry.split(" ")
            process = mysplit[1]
            longProcessList.append(process)
            workingList.append(process)
        cleanedArray.append(workingList)


    processSet = list(set(longProcessList))
    occurSetList = [0] * len(processSet)

    occurIdx = -1
    for unique in processSet:
        occurIdx += 1
        for sublist in cleanedArray:
            if unique in sublist:
                occurSetList[occurIdx] += 1

    trimmedOccurList = []
    trimmedProcessList = []
    for i in range(len(occurSetList)):
        if (occurSetList[i] != len(processArray)):
            trimmedOccurList.append(occurSetList[i])
            trimmedProcessList.append(processSet[i])

    # occurXPlot = [i for i in range(len(trimmedProcessList))]
    occurXPlot = np.arange(len(trimmedProcessList))
    width = 0.75
    occurFig = plt.figure()
    occurAx = occurFig.add_subplot(111)
    occurAx.barh(occurXPlot, trimmedOccurList)
    occurAx.set_yticks(occurXPlot)
    occurAx.set_yticklabels(trimmedProcessList)
    occurAx.set_ylabel("System Processes")
    occurAx.set_xlabel("Occurances")
    occurAx.set_title("Plot of System Occurances")

    plt.show()

    print("Done plotting data!")

