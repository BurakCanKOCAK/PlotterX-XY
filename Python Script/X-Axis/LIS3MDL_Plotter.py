#Author      : ILiM - LI
#Date        : 12-03-2018
#Description : LIS3MDL magnetic sensor plotter

import serial
from drawnow import *
import atexit

##############################################

comPort = 'COM17'
baudRate = 9600
points2Show = 500
#################
minEmptyParkingRangeVal = -970
maxEmptyParkingRangeVal = -720
##############################################
values = []
plt.ion()
cnt = 0

serialArduino = serial.Serial(comPort, baudRate)


def plotValues():
    plt.title('Serial value from Arduino')
    plt.grid(True)
    plt.ylabel('Values')
    plt.plot(values, 'rx-', label='values')
    plt.legend(loc='upper right')
	plt.ylim(-4, +4)


def doAtExit():
    serialArduino.close()
    print("Close serial")
    print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))


atexit.register(doAtExit)

print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))

# pre-load dummy data
for i in range(0, points2Show):
    values.append(0)

while True:
    while (serialArduino.inWaiting() == 0):
        pass
    #print("readline()")
    valueRead = serialArduino.readline(500)
    try:
        valueRead =valueRead.decode("utf-8").replace('\r\n','')
    except:
        pass

    try:
        valueReadList = valueRead.split(" ")
        if not valueReadList[0]:
            valueRead=valueReadList[1]
        else:
            valueRead=valueReadList[0]
        #Get X Value
        valueRead = valueReadList[0]

        if float(valueRead)<maxEmptyParkingRangeVal and float(valueRead)>minEmptyParkingRangeVal:
            print("Parking Empty")
        else:
            print("Occupied")
    except:
        pass

    # check if valid value can be casted
    try:
        valueInInt = float(valueRead)
        #print(valueInInt)
        if valueInInt <= 500000:
            values.append(valueInInt)
            values.pop(0)
            drawnow(plotValues)
        else:
            print("Invalid! too large")
    except ValueError:
        print("Invalid! cannot cast"+ str(valueRead))
