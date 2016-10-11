import time
import datetime
import glob
import signal
import sys
import os

sensorOneWireOnBoardDs18b20Dict = {}

class OneWireOnBoardDs18b20Class(object):
    def __init__(self, romid=str, health=None, temp=None, lastchecked=None, readtime=None, status=None, enable=False):
        self.romid = romid
        self.health = health
        self.temp = temp
        self.lastchecked = lastchecked
        self.readtime = readtime
        self.status = status
        self.enable = enable

RunSoftware = True

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    RunSoftware = False
    sys.exit(0)




#   Allow CTRL + c to shutdown the system
signal.signal(signal.SIGINT, signal_handler)

def readSensorData(sensorRomeId):
        text = '';
        sensorReadingStartTime = time.time()
        #TODO   See if sensor is stile online

        try:
            while text.split("\n")[0].find("YES") == -1:
                tfile = open("/sys/bus/w1/devices/" + sensorRomeId +"/w1_slave")
                text = tfile.read()
                tfile.close()
                time.sleep(0.2)
                #if time.time() - sensorReadingStartTime > Settings.sensorOneWireOnBoardDs18b20CrcWaitingTime:
                #if time.time() - sensorReadingStartTime > float(Settings.OnBoardOneWireSensorDs18b20CrcWaitingTime):
                if time.time() - sensorReadingStartTime > 20:
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

def setSensorStatusEnableFalse():
    #   Set all temp sensor as enable false
    for oneWire in sensorOneWireOnBoardDs18b20Dict:
        sensorOneWireOnBoardDs18b20Dict[oneWire].enable = False

def GetFolderInformation():
    #   Get folders
    folders = glob.glob('/sys/bus/w1/devices/28*')
    for folder in folders:
        romeId = os.path.basename(folder)
        #check if id exist or not in list
        idAlredyExist = False
        if (romeId in sensorOneWireOnBoardDs18b20Dict):
            #   Rome id already exist in dict
            sensorOneWireOnBoardDs18b20Dict[romeId].enable = True
        else:
            #   Hittade en ny temp sensor
            print("Found new Temp sensor: " + romeId)
            tmpds18b20 = OneWireOnBoardDs18b20Class(romeId,0,"-999", 0,0,"found", True)
            sensorOneWireOnBoardDs18b20Dict[romeId] = tmpds18b20
        
def main():
    os.system('modprobe w1-gpio')  # Turns on the GPIO module
    os.system('modprobe w1-therm') # Turns on the Temperature module
    
    while (RunSoftware):

        setSensorStatusEnableFalse()
        GetFolderInformation()
        for oneWire in sensorOneWireOnBoardDs18b20Dict:
            if sensorOneWireOnBoardDs18b20Dict[oneWire].enable is True:
                returnId, returnStatus, returnTemp = readSensorData(sensorOneWireOnBoardDs18b20Dict[oneWire].romid)
                if returnStatus is "ERROR":
                    print("Error when reading sensor: " + oneWire)
                    #sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "missing"
                    #oneWire.status = "missing"
                if returnStatus is "ERROR-CRC":
                    print("Error-CRC when reading sensor: " + oneWire)
                    #sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "crc-error"                    
                if returnStatus is "OK":
                    #sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = "OK"
                    #sensorOneWireOnBoardDs18b20Dict[oneWire].typeOneWireOnBoardDs18b20.status = time.time()
                    print("RomeId:" + str(oneWire) + " OK - Value: " + str(returnTemp))
                    #print("hej")
            else:
                print("RomeId:" + str(oneWire) + " Missing")
                #print("Sensor is missing!!")

        time.sleep(2)

         
           

if __name__ == "__main__":
    sys.exit(int(main() or 0))




