#Enable when running debug on raspberry pi

import ptvsd
ptvsd.enable_attach('aecspi')


GPIO = None
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

import OnBoardOneWireHandling

debug = True

def debug(debugtext):
    if Settings.debugEnable:
        if Settings.debugToConsole:
            print(debugtext)
        if Settings.debugToFile:
            with open(Settings.debugfile, 'a') as file_:
                file_.write(time.strftime("%H:%M:%S") + " - " + str(debugtext) + "\n")

def shutDown():
    print ("Stop all runnings threads")
    for t in Settings.threads:
        print('Thead: ' + str(Settings.threads[t].getName()) + ' will now stop()')
        Settings.threads[t].stop()
       
    print ("Wait 5 sec for threads to end")
    time.sleep(2);

    print ("Threads are joining before exit")
    for t in Settings.threads:
        Settings.threads[t].join()
    sys.exit(0)

def signal_handler(signal, frame):
    print ('You pressed Ctrl+C!')
    shutDown()

#   On Board 1-Wire Init
def OnBoardOneWireInit():
    if ("onboardOneWire" in Settings.threads):
        #   onboard One Wire is already init
        if (Settings.threads["onboardOneWire"].running == False):
            #   The thread is not running. start the Thread.
            Settings.threads["onboardOneWire"].start()
    else:
        #   Not init. do init
        os.system('modprobe w1-gpio')  # Turns on the GPIO module
        os.system('modprobe w1-therm') # Turns on the Temperature module
        thOnBoardOneWireHandling = OnBoardOneWireHandling.OnBoardOneWireHandling("onboardOneWire","1-wire onboard",2)
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
        import RPi.GPIO as GPIO
      

def main():
    print("Aecs-Pi-IoT Starting!!")
    
    if debug:
        print("Waiting for debug init - 30 sek")
        ptvsd.wait_for_attach(30)

    #   Get platform information
    GetPlatformRunningOn()

    #   Allow CTRL + c to shutdown the system
    signal.signal(signal.SIGINT, signal_handler)

    #   Database handling
    Database.start()


    OnBoardOneWireInit();
    
    time.sleep(5)
    while True:
        debug("While is running from start")
        #for oneWire in sensorOneWireOnBoardDs18b20List:
        #    timeago = time.time() - oneWire.lastchecked
        #    print("ID: " + oneWire.romid + " Temp: " + str(round(oneWire.temp,2)) + " Status: " + oneWire.status + " Check: "  + str(round(timeago)))
            #print("ID: " + oneWire.romid + " Temp: " + str(round(oneWire.temp)))
        #print("tstvalue = " + Settings.testvalue)
        #packtest1.test()

        #aa = packtest1()
        #aa.test();
        
        time.sleep(5)

    print("Ending")
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))


