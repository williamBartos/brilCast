import time
import Adafruit_DHT
import time
import datetime
import sys
import os
import requests
import math

import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure

sensor = Adafruit_DHT.DHT11
pin=3
ts = time.time()


def initializeSensors():
    
    dataDict = {}

    def cToF(t):
         return round( ( t*1.8 ) + 32, 1 )

    while True:
    
        tempFile = open("/sys/bus/w1/devices/28-0115a3fdfaff/w1_slave")
        output = tempFile.read()
        tempFile.close()
        temp = float(output[69:])/1000
        outTemp = cToF(temp)

  
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:

            inTemp = cToF(temperature)
            inHum = humidity
        

        else:
            print('Failed to grab reading. Try again')


        writeTime = datetime.datetime.now().replace(microsecond =0)

        dataDict['inTemp'] = inTemp
        dataDict['inHum'] = inHum
        dataDict['temp'] = outTemp
        dataDict['time'] = writeTime

        return dataDict

    


def runSensors():
    print("Running...")
    x = initializeSensors()
    dictToSend = x
    url = 'https://wbartos.pythonanywhere.com/add'
    res = requests.post(url, data = dictToSend)


            
          
runSensors()
    

