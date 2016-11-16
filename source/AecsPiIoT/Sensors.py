import datetime

''' 
    SensorInfo types
    -   onewireonboardds18b20
    aecs@pidev
'''
  

#class SensorInfo(object):
class SensorInfo():
    def __init__(self, id=int, type=str):
        self.id = id
        self.type = type
        self.typeData = None
        self.enable = False #   Shod sensor be in use or not
        self.name = "null"
        self.info = "null"
        self.isWorking = True   #   if read error from sensor – turn this to false
        self.collectTime = 0    #   How often shod the value be read
        self.collectValueTimer = 0  #   How long time it takes to read value
        self.LastChecked = datetime  #  When was is last checked (value read) datetime.datetim.utcnow
        self.saveRealTimeToDatabase = False
        self.saveHistoryToDatabase = False
        
        #self.typeOneWireOnBoardDs18b20 = OneWireOnBoardDs18b20Class

    def GetValue(self):
        if self.type == "onewireonboardds18b20":
            return self.typeData.temp
        else:
            return None
        


        
class OneWireOnBoardDictClass(object):
    def __init__(self, id=int):
        self.id = id        

class OneWireOnBoardDs18b20Class(object):
    def __init__(self, romid=str, health=None, temp=None, status=None, existInFolder=True):
        self.romid = romid
        self.health = health
        self.temp = temp
        self.status = status    #   Status for the sensor [ missing, crc-error, ok ]
        self.existInFolder = existInFolder  #   Do local folder exist for this sensor


class SensorTempTest1Class(object):
    def __init__(self, id = None, status = None, name = None):
        self.id = id
        self.status = status
        self.bane = name
