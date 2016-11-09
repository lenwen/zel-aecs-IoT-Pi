from Settings import Settings
from Debug import Debug

class Shunt (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        #self.running = False;
        self.dbcon = None
        

    def run(self):
        #   dddd
        self.dbcon = sqlite3.connect(Settings.dir_ConfigFiles + "aecs.db")
        Settings.ShuntIsRunning = True
        while(Settings.ShuntIsRunning):
            #   dsfsdf
            self.Info("Running Thread")

            self.Info("Running Thread - Done")
            time.sleep(float(Settings.ShuntWaitBetweenRun))

    def stop(self):
        Settings.ShuntIsRunning = False

    def Info(self, Text):
        Debug.Info("Shunt | {text}".format(text=Text))

    def Warning(self, Text):
        Debug.Warning("Shunt | {text}".format(text=Text))    
    
    def Error(self, Text):
        Debug.Error("Shunt | {text}".format(text=Text))