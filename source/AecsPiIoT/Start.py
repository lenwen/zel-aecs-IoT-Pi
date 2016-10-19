#Enable when running debug on raspberry pi

#GPIO = None
import RPi.GPIO as GPIO

#try:
    
#except RuntimeError:
#    print("Gpio error")


import io
import os
import time
import datetime
import sys
import threading
import signal
import glob
import platform
#from __builtin__ import str, int
from warnings import catch_warnings
from _ast import Str

from Settings import Settings
from DatabaseHandling import Database
from Debug import Debug
from RelayHandling import RelayHandling,RelaysDataClass, GPIO

import OnBoardOneWireHandling
import FlaskWeb

from multiprocessing import Process

commandline = sys.argv
vsDebug = False

#   Read and set CommandLine arguments
for cmd in sys.argv:
    cmdLower = cmd.lower()
    #print(cmdLower)
    if cmdLower == "debugtoconsole":
        Settings.debugToConsole = True
        Settings.debugEnable = True
        Settings.debugForceFromCmd = True
    elif cmdLower == "debugtofile":
        Settings.debugToFile = True
        Settings.debugEnable = True
        Settings.debugForceFromCmd = True
    elif cmdLower == "vs":
        vsDebug = True
        Settings.debugForceFromCmd = True
    #elif cmdLower == @"c:\users\lennie\source\repos\zel-aecs-iot-pi\source\aecspiiot\start.py":
    #    print("Running on vs local")

#    elif cmdLower != "start.py":
    elif cmdLower.endswith("start.py"):
        tmpdd = ""
        #print("dd")
    else:
        print(cmdLower)
        print("Error in starting values\nApplication will exit!")
        sys.exit(0)

#    else:

# c:\users\lennie\source\repos\zel-aecs-iot-pi\source\aecspiiot\start.py

#   if this is Vs debug on Ptvsd. init ptvsd and wait for debug connection
if vsDebug:
    import ptvsd
    ptvsd.enable_attach('aecs')
    Settings.debugEnable = True
    Settings.debugToConsole = True
    Debug.Info("Waiting for debug init - 60 sek")
    ptvsd.wait_for_attach(60)


if Settings.debugToConsole or Settings.debugToFile:
    Debug.Info("Debug is turn on from commandline")
    if (Settings.debugToFile):
        Debug.Info("Debug to file: " + Settings.debugfile)




def shutDown():
    Debug.Info ("Stop all runnings threads")
    for t in Settings.threads:
        print('Thead: ' + str(Settings.threads[t].getName()) + ' will now stop()')
        Settings.threads[t].stop()
       
    Debug.Info("Wait 5 sec for threads to end")
    time.sleep(2);

    #test1 = Process(Settings.threads["website"])
    #test1.terminate()

    Debug.Info("Threads are joining before exit")
    for t in Settings.threads:
        # Settings.threads[t].terminate()
        Settings.threads[t].join()
    sys.exit(0)

def signal_handler(signal, frame):
    Debug.Info ('You pressed Ctrl+C!')
    shutDown()

#   On Board 1-Wire Init
def OnBoardOneWireInit():
    if (Settings.OnBoardOneWireIsRunning):
        if (Settings.OnBoardOneWireShodBeRunning == False):
            #   On Board One Wire is running. but i shod NOT be running
            Settings.threads["onboardOneWire"].stop()
    else:
        if (Settings.OnBoardOneWireShodBeRunning):
            #   On board One Wire shod be running.
            if ("onboardOneWire" in Settings.threads):
                #   onboard One Wire is already init
                if (Settings.OnBoardOneWireIsRunning == False):
                    #   The thread is not running. start the Thread.
                    Settings.threads["onboardOneWire"].run()
            else:
                #   Not init. do init
                os.system('modprobe w1-gpio')  # Turns on the GPIO module
                os.system('modprobe w1-therm') # Turns on the Temperature module
                thOnBoardOneWireHandling = OnBoardOneWireHandling.OnBoardOneWireHandling("onboardOneWire","1-wire onboard",2)
                # thOnBoardOneWireHandling = OnBoardOneWireHandling.OnBoardOneWireHandling("onboardOneWire","1-wire onboard",2)
                
                                                                  
                thOnBoardOneWireHandling.start();
                Settings.threads["onboardOneWire"] = thOnBoardOneWireHandling
