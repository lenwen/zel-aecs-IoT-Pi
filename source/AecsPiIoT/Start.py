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

import OnBoardOneWireHandling

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
    elif cmdLower != "start.py":
        print("Error in starting values\nApplication will exit!")
        sys.exit(0)

#    else:



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

    Debug.Info("Threads are joining before exit")
    for t in Settings.threads:
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
    else:
        Settings.dbfilename = Settings.dir_ConfigFiles + "aecs.db"
        
      
#   Allow CTRL + c to shutdown the system
signal.signal(signal.SIGINT, signal_handler)

def main():
    Debug.Info("Aecs-Pi-IoT Starting!!")
    

    if (Settings.ApplicationShodEnd):
        while (True):
            time.sleep(2)

    #   Get platform information
    GetPlatformRunningOn()

    

    #   Init Database  And get settings from database
    Database.start()
    
    Debug.Info("Wait 2 sek")
    time.sleep(2)

    while True:
        Debug.Info("While is running from start")

        OnBoardOneWireInit();

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

    Debug.Info("Ending")
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))


