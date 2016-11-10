class ShuntClass(object):
    ShuntShodBeRunning = False
    ShuntIsRunning = False
    ShuntWaitBetweenRun = 5
    ShuntData = {}  #   All shunts in system. Dict <ShuntId (int), ShuntDataClass (class)>


class ShuntDataClass(object):
    """description of class"""
    def __init__(self, id=int, name = str):
        self.id = id
        self.name = name
        self.info = None
        self.enable = False
        self.mode = 1
        self.cirkPumpRelayId = 0
        self.tempUpRelayId = 0
        self.tempDownRelayId = 0
        self.tempInSensorId = 0
        self.tempOutSensorId = 0
        self.tempReturnSensorId = 0
        self.shuntPosistionValue = 0
        self.tempWantToHave = 0





