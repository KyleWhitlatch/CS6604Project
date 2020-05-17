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
    parser.add_argument("--compareNum", type=int,default=0,help="Test number to compare data against")
    parser.add_argument("--plotTitle",type=str,default="Testing",help="Title to use for plotting...")
    parser.add_argument("--doTrim", type=bool, default=False,help="Trim sample plots to shortest.")
    parser.add_argument("--compareTrim",type=int,default=0,help="Number of samples to trim for compare data.")
    parser.add_argument("--testTrim",type=int,default=0,help="Number of samples to trim for test data.")
    args = parser.parse_args()
    testReadNum = args.testNum
    testcompareNum = args.compareNum
    filename = "piTestRecord" + str(testReadNum) + ".csv"
    fullFileName = "./CS6604Project/rpidata/" + filename
    processFileName = "piTestRecord"+ str(testReadNum) + "pl.csv"
    fullProcessName = "./CS6604Project/rpidata/" + processFileName
    compfilename = "piTestRecord" + str(testcompareNum) + ".csv"
    compFile= "./CS6604Project/rpidata/" + compfilename
    cprocessFileName = "piTestRecord"+ str(testcompareNum) + "pl.csv"
    fullcprocessFileName = "./CS6604Project/rpidata/" + cprocessFileName
    compareTrim = args.compareTrim
    testTrim = args.testTrim

    ###########################
    name = args.plotTitle
    rpiRead = rpiReadData(name)
    rpiCompare = rpiReadData(name)
    doTrimming = args.doTrim

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

    # Read comparison file
    with open(compFile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            rpiCompare.sampleNum.append(row['SN'])
            rpiCompare.cpuTemp.append(getCPUArrayVals(row['CPU Temp. [C]']))
            rpiCompare.cpuLoad.append(getCPUArrayVals(row['CPU % Load']))

            memArray = getMemVals(row['Virtual Memory [mB] (%)'])
            rpiCompare.memPerc.append(memArray[0])
            rpiCompare.availibleMem.append(memArray[1])
            rpiCompare.totalMem.append(memArray[2])

    compArray = [rpiCompare.cpuTemp, rpiCompare.cpuLoad, rpiCompare.availibleMem, rpiCompare.totalMem, rpiCompare.memPerc]

    if testTrim != 0:
        rpiRead.sampleNum.append(row['SN'])
        rpiRead.cpuTemp = rpiRead.cpuTemp[testTrim:]
        rpiRead.cpuLoad = rpiRead.cpuTemp[testTrim:]
        rpiRead.memPerc = rpiRead.memPerc[testTrim:]

    if compareTrim != 0:
        rpiRead.sampleNum.append(row['SN'])
        rpiRead.cpuTemp = rpiRead.cpuTemp[compareTrim:]
        rpiRead.cpuLoad = rpiRead.cpuTemp[compareTrim:]
        rpiRead.memPerc = rpiRead.memPerc[compareTrim:]

    if not doTrimming:
        plt.locator_params(axis='x', nbins=10)
        fig, axs = plt.subplots(3,sharex=True)
        fig.suptitle(name)
        axs[0].plot(rpiRead.sampleNum, rpiRead.cpuTemp,'tab:blue',label="")
        axs[0].plot(rpiCompare.sampleNum, rpiCompare.cpuTemp,'tab:red')
        axs[1].plot(rpiRead.sampleNum, rpiRead.cpuLoad, 'tab:blue')
        axs[1].plot(rpiCompare.sampleNum, rpiCompare.cpuLoad, 'tab:red')
        axs[2].plot(rpiRead.sampleNum, rpiRead.memPerc, 'tab:blue',label="No Offloading")
        axs[2].plot(rpiCompare.sampleNum, rpiCompare.memPerc, 'tab:red', label="Offloading")
        axs[2].legend(loc='center right')
        axs[2].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x))))

        for index,ax in enumerate(axs.flat):
            if index == 2:
                ax.set(xlabel='Sample', ylabel=ylabels[index])
            else:
                ax.set( ylabel=ylabels[index])

        every_nth = 10
        for ax in axs.flat:
            for n, label in enumerate(ax.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)
    else:

        # Find shortest samples for compare and read
        minsamples = min(len(rpiRead.sampleNum),len(rpiCompare.sampleNum))
        minsamples = minsamples - 1

        plt.locator_params(axis='x', nbins=10)
        fig, axs = plt.subplots(3, sharex=True)
        fig.suptitle(name)
        axs[0].plot(rpiRead.sampleNum[0:minsamples], rpiRead.cpuTemp[0:minsamples], 'tab:blue')
        axs[0].plot(rpiCompare.sampleNum[0:minsamples], rpiCompare.cpuTemp[0:minsamples], 'tab:red')

        axs[1].plot(rpiRead.sampleNum[0:minsamples], rpiRead.cpuLoad[0:minsamples], 'tab:blue')
        axs[1].plot(rpiCompare.sampleNum[0:minsamples], rpiCompare.cpuLoad[0:minsamples], 'tab:red')
        axs[2].plot(rpiRead.sampleNum[0:minsamples], rpiRead.memPerc[0:minsamples], 'tab:blue',label="No Offloading")
        axs[2].plot(rpiCompare.sampleNum[0:minsamples], rpiCompare.memPerc[0:minsamples], 'tab:red', label="Offloading")
        axs[2].legend(loc='center right')
        axs[2].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x))))

        for index, ax in enumerate(axs.flat):
            if index == 2:
                ax.set(xlabel='Sample', ylabel=ylabels[index])
            else:
                ax.set(ylabel=ylabels[index])

        every_nth = 10
        for ax in axs.flat:
            for n, label in enumerate(ax.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)

    plt.savefig("./rpidata/AllResults"+str(testReadNum)+".png")

    # for i in range(len(plotArray)):
    #     figList[i] = plt.figure()
    #     axList[i] = figList[i].add_subplot(111)
    #     workingArray = plotArray[i]
    #     axList[i].plot(rpiRead.sampleNum, workingArray)
    #     axList[i].set_xlabel("Time [s]")
    #     axList[i].set_ylabel(ylabels[i])
    #     axList[i].set_title(titleArray[i])

    # Read number of processes in process log and how often each process is run
    processArray = []
    cprocessArray = []

    with open(fullProcessName, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) # skip header
        for row in csv_reader:
            processArray.append(row)

    with open(fullcprocessFileName, newline='') as xcsvfile:
        csv_reader = csv.reader(xcsvfile)
        next(csv_reader) # skip header
        for row in csv_reader:
            cprocessArray.append(row)

    # Plot total number of processes for each sample on bar graph
    xTotalList = []
    yTotalList = []

    for i in range(len(processArray)):
        yTotalList.append(len(processArray[i]))
        xTotalList.append(i+1)

    cxTotalList = []
    cyTotalList = []

    for i in range(len(cprocessArray)):
        cyTotalList.append(len(cprocessArray[i]))
        cxTotalList.append(i+1)

    # Do trimming

    if len(cxTotalList) < len(xTotalList):
        xTotalList = xTotalList[0:len(cxTotalList)-1]
        yTotalList = yTotalList[0:len(cyTotalList) - 1]
    else:
        cxTotalList = cxTotalList[0:len(xTotalList)-1]
        cyTotalList = cyTotalList[0:len(yTotalList) - 1]


    totalFig = plt.figure()
    totalAx = totalFig.add_subplot(211)
    totalAx.bar(xTotalList, yTotalList,label="No Offloading")
    totalAx.set_ylabel("Total # Processes")
    totalAx.set_title("Comparison of Total System Processes")
    totalAx.set_ylim(min(yTotalList) - 10, max(yTotalList) + 10)
    totalAx.legend(loc='best')

    ctotalAx = totalFig.add_subplot(212)
    ctotalAx.bar(cxTotalList, cyTotalList,color='r',label="Offloading")
    ctotalAx.set_xlabel("Sample Number")
    ctotalAx.set_ylabel("Total # Processes")
    ctotalAx.set_ylim(min(cyTotalList) - 10, max(cyTotalList) + 10)
    ctotalAx.legend(loc='best')

    plt.show()
    plt.savefig("./CS6604Project/rpidata/totalProcesses" + str(testReadNum) + ".png")

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

    plt.savefig("./CS6604Project/rpidata/totalOccurances" + str(testReadNum) + ".png")

    # plt.show()

    print("Done plotting data!")

