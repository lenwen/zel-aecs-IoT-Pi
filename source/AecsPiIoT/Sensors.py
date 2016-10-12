''' 
    SensorInfo types
    -   onewireonboardds18b20
'''

class SensorInfo(object):
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
        self.saveRealTimeToDatabase = 0
        self.saveHistoryToDatabase = 0
        
        #self.typeOneWireOnBoardDs18b20 = OneWireOnBoardDs18b20Class
        
        

class OneWireOnBoardDs18b20Class(object):
    def __init__(self, romid=str, health=None, temp=None, lastchecked=None, status=None, existInFolder=True):
        self.romid = romid
        self.health = health
        self.temp = temp
        self.lastchecked = lastchecked
        self.status = status    #   Status for the sensor [ missing, crc-error, ok ]
        self.existInFolder = existInFolder  #   Do local folder exist for this sensor


class SensorTempTest1Class(object):
    def __init__(self, id = None, status = None, name = None):
        self.id = id
        self.status = status
        self.bane = name
