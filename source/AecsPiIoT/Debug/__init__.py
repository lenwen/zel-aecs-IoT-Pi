
import io
import os
import time
import datetime
from Settings import Settings

def SendToLog(Text):
    if (Settings.debugEnable):
        if (Settings.debugToConsole):
            print(Text)
        if (Settings.debugToFile):
            with open(Settings.debugfile, 'a') as file_:
                file_.write(time.strftime("%H:%M:%S") + " | " + str(Text) + "\n")


class Debug(object):
    def Dev(args):
        SendToLog("Dev | " + Text)
    def Info(Text):
        SendToLog("Info  | " + Text)
    def Warning(Text):
        SendToLog("Warn  | " + Text)
    def Error(Text):
        SendToLog("Error | " + Text)




        