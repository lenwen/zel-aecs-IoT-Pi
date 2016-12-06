#import logging
import io
import os
import time
#import datetime

from datetime import datetime
from enum import Enum

from Settings import Settings
from LogHandling.logSettingsClass import logSettingsClass, logSettingFileClass

#from LogHandling import logmodules, logtypes
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
        if (logtext is None):
            return
        
        logtext = logmodule.name + " | " + logtext

        logWhitDefault = False
        #get settings for this debug message
        if (logmodule.name.lower() in Settings.logHandling):
            #print("logmodule exist!")
            aa = Settings.logHandling[logmodule.name.lower()]
            if (aa.logOnlyUsingDefault):
                logWhitDefault = True
            else:
                if (aa.logDefaultAlso):
                    logWhitDefault = True
                
                LogHandling.Dolog(aa, logtype, logtext)
                
                #do log
        else:
            #print("logmodule dont exist!")
            logWhitDefault = True
            
        if (logWhitDefault):
            LogHandling.Dolog(Settings.logHandling["default"], logtype, logtext)

        #print(logmodule)
        #if logmodule == logmodules.Default:
        #    print("ojojoj")
        #if (logmodule == logmodules.Shunt):
        #    print("sjusjusju")

        #print("-----------------")
        #test1 = logmodules.Default
        #print(logmodule.name)
        #print("-----------------")
        
    def Dolog(dclass = logSettingsClass, logtype = str, logtext = str ):
        
        if dclass is None:
            return
        if logtype is None:
            return
        if logtext is None:
            return

        #print("dolog running!!")
        isTypeNotSet = False
        isTypeDebug = False
        isTypeInfo = False
        isTypeWarning = False
        isTypeError = False
        isTypeCritical = False

        if logtype == logtypes.DEBUG:
            isTypeDebug = True
            if (dclass.logConsoleDebug):
                LogHandling.OutputConsole(logtext, dclass.logAddDateTime)
            for x in dclass.logToFile:
                if (x.fileName is None):
                    continue
                if x.logDebug:
                    # log to file
                    LogHandling.OutputFile(x.fileName, logtext, dclass.logAddDateTime)
                    #print("log to file!!!")
        
        elif logtype == logtypes.INFO:
            isTypeInfo = True
            if (dclass.logConsoleInfo):
                LogHandling.OutputConsole(logtext, dclass.logAddDateTime)
            for x in dclass.logToFile:
                if (x.fileName is None):
                    continue
                if x.logInfo:
                    # log to file
                    LogHandling.OutputFile(x.fileName, logtext, dclass.logAddDateTime)
                    #print("log to file!!!")

        elif logtype == logtypes.WARNING:
            isTypeWarning = True
        
        elif logtype == logtypes.ERROR:
            isTypeWarning = True
        
        elif logtype == logtypes.CRITICAL:
            isTypeCritical = True
        
        else:
            isTypeNotSet = True

        

    def OutputConsole(logtext = str, addDate = bool):
        if (addDate):
            textOutput = str(datetime.utcnow()) + " | " + logtext
        print("--LogHandling-- " + textOutput)

    def OutputFile(fileName = str, logtext = str, addDate = bool):
        if (addDate):
            textOutput = str(datetime.utcnow()) + " | " + logtext
        
        with open(fileName, 'a') as file_:
                file_.write(str(logtext) + "\n")

        
        
        

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



