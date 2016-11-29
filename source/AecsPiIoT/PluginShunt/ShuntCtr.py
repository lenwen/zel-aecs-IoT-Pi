#import time
import datetime
from Settings import Settings
from Debug import Debug

#import glob



class ShuntCtr():
    """description of class"""
    def __init__(self, id=int, name = str):
        self.id = id
        self.name = name
        self.info = str
        self.enable = False
        self.mode = 1
        self.backgroundWorkIsRunning = False    # is there background work running for this shunt
        
        #   RelayId and SensorData
        self.cirkPumpRelayId = 0
        self.tempUpRelayId = 0
        self.tempDownRelayId = 0
        self.tempInSensorId = 0
        self.tempOutSensorId = 0
        self.tempReturnSensorId = 0

        self.shuntPosistionMax = 120
        self.shuntPosistionValue = 0

        #   Cirk pump information
        self.cirkPumpIsOn = False
        self.cirkPumpShodBeOn = False
        self.cirkPumpStartTime = 0 # Time when the pump was started. Datetime utc
        self.cirkPumpStartTimeBeforStartingShunt = 30       #   Time that pump shod run before shunt control is enable - Time in seconds

        self.tempWantToHave = 0

        #   Error codes
        self.ErrorMainInShunt = False
        self.ErrorWhitRelayId = False
        self.ErrorWhitTempOutSensorId = False

    def errorBuild(self):
        if (self.ErrorWhitRelayId):
            self.ErrorMainInShunt = True
        elif self.ErrorWhitTempOutSensorId:
            self.ErrorMainInShunt = True
        else:
            self.ErrorMainInShunt = False
         

    def run(self):
        
        self.debugInfo("Run() - Id: {0} - info: {1}".format(self.id, self.info))
        
        if (self.backgroundWorkIsRunning):
            #   background work is running. check status
            debugInfo("Background work is running")
            return

        if self.enable:
            
            #region   Read status  from cirk pump relay Id
            if (self.cirkPumpRelayId in Settings.relays):
                #   Cirk pump relay id exist
                self.debugInfo("cirk pump relay id exist")
                if (Settings.relays[self.cirkPumpRelayId].Data.IsOn):
                    self.cirkPumpIsOn = True
                else:
                    self.cirkPumpIsOn = False
            else:
                #   Cirk pump relay dont exist.
                self.ErrorWhitRelayId = True
                self.debugWarning("CirkPump relayId dont exist!!!")
                return
            #endregion

            #region     Check sensors id exist or not
            
            #   Do temp Out Sensor id exist ?
            if (self.tempOutSensorId in Settings.sensors):
                #   exist
                if (Settings.sensors[self.tempOutSensorId].isWorking):  #   Sensor have status working = true
                    #   check if sensors readvalue is good

                    #   Seconds ago it was last checkt
                    #print(datetime.datetime.utcnow())
                    #print(Settings.sensors[self.tempOutSensorId].LastChecked)

                    tmpTempatureOutLastCheckInSec = (datetime.datetime.utcnow() - Settings.sensors[self.tempOutSensorId].LastChecked).total_seconds()
                    #tmpdddd = tmpTempatureOutLastCheckInSec.total_seconds()
                    print("seconds ago last check: {}".format(tmpTempatureOutLastCheckInSec))
                else:
                    #   Status not working.
                    self.ErrorWhitTempOutSensorId = True
                    self.debugError("Temp sensor OUT is not working")
                    return

            else:
                # dont exist
                self.debugError("Temp sensor OUT dont exist")
                self.ErrorWhitTempOutSensorId = True
                return
            #endregion

            #region Turn cirk pump on or off
            if (self.cirkPumpIsOn):
                #   Cirk pumps is on
                self.debugInfo("Cirk pump is on")
                if not (self.cirkPumpShodBeOn):
                    self.debugInfo("CirkPump shod be off. Turn off the cirk pump")
                    Settings.relays[self.cirkPumpRelayId].TurnOff()
                    self.cirkPumpStartTime = 0
            else:
                #   Cirk pump is off
                self.debugInfo("Cirk pump is off")
                if (self.cirkPumpShodBeOn):
                    self.debugInfo("Cirkpump shod be on. Turning cirk punp on")
                    Settings.relays[self.cirkPumpRelayId].TurnOn()
                    self.cirkPumpStartTime = datetime.datetime.utcnow()

            #endregion


            if (datetime.datetime.utcnow() - self.cirkPumpStartTime).total_seconds() <= self.cirkPumpStartTimeBeforStartingShunt:
                self.debugInfo("Cirk pump is stile starting up")
                return


            #region Shit

            #tmpCirkPumpRunTime = datetime.datetime.utcnow() - self.cirkPumpStartTime
            #print(tmpCirkPumpRunTime.seconds)
            #total_seconds()

            #divmod(tmpCirkPumpRunTime.tot
            #if ( tmpCirkPumpRunTime.total_seconds() <= self.cirkPumpStartTime):

            #endregion



            



            tempOutNow = None
            #   Get value what the shunt is right now
            if (self.tempOutSensorId in Settings.sensors):
                #   Sensor Id exist. read value
                tempOutNow = Settings.sensors[self.tempOutSensorId].GetValue()
                self.debugInfo("Temp out now: {}".format(tempOutNow))
            else:
                #   SensorId dont Exist
                self.debugWarning("Sensor Id dont exist!!!")

        else:
            self.debugWarning("Shunt id {} is not enable. Turn off power".format(self.id))
            #todo   chech that every relay is turn off that this shunt is using

        self.debugInfo("Run() - Id: {} -- done".format(self.id))

    def stop(self):
        self.debugInfo("Turn off Shunt")

    def debugInfo(self, Text):
        Debug.Info("Shunt {id} Ctr | {text}".format(id=self.id, text=Text))

    def debugWarning(self, Text):
        Debug.Warning("Shunt {id} Ctr | {text}".format(id=self.id, text=Text))
    
    def debugError(self, Text):
        Debug.Error("Shunt {id} Ctr | {text}".format(id=self.id, text=Text))