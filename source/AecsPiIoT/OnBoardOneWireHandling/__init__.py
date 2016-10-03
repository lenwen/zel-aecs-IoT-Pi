import threading
import time
import datetime
import glob
import sqlite3
import os

from Settings import Settings
from Debug import Debug
from Sensors import OneWireOnBoardDs18b20Class, SensorInfo

#   Dict sensors ds18b20
#   dict< romeId (string), class>


#sensorOneWireOnBoardDs18b20Dict = {str, SensorInfo}
sensorOneWireOnBoardDs18b20Dict = {}

class OnBoardOneWireHandling (threading.Thread):
    

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        #self.running = False;
        self.dbcon = None

    def run(self):
        #   Database connection.
        self.dbcon = sqlite3.connect(Settings.dir_ConfigFiles + "aecs.db")
        #global sensorOneWireOnBoardDs18b20List
        #self.running = True;
        Settings.OnBoardOneWireIsRunning = True

        FolderScanLastTime = 0;
        while(Settings.OnBoardOneWireIsRunning):
            Debug.Info("board-Onewire| While running")

            #print("running!!!!")
            if time.time() - FolderScanLastTime > 60:
                self.getFoldersToScan()
                FolderScanLastTime = time.time()
            
            #for oneWire in sensorOneWireOnBoardDs18b20List:
            
            for oneWire in sensorOneWireOnBoardDs18b20Dict:
                returnId, returnStatus, returnTemp = self.readSensorData(sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.romid)
                if returnStatus is "ERROR":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "missing"
                    #oneWire.status = "missing"
                if returnStatus is "ERROR-CRC":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "crc-error"                    
                if returnStatus is "OK":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "OK"
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = time.time()
                    Debug.Info("RomeId:" + str(oneWire) + " Value: " + str(returnTemp))
                
                sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.temp = returnTemp
            
            #   Time to wait befor next run    
            time.sleep(float(Settings.OnBoardOneWireWaitBetweenRun))
            # time.sleep(Settings.OnBoardOneWireWaitBetweenRun)
            
            

        self.running = False;
        #return super().run()
    
    def getFoldersToScan(self):
        #global sensorOneWireOnBoardDs18b20List, dir_OneWireOnBoard
        folders = glob.glob(Settings.dir_OneWireOnBoard + '28*')
        for folder in folders:
            romeId = os.path.basename(folder)
            #check if id exist or not in list
            idAlredyExist = False
            if (romeId in sensorOneWireOnBoardDs18b20Dict):
                #   Rome id already exist in dict
                sensorOneWireOnBoardDs18b20Dict[romeId].enable = True
                idAlredyExist = True
            else:
                #   Sensor dont exist in local dict. Add the sensor
                tmpDs18b20 = OneWireOnBoardDs18b20Class(romeId,0,"-999", 0,"found")
                sensordata = SensorInfo(0,"onewireonboardds18b20")
                sensordata.enable = True
                sensordata.collectValueTime = 5
                sensordata.typeOneWireOnBoardDs18b20 = tmpDs18b20
                sensorOneWireOnBoardDs18b20Dict[romeId] = sensordata

                #lid = cur.lastrowid

                #sensorOneWireOnBoardDs18b20Dict[romeId] = 
            #for oneWire in sensorOneWireOnBoardDs18b20List:
            #for oneWire in sensorOneWireOnBoardDs18b20Dict:
            #    if id in oneWire.romid:
            #        idAlredyExist = True
            
            #if idAlredyExist is False:
            #        # this id dont exist. add this id
            #        sensorOneWireOnBoardDs18b20List.append(SensorOneWireDs18b20Class(0,id,0,"-999",0,"new","new","new"))

    def readSensorData(self, sensorRomeId):
        text = '';
        sensorReadingStartTime = time.time()
        #TODO   See if sensor is stile online

        try:
            while text.split("\n")[0].find("YES") == -1:
                tfile = open(Settings.dir_OneWireOnBoard + sensorRomeId +"/w1_slave")
                text = tfile.read()
                tfile.close()
                time.sleep(0.2)
                #if time.time() - sensorReadingStartTime > Settings.sensorOneWireOnBoardDs18b20CrcWaitingTime:
                if time.time() - sensorReadingStartTime > float(Settings.OnBoardOneWireSensorDs18b20CrcWaitingTime):
                    #   This sensor have not got CRC = YES in more then x sec now.
                    return sensorRomeId,"ERROR-CRC", -999
                #time.sleep(1)
            secondline = text.split("\n")[1]
            temperaturedata = secondline.split(" ")[9]
            temperature = float(temperaturedata[2:])
            temperatures = (temperature / 1000)
            return sensorRomeId,"OK", temperatures
        except:
            return sensorRomeId,"ERROR", -999

    def stop(self):
        Settings.OnBoardOneWireIsRunning = False
    

