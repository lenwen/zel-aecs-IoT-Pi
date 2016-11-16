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
            self.Info("board-Onewire| While running")

            #   Do onewire folder need to be scanned
            if time.time() - FolderScanLastTime > 60:   #TODO   move folder scan time to database settings
                self.getFoldersToScan()
                FolderScanLastTime = time.time()
            
            
            #   forech onewire senor in sensorOneWireOnBoardDs18b20Dict
            for oneWire in sensorOneWireOnBoardDs18b20Dict:
                # returnId, returnStatus, returnTemp = self.readSensorData(sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.romid)
                #timeStarted = time.time()
                
                if (datetime.datetime.utcnow() - Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].LastChecked).total_seconds() >= Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].collectTime:
                    #   Denna sensors behövs läsa ett nytt värde ifrån

                    timeStarted = datetime.datetime.utcnow()
                    returnId, returnStatus, returnTemp = self.readSensorData(Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.romid)
                    if returnStatus is "ERROR":
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.status = "missing"
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].isWorking = False
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.existInFolder = False
                        #oneWire.status = "missing"
                    if returnStatus is "ERROR-CRC":
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.status = "crc-error"
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].isWorking = False
                    if returnStatus is "OK":
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.status = "ok"
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].LastChecked = datetime.datetime.utcnow() # time.time()
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].isWorking = True
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.existInFolder = True
                        Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].typeData.temp = returnTemp
                        self.Info("RomeId:" + str(oneWire) + " Value: " + str(returnTemp))
                
                    Settings.sensors[sensorOneWireOnBoardDs18b20Dict[oneWire].id].collectValueTimer = (datetime.datetime.utcnow() - timeStarted).total_seconds()  # time.time() - timeStarted
                #sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.temp = returnTemp
            
            #   Time to wait befor next run    
            time.sleep(float(Settings.OnBoardOneWireWaitBetweenRun))
            # time.sleep(Settings.OnBoardOneWireWaitBetweenRun)
            
            

        self.running = False;
        #return super().run()
    
        #   Get OnBoard One-wire devices
    def getFoldersToScan(self):
        
        self.Info("----> OneWire-Onboard Folder Scan is starting <----")
        folders = glob.glob(Settings.dir_OneWireOnBoard + '28*')
        newRomeIdThatsNeedsToAdd = []

        for folder in folders:
            romeId = os.path.basename(folder)

            
            idAlredyExist = False
            
            #check if romeid exist or not in list<romeid, OneWireOnBoardDictClass>
            if (romeId in sensorOneWireOnBoardDs18b20Dict):
                #   Rome id already exist in dict
                Settings.sensors[sensorOneWireOnBoardDs18b20Dict[romeId].id].typeData.existInFolder = True
                # sensorOneWireOnBoardDs18b20Dict[romeId].enable = True
                idAlredyExist = True
            else:
                #   Sensor dont exist in Sensor information data. Add information.
                newRomeIdThatsNeedsToAdd.append(romeId)

        #   Do romid exist on device list<newRomeIdThatsNeedsToAdd>
        if newRomeIdThatsNeedsToAdd != None:

            
            conn = sqlite3.connect(Settings.dbfilename)
            
            for NewRomeId in newRomeIdThatsNeedsToAdd:
                self.Info("Found OnBoard-OneWire Ds18b20 sensor. RomeId: " + NewRomeId)
                
                tmpDs18b20 = OneWireOnBoardDs18b20Class(romeId,0,"-999", 0,"found")
                tmpDs18b20.existInFolder = True

                c = conn.cursor()
                c.execute("select id, name,info,enable,isworking,collectvaluetime,saverealtimetodatabase,savehistorytodatabase, sensorvalue1 from tblsensors where type = 'onewireonboardds18b20' and tag = '{rid}'".format(rid=NewRomeId))
                tmpRowData =  c.fetchone()
                # tmpRowData =  c.fetchall()
                
                #   Do romeId exist in database?
                if tmpRowData is None:      #   Sensor dont exist in database
                    
                    self.Info("This is a new sensor that dont exist in database")
                    
                    #   Add information to database
                    self.Info("Adding to database")
                    sqlInsert = "insert into tblsensors (type,tag,name,info,enable,isworking,collectvaluetime,saverealtimetodatabase,savehistorytodatabase, sensorvalue1, sensorvalue2) VALUES('onewireonboardds18b20', '{romeId}', 'new', 'new', 1, 0, 60, 0, 0, '-999', 0)".format(romeId=NewRomeId)
                    c.execute(sqlInsert)
                    #c.execute("insert into tblsensors (type,tag,name,info,enable,isworking,collectvaluetime,saverealtimetodatabase,savehistorytodatabase, sensorvalue1, sensorvalue2) VALUES('onewireonboardds18b20', ?, 'new', 'new', 1, 1, 60, 0, 0, -999, 0);", (NewRomeId))
                    newSensorId = c.lastrowid
                    conn.commit()
                    self.Info("Id: {lineId}  - RomeId: {lindeRid}".format(lineId=newSensorId, lindeRid=NewRomeId))
                    #self.Info("ddddd")
                    
                    #   Add information to settings sensor

                    #   Create OneWireOnBoardDs18b20Class
                    self.Info("Adding information to settings sensor information")
                    sensordata = SensorInfo(newSensorId,"onewireonboardds18b20")
                    sensordata.typeData = OneWireOnBoardDs18b20Class(NewRomeId,0,-999,"ok",True)
                    sensordata.enable = True
                    sensordata.name = "new"
                    sensordata.info = "new"
                    sensordata.isWorking = False
                    sensordata.collectTime = 60
                    sensordata.collectValueTimer = 0
                    sensordata.LastChecked = datetime.datetime.utcnow() - datetime.timedelta(minutes=60) # datetime.datetime.utcnow()
                    sensordata.saveRealTimeToDatabase = False
                    sensordata.saveHistoryToDatabase = False
                    
                    Settings.sensors[newSensorId] = sensordata

                    #   add information to sensorOneWireOnBoardDs18b20Dict
                    self.Info("Add romeId to onboardOneWire dict")
                    sensorOneWireOnBoardDs18b20Dict[NewRomeId] = OneWireOnBoardDictClass(newSensorId)


                else:       #   Sensor already exist inside database
                    self.Info(NewRomeId + "  Already exist inside database")
                    #   id  name    info    enable  isworking   collectvaluetime    saverealtimetodatabase  savehistorytodatabase   sensorvalue1
                    #   0   1       2       3       4           5                   6                       7                       8
                    self.Info("Adding information to settings sensor information")
                    sensordata = SensorInfo(tmpRowData[0],"onewireonboardds18b20")
                    sensordata.typeData = OneWireOnBoardDs18b20Class(NewRomeId,0,tmpRowData[8],"ok",True)
                    if tmpRowData[3] == 1:
                        sensordata.enable = True
                    else:
                        sensordata.enable = False

                    sensordata.name = tmpRowData[1]
                    sensordata.info = tmpRowData[2]
                    sensordata.isWorking = False
                    sensordata.collectTime = tmpRowData[5]
                    sensordata.collectValueTimer = 0
                    sensordata.LastChecked = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
                    sensordata.saveRealTimeToDatabase = False   #todo fix this
                    sensordata.saveHistoryToDatabase = False    #todo fix this
                    
                    Settings.sensors[tmpRowData[0]] = sensordata

                    #   add information to sensorOneWireOnBoardDs18b20Dict
                    self.Info("Add romeId to onboardOneWire dict")
                    sensorOneWireOnBoardDs18b20Dict[NewRomeId] = OneWireOnBoardDictClass(tmpRowData[0])

                    #rowId = tmpRowData[0]
                    #rowName = tmpRowData["name"]
                    self.Info("sdfsdf")

                #print("sdfdsf")

            
            #sensordata = SensorInfo(0,"onewireonboardds18b20")
            #sensordata.enable = True
            #sensordata.typeOneWireOnBoardDs18b20 = tmpDs18b20
            #sensorOneWireOnBoardDs18b20Dict[romeId] = sensordata

                #lid = cur.lastrowid

                #sensorOneWireOnBoardDs18b20Dict[romeId] = 
            #for oneWire in sensorOneWireOnBoardDs18b20List:
            #for oneWire in sensorOneWireOnBoardDs18b20Dict:
            #    if id in oneWire.romid:
            #        idAlredyExist = True
            
            #if idAlredyExist is False:
            #        # this id dont exist. add this id
            #        sensorOneWireOnBoardDs18b20List.append(SensorOneWireDs18b20Class(0,id,0,"-999",0,"new","new","new"))
        #Debug.Info("########")

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

    def Info(self, Text):
        Debug.Info("OnBoardOneWire | {text}".format(text=Text))

    def Warning(self, Text):
        Debug.Warning("OnBoardOneWire | {text}".format(text=Text))    
    
    def Error(self, Text):
        Debug.Error("OnBoardOneWire | {text}".format(text=Text))

