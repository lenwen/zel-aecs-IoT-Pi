import RPi.GPIO as GPIO
from Settings import Settings
from Debug import Debug

class RelayHandling(object):
    def __init__(self, relayId):
        self.relayId = relayId
        self.IsInit = False
        self.Data = None
        self.Name = None
        self.NameInfo = None
        
        #self.gpioPin = gpioPin

    def Init(self, gpioPin = int, type=int, SetOn=bool, enable=bool, isLocked = bool, mode=int ):
        if self.Init is True:
            self.Error("This Relay is already init")
        else:
            self.Info("Running Init()")
            self.Data = RelaysDataClass(gpioPin, type)
            
            if self.Data.Type == 1:
                GPIO.setup(self.Data.GpioPin, GPIO.OUT, initial=1)
            elif self.Data.Type == 2:
                GPIO.setup(self.Data.GpioPin, GPIO.OUT, initial=0)
            else:
                self.Error("Relay type error!!!")
            self.Data.Enable = enable
            self.Data.IsLocked = isLocked
            self.Data.Mode = mode

            if SetOn is True:
                self.TurnOn(True)
            else:
                self.TurnOff(True)

            
            

        print("Init")
        

    def TurnOn(self, force=bool):
        self.Info("TurnOn")
        if self.Data.Type == 1:
            GPIO.output(self.Data.GpioPin, GPIO.LOW)
        elif self.Data.Type == 2:
            GPIO.output(self.Data.GpioPin, GPIO.HIGH)
        else:
            self.Error("Relay type error.")
        self.Data.IsOn = True

    def TurnOff(self, force=bool):
        self.Info("TurnOff")
        if self.Data.Type == 1:
            GPIO.output(self.Data.GpioPin, GPIO.HIGH)
        elif self.Data.Type == 2:
            GPIO.output(self.Data.GpioPin, GPIO.LOW)
        else:
            self.Error("Relay type error.")
        self.Data.IsOn = False

    def Switch(self, force=bool):
        if self.Data.IsOn is True:
            self.TurnOff(force)
        else:
            self.TurnOn(force)
    


    
    def Info(self, Text):
        Debug.Info("RelayHandling | Id: {id} | {text}".format(id=self.relayId,text=Text))

    def Warning(self, Text):
        Debug.Warning("RelayHandling | Id: {id} | {text}".format(id=self.relayId,text=Text))
    
    def Error(self, Text):
        Debug.Error("RelayHandling | Id: {id} | {text}".format(id=self.relayId,text=Text))


class RelaysDataClass(object):
    def __init__(self, gpioPin=int, type=int):
        self.GpioPin = gpioPin
        self.Type = type    #   1 = Off=high signal(1) on= low signal(0)
        #self.IsInit = False
        self.IsOn = False
        self.IsLocked = False
        self.Enable = False
        self.Mode = 1   #   1= Manuel | 2  = semi | 3 = Auto