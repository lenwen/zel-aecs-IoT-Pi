import sqlite3

from Debug import Debug
from Settings import Settings


class dbTblGpioLayout(object):
    """description of class"""
    def __init__():
        self.dsfdsf = "asds"

    def GetFreeGpioPortAsSelectedList():
        #   Get free grioPorts 
        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        c.execute("select physical, bcm, wpi, name from tblgpiolayout where inuse = 0 and name like 'GPIO%' order by bcm")
        rows = c.fetchall()

        if rows is None:
            return None

        test1 = []
        for row in rows:
            test1.append((row[0],"{} - Bcm {} - Wpi {}".format(row[3], row[1], row[2])))
        
        return test1



