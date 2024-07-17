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
        self.dec = 0
        self.active_serie = "Excercise"

    def get_series(self, diciplin):
        seriesline = ""
        series = {}
        with open("recourses\\diciplins.csv", mode="r") as f:
            csvfile = csv.reader(f)
            for line in csvfile:
                if diciplin in line:
                    seriesline = line
        seriesline.pop(0)
        if seriesline.pop(0) == "dec":
            self.dec = 1
        self.innerten = float(seriesline.pop(0))
        self.caliber = float(seriesline.pop(0))
        for i in range(len(seriesline)):
            series["Series " + str(i + 1)] = {"Tot": 0, "Inner tens": 0}
            for j in range(int(seriesline[i])):
                series["Series " + str(i + 1)]["Shot " + str(j + 1)] = []
        series["Remaining"] = {}
        series["Excercise"] = {}
        return series
        
    def add_shot(self, incoming_shot : list, relay, excercise, nr):
        print(excercise)
        if excercise == "32" or excercise == "544" or excercise == "551" or excercise == "39" or excercise == "35" or excercise == "547":
            if "Serie" in self.active_serie:
                if not "Excercise 2" in self.relays[relay]["series"].keys():
                    #self.relays[relay]["series"]["Excercise 2"][nr] == incoming_shot
                    self.active_serie = "Excercise 2"
                elif not "Excercise 3" in self.relays[relay]["series"].keys():
                    #self.relays[relay]["series"]["Excercise 3"][nr] == incoming_shot
                    self.active_serie = "Excercise 3"
                self.relays[relay]["series"][self.active_serie] = {}
            self.relays[relay]["series"][self.active_serie][nr] = incoming_shot
            """
            if not nr in self.relays[relay]["series"]["Excercise"].keys():
                self.relays[relay]["series"]["Excercise"][nr] = incoming_shot
                self.active_series = "Excercise"
            else:
                try:
                    if not nr in self.relays[relay]["series"]["Excercise 2"].keys():    
                        self.relays[relay]["series"]["Excercise 2"][nr] = incoming_shot
                        self.active_serie = "Excercise 2"
                    else:
                        try: 
                            if not nr in self.relays[relay]["series"]["Excercise 3"].keys():
                                self.relays[relay]["series"]["Excercise 3"][nr] = incoming_shot
                                self.active_serie = "Excercise 3"
                        except:
                            self.relays[relay]["series"]["Excercise 3"][nr] = incoming_shot
                            self.active_serie = "Excercise 3"
                except:
                    self.relays[relay]["series"]["Excercise 2"][nr] = incoming_shot
                    self.active_serie = "Excercise 2"
                """
            
        else:
            for serie in self.relays[relay]["series"].keys():
                find = False
                if "Serie" in serie:
                    for shot in self.relays[relay]["series"][serie].keys():
                        if "Shot" in shot:
                            if not self.relays[relay]["series"][serie][shot]:
                                self.relays[relay]["series"][serie][shot] = incoming_shot
                                self.relays[relay]["result"] += incoming_shot[self.dec]
                                self.relays[relay]["result"] = round(self.relays[relay]["result"], 1)
                                
                                self.relays[relay]["series"][serie]["Inner tens"] += incoming_shot[4]
                                self.relays[relay]["inner tens"] += incoming_shot[4]
                                
                                self.relays[relay]["series"][serie]["Tot"] += incoming_shot[self.dec]
                                self.relays[relay]["series"][serie]["Tot"] = round(self.relays[relay]["series"][serie]["Tot"], 1)
                                
                                find = True
                                self.active_serie = serie
                                self.relays[relay]["num_shots"] += 1
                                break
                    if find:
                        break
            else:
                self.relays[relay]["series"]["Remaining"][nr] = incoming_shot
                self.active_serie = "Remaining"
    
    def add_relay(self, relaynumber, diciplin, league, result, inner_tens, lane):
        self.relays[relaynumber] = {"series": self.get_series(diciplin),
                                    "dicipline": diciplin,
                                    "league": league,
                                    "result": result,
                                    "inner tens": inner_tens,
                                    "lane": lane,
                                    "num_shots": 0}
    
    def check_if_innerten(self, x, y):
        distance = abs((x**2 + y**2)**0.5 - (self.caliber/2))
        if distance < self.innerten:
            return 1
        else:
            return 0
    
    def __str__(self):
        return self.startnumber
