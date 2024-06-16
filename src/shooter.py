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
        
        with open("recourses\diciplins.csv", mode="r") as f:
            csvfile = csv.reader(f)
            for line in csvfile:
                print(line)
        
        

emil = shooter(age="19")
emil.get_series()