import csv
import os

class shooter():
    
    def __init__(self, firstname : str = ""
                     , lastname : str = ""
                     , league : str = ""
                     , team : str = ""
                     , result : dict = 0
                     , diciplin : str = ""
                     , lane : str = ""
                     , startnumber : str = ""
                     , relay : str = ""):
        self.firstname = firstname
        self.lastname = lastname
        self.league = league
        self.team = team
        self.result = result
        self.diciplin = diciplin
        self.lane = lane
        self.startnumber = startnumber
        self.relay = relay
        self.series = self.get_series()

    def get_series(self):
        seriesline = ""
        series = {}
        with open("recourses\diciplins.csv", mode="r") as f:
            csvfile = csv.reader(f)
            for line in csvfile:
                if self.diciplin in line:
                    seriesline = line
        seriesline.pop(0)
        for i in range(len(seriesline)):
            series["Series " + str(i + 1)] = {}
            for j in range(int(seriesline[i])):
                series["Series " + str(i + 1)]["Shot " + str(j + 1)] = []
        series["Remaining"] = {}     
        return series
        
    def add_shot(self, incoming_shot : list):
        for serie in self.series:
            for shot in self.series[serie]:
                if not self.series[serie][shot]:
                   self.series[serie][shot] = incoming_shot     
                   break
            break
                       
            
