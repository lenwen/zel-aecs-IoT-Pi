
import time
import datetime
import glob
import sqlite3
import os


from Settings import Settings

conn = sqlite3

class Database(object):
    def __init__():
        self.dsfdsf = "asds"
        

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
            c.execute("INSERT INTO tblsettings VALUES('debugfile','1');")
            c.execute("INSERT INTO tblsettings VALUES('sensoronewireonboardds18b20crcwaitingtime','5');")
            c.execute("INSERT INTO tblsettings VALUES('sensoronewireonboardds18b20missingtime','30');")

            c.execute("CREATE TABLE `tblsensors` (`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,	`type`	TEXT NOT NULL,	`tag`	TEXT NOT NULL,	`name`	TEXT,	`info`	TEXT,	`enable`	INTEGER NOT NULL DEFAULT 0,	`isworking`	INTEGER NOT NULL DEFAULT 0,	`collectvaluetime`	INTEGER NOT NULL DEFAULT 0,	`saverealtimetodatabase`	INTEGER NOT NULL DEFAULT 0,	`savehistorytodatabase`	INTEGER NOT NULL DEFAULT 0,	`sensorvalue1`	REAL,	`sensorvalue2`	REAL);")
            c.execute("CREATE INDEX `sensormatch` ON `tblsensors` (`type` ASC,`tag` ASC);")
            conn.commit()
            c.close()
            dsfdsfdsf = "sdfsdf"
        
        c = conn.cursor()
        c.execute("SELECT data FROM tblsettings where name = 'dbversion';")

        row = c.fetchone()
        dbversion = int(str(row[0]))

        dsfdsf = "sdfdsfd"

        print(dbversion)

        Database.DoDbNeedUpdate(dbversion)

        #   Get all settings from database that the system need to run
        c.execute("select * from tblsettings;")
        rows = c.fetchall()

        for row in rows:
            print(row)

        print("ddd")

    def DoDbNeedUpdate(dbversion = int):
        if dbversion < 2:
            Database.DoUpgrade2()
             
    def DoUpgrade2():
        print("upgrade 2")
           
