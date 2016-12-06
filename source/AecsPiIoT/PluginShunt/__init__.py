import threading
import time
import datetime
import glob
import sqlite3
import os

from Settings import Settings
#from Debug import Debug
from LogHandling import *

from PluginShunt.ShuntDataClass import ShuntDataClass
from PluginShunt.ShuntCtr import ShuntCtr as ctr


class PluginShunt (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        #self.running = False;
        #self.dbcon = sqlite3.connect(Settings.dir_ConfigFiles + "aecs.db")
        

    def run(self):
        #   dddd
        
        #if (Settings.shunt is None):
        #    Debug.Info("Shunt is None - Read information from database")
        #    self.LoadFromDatabase()
        #    self.FajkData

        if not (Settings.shunt is None):
            Settings.shunt.ShuntIsRunning = True
            while(Settings.shunt.ShuntIsRunning):
                # sdfdsfdsf
                self.debugInfo("Running Thread")
                for shuntId in Settings.shunt.ShuntCtr:
                    Settings.shunt.ShuntCtr[shuntId].run()
                    Settings.shunt.ShuntCtr[shuntId].errorBuild()
                        

                self.debugInfo("Running Thread - Done - Waiting for next run")
                time.sleep(float(Settings.shunt.ShuntWaitBetweenRun))

            for shuntId in Settings.shunt.ShuntCtr:
                Settings.shunt.ShuntCtr[shuntId].stop()


    def stop(self):
        Settings.shunt.ShuntIsRunning = False

    def debugInfo(self, Text):
        LogHandling.log(logmodules.Shunt, logtypes.INFO, Text)
        #Debug.Info("Shunt | {text}".format(text=Text))

    def debugWarning(self, Text):
        LogHandling.log(logmodules.Shunt, logtypes.WARNING, Text)
        #Debug.Warning("Shunt | {text}".format(text=Text))    
    
    def debugError(self, Text):
        LogHandling.log(logmodules.Shunt, logtypes.ERROR, Text)
        #Debug.Error("Shunt | {text}".format(text=Text))