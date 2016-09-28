''' 
    SensorInfo types
    -   onewireonboardds18b20
'''

class SensorInfo(object):
    def __init__(self, id=int, type=str):
        self.id = id
        self.type = type
        self.enable = False
        self.name = "null"
        self.info = "null"
        self.enable = True
        self.isWorking = True
        self.collectValueTime = 0
        self.saveRealTimeToDatabase = 0
        self.saveHistoryToDatabase = 0
        self.typeOneWireOnBoardDs18b20 = OneWireOnBoardDs18b20Class
        
        

class OneWireOnBoardDs18b20Class(object):
    def __init__(self, romid=str, health=None, temp=None, lastchecked=None, status=None):
        self.romid = romid
        self.health = health
        self.temp = temp
        self.lastchecked = lastchecked
        self.status = status


class SensorTempTest1Class(object):
    def __init__(self, id = None, status = None, name = None):
        self.id = id
        self.status = status
        self.bane = name
