#import logging
import io
import os
import time
import datetime
from enum import Enum

from Settings import Settings
from LogHandling.logSettingsClass import logSettingsClass, logSettingFileClass

# from LogHandling import logmodules, logtypes
#from LogHandlingClassData import * #  LogHandlingClassData import logmodules, logtypes

#   https://docs.python.org/3/howto/logging.html
#   https://docs.python.org/3/library/logging.html

class LogHandling(object):
    #def __init__(logmodule = logmodules, logtype = logtypes, logtext = str):
    #def __init__(logmodule = str, logtype = str, logtext = str):
    #    print("hej--hej")
    #    print (logmodule)
    #    print("hej--hej")
    def log(logmodule, logtype = str, logtext = str):
        
        #get settings for this debug message
        if (logmodule.name.lower() in Settings.logHandling):
            print("logmodule exist!")
        else:
            print("logmodule dont exist!")
        
        print(logmodule)
        if logmodule == logmodules.Default:
            print("ojojoj")
        if (logmodule == logmodules.Shunt):
            print("sjusjusju")

        print("-----------------")
        test1 = logmodules.Default
        print(logmodule.name)
        print("-----------------")
        
       
            
        
        
        

#class LogHandlingClassData(object):
#    type = str
#    outputDebug = False
#    outputInfo = False


class logmodules(Enum):
    Default = 0
    Shunt = 10

class logtypes(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50



