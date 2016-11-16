class Settings(object):
    version = '0.0.201609271808'
    versionNice = 'Version 0.0 Build x'
    osPlatform = ''
    osVersion = ''
    rpi_Revision = "-99"  # Possible answers are 0 = Compute Module, 1 = Rev 1, 2 = Rev 2, 3 = Model B+/A+
    runningOnRaspberry = False

    #   Node information
    nodeName = "aecs"

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

    #   Webserver settings
    webSitePort = 80    #todo   get this value from database

    #   Sensor 1-Wire On Board settings
    OnBoardOneWireIsRunning = False
    OnBoardOneWireShodBeRunning = False
    OnBoardOneWireWaitBetweenRun = 2
    OnBoardOneWireSensorDs18b20CrcWaitingTime = 5
    OnBoardOneWireSensorDs18b20MissingTime = 30

    #   Shunt settings
    ShuntPluginEnable = False
    shunt = None
    # ShuntData = {}  #   All shunts in system. Dict <ShuntId (int), ShuntData (class)>

    #   built in fan control
    FanControllEnable = True
    FanInitDone = False
    FanPwmData = None
    FanRunValueLowestforTurnOff = 20
    FanRunValueHighestAllow = 100
    FanPwmBcmId = 18
    FanFrequency = 100
    FanStartValue = 20
    FanTempSensorId = 1001
    FanTempStartValue = 22
    FanTempValueDoMaxRunValue = 35
    FanTempValueNow = 0
    FanTempValueOld = 0
    


    #   Security information
    keyAccess = "jdiieh39sa"

    #   All threads that is running in system
    threads = {}  

    #   All sensors in system
    #   Dict <sensorId (int), SensorInfo (class)> 
    sensors = {}

    #   All relay in system
    #   Dict <relayId (int), relayHandling (class)>
    relays = {}
    

    # aecs@pidev

