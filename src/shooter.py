import csv
import os

class shooter():
    
    def __init__(self, firstname : str = ""
                     , lastname : str = ""
                     , team : str = ""
                     , startnumber : str = ""
                     ):
        self.firstname = firstname
        self.lastname = lastname
        self.team = team
        self.startnumber = startnumber
        self.relays = {}

    def get_series(self, diciplin):
        seriesline = ""
        series = {}
        with open("recourses\diciplins.csv", mode="r") as f:
            csvfile = csv.reader(f)
            for line in csvfile:
                if diciplin in line:
                    seriesline = line
        seriesline.pop(0)
        for i in range(len(seriesline)):
            series["Series " + str(i + 1)] = {}
            for j in range(int(seriesline[i])):
                series["Series " + str(i + 1)]["Shot " + str(j + 1)] = []
        series["Remaining"] = {}
        series["Excercise"] = {}
        return series
        
    def add_shot(self, incoming_shot : list, relay, excercise, nr):
        if excercise == "32":
            self.relays[relay]["series"]["Excercise"][nr] = incoming_shot
            
        else:
            for serie in self.relays[relay]["series"].values():
                if "Serie" in serie:
                    for shot in self.series[serie]:
                        if not self.series[serie][shot]:
                            self.series[serie][shot] = incoming_shot    
                            break
            self.relays[relay]["series"]["Remaining"][nr] = incoming_shot
                
    
    def add_relay(self, relaynumber, diciplin, league, result, lane):
        self.relays[relaynumber] = {"series": self.get_series(diciplin),
                                    "dicipline": diciplin,
                                    "league": league,
                                    "result": result,
                                    "lane": lane}
    def __str__(self):
        return self.startnumber
