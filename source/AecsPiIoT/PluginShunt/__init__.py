import threading
import time
import datetime
import glob
import sqlite3
import os

from Settings import Settings
from Debug import Debug

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
                self.Info("Running Thread")
                for keys in Settings.shunt.ShuntCtr:
                    Settings.shunt.ShuntCtr[keys].run()

                self.Info("Running Thread - Done - Waiting for next run")
                time.sleep(float(Settings.shunt.ShuntWaitBetweenRun))

    def stop(self):
        Settings.shunt.ShuntIsRunning = False

    def Info(self, Text):
        Debug.Info("Shunt | {text}".format(text=Text))

    def Warning(self, Text):
        Debug.Warning("Shunt | {text}".format(text=Text))    
    
    def Error(self, Text):
        Debug.Error("Shunt | {text}".format(text=Text))