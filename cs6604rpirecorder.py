import psutil
import csv
import os,sys
from itertools import count
import time

class rpiData:

    def __init__(self, name):
        self.name = name
        self.index = count()
        self.sampleNum = []
        self.memArray = []
        self.cpuTemp = []
        self.cpuLoad = []
        self.processArray = []
        self.rowCnt = 0


def get_cpu_temperature():
    """
    Get CPU temperature.
    """
    try:

        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0

        return str(temp)
    except:
        return str(0.00)

def doMainRecordLoop(rpiData):
    # Create main while loop to get psutil data

    try:
        while True:
            print("Running main recording loop!")
            # Record Sample Number
            rpiData.sampleNum.append(next(rpi3Data.index))

            # Get current availible memory string
            currMem = psutil.virtual_memory()
            availibleMem = round(currMem.used/1024.0/1024.0,1)
            totalMem = round(currMem.total/1024.0/1024.0,1)
            memPerc = currMem.percent
            memStr = "Used: " + str(availibleMem) +"/" +str(totalMem) + " ("+str(memPerc)+")"
            rpiData.memArray.append(memStr)

            # Get CPU Temp
            # Using different function for cpu temp
            rpiData.cpuTemp.append(get_cpu_temperature()) # Only works on raspberry pi

            # Get CPU Load
            rpiData.cpuLoad.append(str(psutil.cpu_percent(percpu=False)))

            # Get process log
            pidsList = []
            pidsString = ""
            procs = {p.pid: p.info for p in psutil.process_iter(['pid','name'])}
            for i,j in procs.items():
                pidsString = "(" + str(i) + ") " + str(j['name'])
                pidsList.append(pidsString)
            rpiData.processArray.append(pidsList)

            time.sleep(1)
            
    except KeyboardInterrupt:
        pass

    strcwd = str(os.getcwd())
    global testnum
    print("Stopped!")

    # Write collected data to csv
    filename = strcwd + "/rpidata/piTestRecord" + str(testnum) + ".csv"
    print("Recording data in :" + strcwd + "/rpidata")

    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SN", "CPU Temp. [C]", "CPU % Load","Virtual Memory [mB] (%)"])
        for i in range(len(rpiData.sampleNum)):
            writer.writerow([rpiData.sampleNum[i], rpiData.cpuTemp[i],rpiData.cpuLoad[i],rpiData.memArray[i]])

    plname = strcwd + "/rpidata/piTestRecord" + str(testnum) + "pl" + ".csv"

    with open(plname, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PROCESS LOG:"])
        for sublist in rpiData.processArray:
            writer.writerow(sublist)
    

if __name__ == "__main__":
    print("Starting CS 6604 data recorder!")
    global testnum
    testnum = input("Test Number:")
    rpi3Data = rpiData("RaspPi3Data")
    doMainRecordLoop(rpi3Data)
