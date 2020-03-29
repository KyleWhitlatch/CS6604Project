
import csv
import matplotlib.pyplot as plt
from itertools import count
import statistics

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

    testReadNum = 1
    filename = "piTestRecord" + str(testReadNum) + ".csv"
    fullFileName = "./rpidata/" + filename

    ###########################
    # Change name for plotting here:
    name = "Testing"
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

    # Read number of processes in process

    plt.show()


    print("Done plotting data!")

