
import sqlite3

from Debug import Debug
from Settings import Settings
from RelayHandling import RelayHandling,RelaysDataClass, GPIO
from DatabaseHandling.dbTblGpioLayout import dbTblGpioLayout

"""
    Database design information.
    id
    gpiopin
    type
    mode                    INTEGER NOT NULL                        1= Manuel | 2  = semi | 3 = Auto
    isenable                INTERGET NOT NULL DEFAULT 0
    startason
    startaslastvalue
    isonnow                 INTERGET NOT NULL DEFAULT 0
    loghistorytodatabase
    name                    TEXT NOT NULL DEFAULT 'No name'
    nameinfo                TEXT NOT NULL DEFAULT 'No name'
    


"""

class dbTblRelays(object):
    """description of class"""


    def AddRelay(pgioPin = str, type = str, mode = str, isenable = bool, startason = bool, startaslastvalue = bool, loghistorytodatabase = bool, name = str, nameinfo = str):
        print("sdfdsf")
        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        sqlstring = "INSERT INTO 'tblrelays' (gpiopin,type ,mode ,isenable ,startason ,startaslastvalue , isonnow,loghistorytodatabase, name ,nameinfo) VALUES ("
        sqlstring += "'{}',".format(pgioPin)
        sqlstring += "'{}',".format(type)
        sqlstring += "'{}',".format(mode)
        sqlstring += "'{}',".format(int(isenable))
        sqlstring += "'{}',".format(int(startason))
        sqlstring += "'{}',".format(int(startaslastvalue))
        sqlstring += "'0',"                                         # isonnow)
        sqlstring += "'{}',".format(int(loghistorytodatabase))
        sqlstring += "'{}',".format(name)
        if nameinfo is None:
            sqlstring += "'No info'".format(nameinfo)
        else:
            sqlstring += "'{}'".format(nameinfo)
        
        sqlstring += ");"
        
        c.execute(sqlstring)
        newrelayId = str(c.lastrowid)
        conn.commit()
        c.close()
        return newrelayId

    #  aecs@pidev
    def GetRelaysAndSaveToSettingsRelay():
        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        c.execute("select id, gpiopin, type, mode, isenable, startason, startaslastvalue, isonnow, loghistorytodatabase, name, nameinfo from tblrelays;")
        #                  0      1      2     3       4         5          6                 7             8              9       10
        rows = c.fetchall()
        if rows is None:
            return None

        for row in rows:
            tmprelayAdd = RelayHandling(row[0])     #   Add relay id
            #   Get BCM port for relay Physical port
            tmprelayAdd.Name = str(row[9])
            tmprelayAdd.NameInfo = str(row[10])

            #tmprelayAdd.Init(bcmid, type, SetOn, enable, isLocked, mode)
            tmprelayAdd.Init(int(dbTblGpioLayout.GetBcmNameUsingPhysicalId(str(row[1]))), int(row[2]), False, bool(row[4]), False, int(row[3]))
            
            tmprelayAdd.Data.Startason = bool(row[5])
            tmprelayAdd.Data.StartAsLastValue = bool(row[6])
            tmprelayAdd.Data.LogHistoryToDatabase = bool(row[8])

            print("sdfdsf")
            
            if tmprelayAdd.Data.Startason:
                tmprelayAdd.TurnOn(True)
                
            else:
                #   TODO    fix start when db value is startaslastvalue
                print("sdfdsfs")

            #   All relay to settings
            #   Settings.relays[relayId] = relayClass
            Settings.relays[row[0]] = tmprelayAdd



