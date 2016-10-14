import threading
import time
import datetime
import glob
import sqlite3
import os

from Settings import Settings
from Debug import Debug
from Sensors import OneWireOnBoardDs18b20Class, SensorInfo, OneWireOnBoardDictClass

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

            #   Do onewire folder need to be scanned
            if time.time() - FolderScanLastTime > 60:   #TODO   move folder scan time to database settings
                self.getFoldersToScan()
                FolderScanLastTime = time.time()
            
            
            #   forech onewire senor in sensorOneWireOnBoardDs18b20Dict
            for oneWire in sensorOneWireOnBoardDs18b20Dict:
                returnId, returnStatus, returnTemp = self.readSensorData(sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.romid)
                if returnStatus is "ERROR":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "missing"
                    #oneWire.status = "missing"
                if returnStatus is "ERROR-CRC":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "crc-error"                    
                if returnStatus is "OK":
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "ok"
                    sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = time.time()
                    Debug.Info("RomeId:" + str(oneWire) + " Value: " + str(returnTemp))
                
                sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.temp = returnTemp
            
            #   Time to wait befor next run    
            time.sleep(float(Settings.OnBoardOneWireWaitBetweenRun))
            # time.sleep(Settings.OnBoardOneWireWaitBetweenRun)
            
            

        self.running = False;
        #return super().run()
    
        #   Get OnBoard One-wire devices
    def getFoldersToScan(self):
        
        Debug.Info("----> OneWire-Onboard Folder Scan is starting <----")
        folders = glob.glob(Settings.dir_OneWireOnBoard + '28*')
        newRomeIdThatsNeedsToAdd = []

        for folder in folders:
            romeId = os.path.basename(folder)

            #check if romeid exist or not in list<romeid, OneWireOnBoardDictClass>
            idAlredyExist = False
            

            if (romeId in sensorOneWireOnBoardDs18b20Dict):
                #   Rome id already exist in dict
                Settings.sensors[sensorOneWireOnBoardDs18b20Dict[romeId].id].typeData.existInFolder = True
                # sensorOneWireOnBoardDs18b20Dict[romeId].enable = True
                idAlredyExist = True
            else:
                #   Sensor dont exist in Sensor information data. Add information.
                newRomeIdThatsNeedsToAdd.append(romeId)

        if newRomeIdThatsNeedsToAdd != None:

            #   Do romeId exist in database?
            conn = sqlite3.connect(Settings.dbfilename)
            
            for NewRomeId in newRomeIdThatsNeedsToAdd:
                Debug.Info("Found OnBoard-OneWire Ds18b20 sensor. RomeId: " + NewRomeId)
                
                tmpDs18b20 = OneWireOnBoardDs18b20Class(romeId,0,"-999", 0,"found")
                tmpDs18b20.existInFolder = True

                c = conn.cursor()
                c.execute("select * from tblsensors where type = 'onewireonboardds18b20' and tag = '{rid}'".format(rid=NewRomeId))
                tmpRowData =  c.fetchall()
                if tmpRowData == None:
                    #   Sensor dont exist in database
                    Debug.Info("This is a new sensor that dont exist in database")
                    Debug.Info("Adding to database")
                    c.execute("insert into tblsensors (type,tag,name,info,enable,isworking,collectvaluetime,saverealtimetodatabase,savehistorytodatabase, sensorvalue1, sensorvalue2) VALUES();")
                    #   Add information to database
                    #   Add information to settings sensor
                    #   add information to sensorOneWireOnBoardDs18b20Dict
                else:
                    #   Sensor already exist inside database
                    Debug.Info(NewRomeId + "Already exist inside database")
                print("sdfdsf")

            
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
        Debug.Info("########")

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
    

