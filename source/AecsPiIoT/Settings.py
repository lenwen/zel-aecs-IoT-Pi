class Settings(object):
    version = '0.0.201609271808'
    osPlatform = ''
    osVersion = ''
    dir_OneWireOnBoard = '/sys/bus/w1/devices/'
    dir_ConfigFiles = '/etc/aecs/'
    dbfilename = ""
    dbVersion = 0
    #   Debug information
    debugForceFromCmd = False
    debugEnable = False
    debugToConsole = False
    debugToFile = False
    debugfile = '/etc/aecs/debug.log'

    ApplicationShodEnd = False

    #   Sensor 1-Wire On Board settings
    OnBoardOneWireIsRunning = False
    OnBoardOneWireShodBeRunning = False
    OnBoardOneWireWaitBetweenRun = 10
    OnBoardOneWireSensorDs18b20CrcWaitingTime = 5
    OnBoardOneWireSensorDs18b20MissingTime = 30

    #   All threads that is running in system
    threads = {}  

    #   All sensors in system
    #   Dict <sensorId (int), Sensorclass> 
    sensors = {}


    

    # aecs@pidev

