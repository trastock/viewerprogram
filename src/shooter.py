import csv
import os

class shooter():
    
    def __init__(self, firstname : str = ""
                     , lastname : str = ""
                     , age : str = ""
                     , result : dict = 0
                     , diciplin : str = ""):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.result = result
        self.diciplin = diciplin
        self.series = self.get_series()

    def get_series(self):
        print(os.getcwd())
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
                series["Series " + str(i + 1)]["Shot " + str(j + 1)] = {}
        series["Remaining"] = {}     
        return series
        
    def add_shot(self, incoming_shot : dict):
        for serie in self.series:
            for shot in self.series[serie]:
                print(self.series[serie][shot])
                if not self.series[serie][shot]:
                   self.series[serie][shot] = incoming_shot     
                   break
                       
            
emil = shooter(age="22", diciplin="FR60PRFINAL")
emil.add_shot({'decimal': 10.9})
print(emil.series)