def WebSiteInit():
    thWebSite = FlaskWeb.WebSite("website")
    thWebSite.start()
    Settings.threads["website"] = thWebSite

def GetPlatformRunningOn():
     #   Get os information
    Settings.osPlatform = platform.system()
    Settings.osVersion = platform.release()

    if Settings.osPlatform.lower() == "windows":
        #   Running on windows
        Settings.dir_ConfigFiles = r"c:\\temp\aecs\\"
        Settings.dir_OneWireOnBoard = r'c:\\temp\\aecs\\onewire\\'
        Settings.debugfile = r'c:\\temp\aecs\\debug.log'
        Settings.dbfilename = Settings.dir_ConfigFiles + "aecs.db"
        Settings.runningOnRaspberry = False
    else:
        Settings.dbfilename = Settings.dir_ConfigFiles + "aecs.db"
        Settings.runningOnRaspberry = True
        
      
#   Allow CTRL + c to shutdown the system
signal.signal(signal.SIGINT, signal_handler)

def main():
    Debug.Info("Aecs-Pi-IoT Starting!!")
    

    if (Settings.ApplicationShodEnd):
        while (True):
            time.sleep(2)

    #   Get platform information
    GetPlatformRunningOn()

    #   Setup Grip as BCM
    GPIO.setmode(GPIO.BCM)
    Settings.rpi_Revision = str(GPIO.RPI_REVISION)

    #   Init Database  And get settings from database
    Database.start()
    
    Debug.Info("Wait 2 sek")
    time.sleep(2)

    #   Setup 2 relay to test
    tmprel1 = RelayHandling(1)
    tmprel1.Init(21, 1, True, True, False,1)
    Settings.relays[1] = tmprel1
    tmprel2 = RelayHandling(2)
    tmprel2.Init(20,1,False, True,False,1)
    Settings.relays[2] = tmprel2
    tmprel3 = RelayHandling(3)
    tmprel3.Init(16,1,False, True,False,2)
    Settings.relays[3] = tmprel3

    WebSiteInit();
    time.sleep(2)

    while True:
        Debug.Info("While is running from start")

        OnBoardOneWireInit();

        if Settings.runningOnRaspberry:
            #   Read raspbery pi int sensors
            with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as myfile:
                data = myfile.read()  # .replace('\n', '')
                Debug.Info("CPU: " + data)

        sdfsd = "dsfsdf"
        #for oneWire in sensorOneWireOnBoardDs18b20List:
        #    timeago = time.time() - oneWire.lastchecked
        #    print("ID: " + oneWire.romid + " Temp: " + str(round(oneWire.temp,2)) + " Status: " + oneWire.status + " Check: "  + str(round(timeago)))
            #print("ID: " + oneWire.romid + " Temp: " + str(round(oneWire.temp)))
        #print("tstvalue = " + Settings.testvalue)
        #packtest1.test()

        #aa = packtest1()
        #aa.test();
        
        time.sleep(5)
        #   Relay testing code
        #Settings.relays[1].Switch(True)
        #Settings.relays[2].Switch(True)
        #if Settings.relays[1].Data.IsOn:
        #    Settings.relays[1].TurnOff(0,False)
        #else:
        #    Settings.relays[1].TurnOn(0,False)
        
        #if Settings.relays[2].Data.IsOn:
        #    Settings.relays[2].TurnOff(0,False)
        #else:
        #    Settings.relays[2].TurnOn(0,False)

    Debug.Info("Ending")
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))


