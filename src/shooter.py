import csv
import os

class shooter():
    
    def __init__(self, name : str = "dummy_name"
                     , age : str = ""
                     , result : dict = {}
                     , diciplin : str = ""):
        self.name = name
        self.age = age
        self.result = result
        self.diciplin = diciplin
        self.series = {}
        
    
    def get_series(self):
        print(os.getcwd())
        seriesline = ""
        with open("recourses\diciplins.csv", mode="r") as f:
            csvfile = csv.reader(f)
            for line in csvfile:
                if self.diciplin in line:
                    seriesline = line
        seriesline.pop(0)
        num_shots = 0
        for i in range(len(seriesline)):
            self.series["Series " + str(i + 1)] = {}
            for j in range(int(seriesline[i])):
                self.series["Series " + str(i + 1)]["Shot " + str(j + 1)] = {}
        self.series["Remaining"] = {}        
        
        

emil = shooter(age="19", diciplin="FR60PRFINAL")
emil.get_series()