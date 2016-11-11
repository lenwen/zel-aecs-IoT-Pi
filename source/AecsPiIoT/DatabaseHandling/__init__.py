
import time
import datetime
import glob
import sqlite3
import os
from Debug import Debug
from Settings import Settings

#from Settings import Settings

conn = sqlite3

class Database(object):
    def __init__():
        self.dsfdsf = "asds"
        
    def Info(Text):
        Debug.Info("Database | {text}".format(text=Text))

    def Warning(Text):
        Debug.Warning("Database | {text}".format(text=Text))    
    
    def Error(Text):
        Debug.Error("Database | {text}".format(text=Text))    

    def start():
        #   Check if db file exist.
        dbCreateFile = True

        dfdsf = "sdfds"
        if os.path.isfile(Settings.dbfilename):
            #   File exist. dont do default loyout
            dbCreateFile = False

        #   Connect or create db file
        conn = sqlite3.connect(Settings.dbfilename)
        
        if dbCreateFile:
            #   Indert default loyout into database file
            c = conn.cursor()
#            sql = 'create table if not exists settings (name text primary key not null, data text not null;)'
            c.execute("create table if not exists tblsettings (name text primary key not null, data text not null);")
            c.execute("INSERT INTO tblsettings VALUES('dbversion','1');")
            c.execute("INSERT INTO tblsettings VALUES('debugenable','1');")
            c.execute("INSERT INTO tblsettings VALUES('debugtoconsole','1');")
            c.execute("INSERT INTO tblsettings VALUES('debugtofile','1');")
            c.execute("INSERT INTO tblsettings VALUES('debugfile','/etc/aecs/debug.log');")
            c.execute("INSERT INTO tblsettings VALUES('OnBoardOneWireShodBeRunning','1');")
            c.execute("INSERT INTO tblsettings VALUES('OnBoardOneWireWaitBetweenRun','10');")
            c.execute("INSERT INTO tblsettings VALUES('OnBoardOneWireSensorDs18b20CrcWaitingTime','20');")
            c.execute("INSERT INTO tblsettings VALUES('OnBoardOneWireSensorDs18b20MissingTime','30');")
            c.execute("CREATE TABLE `tblsensors` (`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,	`type`	TEXT NOT NULL,	`tag`	TEXT NOT NULL,	`name`	TEXT,	`info`	TEXT,	`enable`	INTEGER NOT NULL DEFAULT 0,	`isworking`	INTEGER NOT NULL DEFAULT 0,	`collectvaluetime`	INTEGER NOT NULL DEFAULT 0,	`saverealtimetodatabase`	INTEGER NOT NULL DEFAULT 0,	`savehistorytodatabase`	INTEGER NOT NULL DEFAULT 0,	`sensorvalue1`	REAL,	`sensorvalue2`	REAL);")
            c.execute("CREATE INDEX `index_tblsensors_sensormatch` ON `tblsensors` (`type` ASC,`tag` ASC);")
            c.execute("INSERT INTO SQLITE_SEQUENCE VALUES('tblsensors',1000);")

            #c.execute("UPDATE SQLITE_SEQUENCE SET seq = 1000 WHERE name = 'tblsensors'")
            conn.commit()
            c.close()
            #   bugfix for sqllite seq
            # http://stackoverflow.com/questions/692856/set-start-value-for-autoincrement-in-sqlite
            # INSERT INTO sqlite_sequence (name,seq) SELECT '<table>', <n> WHERE NOT EXISTS (SELECT changes() AS change FROM sqlite_sequence WHERE change <> 0);
        
        c = conn.cursor()
        c.execute("SELECT data FROM tblsettings where name = 'dbversion';")

        row = c.fetchone()
        dbversion = int(str(row[0]))

        # dsfdsf = "sdfdsfd"
        Debug.Info("Database running version: " + str(dbversion))

        Database.DoDbNeedUpdate(dbversion)

        #   Get all settings from database that the system need to run
        c.execute("select * from tblsettings;")
        rows = c.fetchall()

        #   Save settings to running application
        for row in rows:
            if row[0] is not None:
                matchWord = str(row[0].lower().strip())
                
                if matchWord == "dbversion":
                    Settings.dbVersion = row[1]
                elif matchWord == "debugenable":
                    Debug.Info("debugenable Found in database")
                    if (Settings.debugForceFromCmd is False):
                        Settings.debugEnable = row[1]
                    else:
                        Debug.Info("Debug force from console. dont change value")

                elif matchWord == "debugtoconsole":
                    Debug.Info("debugtoconsole found in database")
                    if (Settings.debugForceFromCmd is False):
                        Settings.debugToConsole = row[1]
                    else:
                        Debug.Info("Debug force from console. dont change value")

                elif matchWord == "debugtofile":
                    Debug.Info("debugtofile found in database")
                    if (Settings.debugForceFromCmd is False):
                        Settings.debugToFile = row[1]
                    else:
                        Debug.Info("Debug force from console. dont change value")

                elif matchWord == "debugfile":
                    Debug.Info("debugfile found in database")
                    if (Settings.debugForceFromCmd is False):
                        if Settings.runningOnRaspberry is True:
                            Settings.debugfile = row[1]
                    else:
                        Debug.Info("Debug force from console. dont change value")

                elif matchWord == "onboardonewireshodberunning":
                    Debug.Info("OnBoardOneWireShodBeRunning Found in database")
                    if row[1] == "1":
                        Settings.OnBoardOneWireShodBeRunning = True
                    else:
                        Settings.OnBoardOneWireShodBeRunning = False

                elif matchWord == "onboardonewirewaitbetweenrun":
                    Debug.Info("OnBoardOneWireWaitBetweenRun Found in database")
                    Settings.OnBoardOneWireWaitBetweenRun = row[1]

                elif matchWord == "onboardonewiresensords18b20crcwaitingtime":
                    Debug.Info("OnBoardOneWireSensorDs18b20CrcWaitingTime Found in database")
                    Settings.OnBoardOneWireSensorDs18b20CrcWaitingTime = row[1]

                elif matchWord == "onboardonewiresensords18b20missingtime":
                    Database.Info("Settings | OnBoardOneWireSensorDs18b20MissingTime Found in database")
                    Settings.OnBoardOneWireSensorDs18b20MissingTime = row[1]

                elif matchWord == "shuntpluginenable":
                    Database.Info("Settings | ShuntPluginEnable Found in database")
                    Settings.ShuntPluginEnable = bool(row[1])

                else:
                    Debug.Error("Settings Value is missing!!!!!\nValue: " + matchWord + "\nData: " + row[1]) 

        Debug.Info("Settings read from database done!")
        

    def DoDbNeedUpdate(dbversion = int):
        if dbversion < 2:
            Database.DoUpgrade2()
            if Settings.rpi_Revision == "3":
                Database.LayoutPiRevision3()
        if dbversion < 3:
            Database.DoUpgrade3()
             
    def DoUpgrade2():
        Debug.Info("Running database upgrade 2")
        connUpdate = sqlite3.connect(Settings.dbfilename)
        c = connUpdate.cursor()
        c.execute("CREATE TABLE `tblrelays` (	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,	`gpiopin`	INTEGER NOT NULL,	`type`	INTEGER NOT NULL,	`mode`	INTEGER NOT NULL,	`isenable`	INTEGER NOT NULL DEFAULT 0,	`startason`	INTEGER NOT NULL DEFAULT 0,	`startaslastvalue`	INTEGER NOT NULL DEFAULT 0, `isonnow` INTEGER NOT NULL DEFAULT 0,	`loghistorytodatabase`	INTEGER NOT NULL,	`name`	TEXT NOT NULL DEFAULT 'No name',	`nameinfo`	TEXT NOT NULL DEFAULT 'No info');")
        c.execute("INSERT INTO SQLITE_SEQUENCE VALUES('tblrelays',100);")
        c.execute("CREATE TABLE 'tblgpiolayout' ( `physical` INTEGER NOT NULL UNIQUE, `bcm` INTEGER, `wpi` INTEGER, `name` TEXT NOT NULL, `inuse` INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(`physical`) );")
        c.execute("CREATE INDEX `index_tblgpiolayoyt_bcm` ON `tblgpiolayout` (`bcm` ASC);")
        c.execute("CREATE INDEX `index_tblgpiolayoyt_wpi` ON `tblgpiolayout` (`wpi` ASC);")
        c.execute("UPDATE tblsettings SET data = '2' where name = 'dbversion' ;")
        connUpdate.commit()
        c.close()
        Debug.Info("Running database upgrade 2 - Done")

    def DoUpgrade3():
        Debug.Info("Running database upgrade 3")
        connUpdate = sqlite3.connect(Settings.dbfilename)
        c = connUpdate.cursor()
        c.execute("CREATE TABLE `tbllogrelays` (	`logid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,	`relayid`	INTEGER NOT NULL,	`datelogutc`	INTEGER NOT NULL,	`changefrom`	TEXT NOT NULL,	`changeto`	TEXT NOT NULL,	`changeby`	TEXT NOT NULL);")
        c.execute("CREATE INDEX `index_tbllogrelays_relayid` ON `tbllogrelays` (`relayid` ASC);")
        c.execute("UPDATE tblsettings SET data = '3' where name = 'dbversion' ;")
        connUpdate.commit()
        c.close()
        Debug.Info("Running database upgrade 3 - Done")

    def LayoutPiRevision3():
        Debug.Info("Running Layout Pi Revision3 update")
        connUpdate = sqlite3.connect(Settings.dbfilename)
        c = connUpdate.cursor()
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (1,NULL,NULL,'3.3v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (2,NULL,NULL,'5v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (3,2,8,'SDA.1',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (4,NULL,NULL,'5v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (5,3,9,'SCL.1',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (6,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (7,4,7,'GPIO. 7 - OneWire',1);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (8,14,15,'TxD',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (9,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (10,15,16,'RxD',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (11,17,0,'GPIO. 0',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (12,18,1,'GPIO. 1',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (13,27,2,'GPIO. 2',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (14,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (15,22,3,'GPIO. 3',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (16,23,4,'GPIO. 4',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (17,NULL,NULL,'3.3v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (18,24,5,'GPIO. 5',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (19,10,12,'MOSI',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (20,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (21,9,13,'MISO',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (22,25,6,'GPIO. 6',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (23,11,14,'SCLK',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (24,8,10,'CE0',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (25,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (26,7,11,'CE1',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (27,0,30,'SDA.0',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (28,1,31,'SCL.0',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (29,5,21,'GPIO. 21',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (30,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (31,6,22,'GPIO. 22',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (32,12,26,'GPIO. 26',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (33,13,23,'GPIO. 23',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (34,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (35,19,24,'GPIO. 24',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (36,16,27,'GPIO. 27',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (37,26,25,'GPIO. 25',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (38,20,28,'GPIO. 28',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (39,NULL,NULL,'0v',0);")
        c.execute("INSERT INTO `tblgpiolayout` (physical,bcm,wpi,name,inuse) VALUES (40,21,29,'GPIO. 29',0);")
        connUpdate.commit()
        c.close()

         
# aecs@pidev