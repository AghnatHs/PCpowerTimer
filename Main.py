import os

import kivy

from datetime import datetime,timedelta
from pathlib import Path
import datetime

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout

class Timer():
    def __init__(self,hour,minute,second):
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def totalTime(self):
        self.hour = int(self.hour*60*60)
        self.minute = int(self.minute*60)
        totalTime = self.hour + self.minute + int(self.second)
        return totalTime

class MainScreen(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        #constant
        self.ID_HOUR = 0
        self.ID_MINUTE = 1
        self.ID_SECOND = 2

        self.hour = 0
        self.minute = 0
        self.second = 0        

        self.initWidget()

    def initWidget(self):
        self.hourLabel = self.ids.hourLabel
        self.minuteLabel = self.ids.minuteLabel
        self.secondLabel = self.ids.secondLabel
        self.hourEstimatedLabel = self.ids.hourEstimatedLabel

        self.hourLabel.text = "00"
        self.minuteLabel.text = "00"
        self.secondLabel.text = "00"

    def increaseTime(self,idz):
        if idz==self.ID_HOUR: self.hour+=1
        elif idz==self.ID_MINUTE: self.minute+=1
        else: self.second+=1
        
        if self.hour>99:self.hour=0
        if self.minute>59:self.minute=0
        if self.second>59:self.second=0

        self.updateTimeWidget() 
    def decreaseTime(self,idz):
        if idz==self.ID_HOUR: self.hour-=1
        elif idz==self.ID_MINUTE: self.minute-=1
        else: self.second-=1
        
        if self.hour<0:self.hour=99
        if self.minute<0:self.minute=59
        if self.second<0:self.second=59

        self.updateTimeWidget()
    def updateTimeWidget(self):
        _hour = self.hour
        _minute = self.minute
        _second = self.second
        _hourNow = datetime.datetime.now().time()

        self.hourLabel.text = self.getStringedTimeHour(_hour)
        self.minuteLabel.text = self.getStringedTime(_minute)
        self.secondLabel.text = self.getStringedTime(_second)

        _hourEstimated = datetime.datetime.combine(datetime.datetime.today(), _hourNow) + timedelta(seconds=Timer(_hour,_minute,_second).totalTime())
        
        self.hourEstimatedLabel.text = "Executed in : "+str(_hourEstimated.strftime(r"%d/%m/%y %H:%M:%S"))
    def getStringedTime(self,value):
        if value>=10: return str(value)
        else: return "0"+str(value)
    def getStringedTimeHour(self,value):
        if value>=10: return str(value)
        elif value<0: return str(99)
        else: return "0"+str(value)

    def exec(self,command=False):
        home = str(Path.home())
        time = Timer(self.hour,self.minute,self.second).totalTime()
        os.system("dir "+home)
        if time>0:
            os.system("shutdown -a")
            if command!=False:
                os.system(command+str(time))

class MainApp(App):
    def build(self):
        Builder.load_file("Main.kv")
        self.title = "PC Shutdown Timer by Aghnat HS"
        Screen = MainScreen()
        return Screen

app = MainApp()
app.run()