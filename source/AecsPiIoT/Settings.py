class Settings(object):
    version = '0.0.201609271808'
    osPlatform = ''
    osVersion = ''
    dir_OneWireOnBoard = '/sys/bus/w1/devices/'
    dir_ConfigFiles = '/etc/aecs/'
    dbfilename = ""
    #   Debug information
    debugEnable = True
    debugToConsole = True
    debugToFile = True
    debugfile = '/etc/aecs/debug.log'

    #   Sensor 1-Wire On Board settings
    sensorOneWireOnBoardDs18b20CrcWaitingTime = 5
    sensorOneWireOnBoardDs18b20MissingTime = 30

    #   All threads that is running in system
    threads = {}  

    #   All sensors in system
    #   Dict <sensorId (int), Sensorclass> 
    sensors = {}


    


