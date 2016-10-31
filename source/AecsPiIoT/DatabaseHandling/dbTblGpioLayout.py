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
            test1.append((row[0],"Physical {} - {} - Bcm {} - Wpi {}".format(row[0], row[3], row[1], row[2])))
        
        return test1

    def IsPhysicalPortFree(phyId = str):
        if phyId is None:
            return False

        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        c.execute("select * from tblgpiolayout where physical = '{}' and inuse = 0;".format(phyId))
        rows = c.fetchall()
        c.close()
        if rows is None:
            return False
        if len(rows) == 1:
            return True

        if rows.count == 1:
            return True

        return False

    def SetPhysicalPortInUseStatus(phyId = str, inUse = bool):
        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        sqlString = "UPDATE tblgpiolayout SET inuse = "
        if inUse is True:
            sqlString += "1 "
        else:
            sqlString += "0 "

        sqlString += " where physical = '{}';".format(phyId)
        c.execute(sqlString)
        conn.commit()
        c.close()

    def GetBcmNameUsingPhysicalId(physicalId = str):
        conn = sqlite3.connect(Settings.dbfilename)
        c = conn.cursor()
        c.execute("select bcm from tblgpiolayout where physical = '{}';".format(physicalId))
        rows = c.fetchone()

        if rows is None:
            return None
        try:
            return str(rows[0])
        
        except:
            return None






