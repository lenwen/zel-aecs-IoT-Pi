
import sqlite3

from Debug import Debug
from Settings import Settings

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
        c = connUpdate.cursor()
        sqlstring = "INSERT INTO 'tblrelays' (gpiopin,type ,mode ,isenable ,startason ,startaslastvalue , isonnow,loghistorytodatabase, name ,nameinfo) VALUES ("
        sqlstring += "'{}',".format(pgioPin)
        sqlstring += "'{}',".format(type)
        sqlstring += "'{}',".format(mode)
        sqlstring += "'{}',".format(isenable)
        sqlstring += "'{}',".format(startason)
        sqlstring += "'{}',".format(startaslastvalue)
        sqlstring += "'0',".format(isonnow)
        sqlstring += "'{}',".format(loghistorytodatabase)
        sqlstring += "'{}',".format(name)
        if nameinfo is None:
            sqlstring += "'No info'".format(nameinfo)
        else:
            sqlstring += "'{}'".format(nameinfo)
        
        sqlstring += ");"
        
        c.execute(sqlstring)
        newrelayId = str(c.lastrowid)
        coon.commit()
        coon.close()
        return newrelayId



