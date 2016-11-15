#Enable when running debug on raspberry pi

#GPIO = None
#BUG fix python requirements
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
from decimal import *

from Settings import Settings
from DatabaseHandling import Database, dbTblRelays
from Debug import Debug
from RelayHandling import RelayHandling,RelaysDataClass, GPIO

#   Shunt import 
from PluginShunt import ShuntCtr, ShuntDataClass
import PluginShunt


import OnBoardOneWireHandling
import FlaskWeb

from multiprocessing import Process

commandline = sys.argv
vsDebug = False

def Info(Text):
    Debug.Info("Main | {text}".format(text=Text))

def Warning(Text):
    Debug.Warning("Main | {text}".format(text=Text))    
    
def Error(Text):
    Debug.Error("Main | {text}".format(text=Text))

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

def LoadFajkShuntdata():
    z = ShuntDataClass()
    z.ShuntInitIsDone = True
    z.ShuntIsRunning = False
    z.ShuntShodBeRunning = True
    z.ShuntWaitBetweenRun = 5
    Settings.shunt = z
    
    x = ShuntCtr.ShuntCtr(1,"test1")
    x.info = "start"
    x.enable = True
    x.cirkPumpShodBeOn = True
    x.cirkPumpStartTimeBeforStartingShunt = 30
    x.tempOutSensorId = 1001
    x.cirkPumpRelayId = 101
    Settings.shunt.ShuntCtr[1] = x

    x = ShuntCtr.ShuntCtr(2, "test2")
    x.info = "start"
    x.enable = True
    Settings.shunt.ShuntCtr[2] = x

    # print("aaaaa")

def ErrorDataBuild():
    if not (Settings.shunt is None):
        for shuntId in Settings.shunt.ShuntCtr:
            if (Settings.shunt.ShuntCtr[shuntId].ErrorMainInShunt):
                Debug.Error("----------------------------------------------")
                Debug.Error("MAIN ERROR IN shunt id: {}".format(shuntId))
                Debug.Error("----------------------------------------------")
                
                Debug.Error("trying to automatisk fix errors")
                try:
                    Settings.shunt.ShuntCtr[shuntId].errorCheckAndFix()
                except AttributeError:
                    Debug.Error("No automatisk fix error exist")
                Debug.Error("----------------------------------------------")
        
def PluginShuntInit():
    if Settings.ShuntPluginEnable:
        #   Shunt shod be used
        if (Settings.shunt is None):
            #   Shunt data is none. do init.
            #Load shuntdata from database.
            LoadFajkShuntdata()
        
        #   Check if thread already exist
        if ("pluginShunt" in Settings.threads):
            #   Thread already exist
            if (Settings.shunt.ShuntIsRunning == False):
                #   Thread is not running. start the thread.
                if (Settings.shunt.ShuntShodBeRunning):
                    #   Thread ska köras. starta den
                    Settings.threads["pluginShunt"].run()

        else:
            thPluginShunt = PluginShunt.PluginShunt("pluginShunt","Shunt system",2)
            print("bbbbb")
            thPluginShunt.start()
            Settings.threads["pluginShunt"] = thPluginShunt
            print("aaaaa")






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

#   Fun BuildIn Box control        
def OnDeviceFan():
    if Settings.FanControllEnable:
        Info("FAN | Device enable - Running fan control")
        if Settings.FanInitDone:
            #   Read sensor temp value
            # Info("FAN | Fan speed is running")
            if Settings.FanTempSensorId in Settings.sensors:
                
                #   Get temp value whitout decimal data. Get only int value ex: 22  not 22.0
                #tmpsensorValue = round(Settings.sensors[1001].GetValue(), 0)
                tmpsensorValue = int(Settings.sensors[1001].GetValue())
                Info("FAN | temperatur sensorId exist - Value: {}".format(str(tmpsensorValue)))
                #print (str(Settings.sensors[1001].GetValue()))
            else:
                Warning("FAN | - sensor id dont exist")
                #onewireonboardds18b20
        else:
            Info("FAN | init is not done. Doing onDeviceFan init()")
            GPIO.setup(Settings.FanPwmBcmId, GPIO.OUT)
            Settings.FanPwmData = GPIO.PWM(Settings.FanPwmBcmId, Settings.FanFrequency)
            Settings.FanPwmData.ChangeFrequency(Settings.FanFrequency)
            Settings.FanPwmData.start(Settings.FanStartValue)
            Settings.FanInitDone = True
        
        Info("FAN | Device Fan enable - Running fan control - Done")

#   Allow CTRL + c to shutdown the system
signal.signal(signal.SIGINT, signal_handler)

def main():
    Debug.Info("Aecs-Pi-IoT Starting!!")
    

    if (Settings.ApplicationShodEnd):
        while (True):
            time.sleep(2)

    #   Get platform information
    GetPlatformRunningOn()


    #   Setup Grio as BCM
    if Settings.runningOnRaspberry:
        GPIO.setmode(GPIO.BCM)
        Settings.rpi_Revision = str(GPIO.RPI_REVISION)
    else:
        Settings.rpi_Revision = "3"


    #TODO   Run some test to see that everthing is OK


    #   Init Database  And get settings from database
    Database.start()
    
    Debug.Info("Wait 2 sek")
    time.sleep(2)

    #   Get relay information from database.
    dbTblRelays.dbTblRelays.GetRelaysAndSaveToSettingsRelay()


    WebSiteInit();
    time.sleep(2)

    Settings.ShuntPluginEnable = True
    mainThreadRunTime = 0
    while True:
        Info("While is running from start")
        mainThreadRunTime = mainThreadRunTime + 1
        
        OnBoardOneWireInit();

        
        PluginShuntInit()

        if Settings.runningOnRaspberry:
            #   Read raspbery pi int sensors
            with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as myfile:
                data = myfile.read()  # .replace('\n', '')
                Debug.Info("CPU: " + data)

        sdfsd = "dsfsdf"
        
        OnDeviceFan();

        #   Test change shunt information.
        Settings.shunt.ShuntCtr[1].info = "run: {}".format(mainThreadRunTime)
        Settings.shunt.ShuntCtr[2].info = "run: {}".format(mainThreadRunTime - 1)
        
        #   Check the system for errors
        ErrorDataBuild()

        time.sleep(5)


    Debug.Info("Ending")

    

if __name__ == "__main__":
    sys.exit(int(main() or 0))



