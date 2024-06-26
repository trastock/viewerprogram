import csv

try:
    from .shooter import shooter
except:
    from shooter import shooter

import numpy as np
import h5py 
import os

class competition():
    def __init__(self,
                 competition_name : str = "",
                 date : str = "",
                 host : str = "",
                 diciplin : str = "",
                 firstlane : str = "",
                 lastlane : str = ""
                 ):
    
        self.competition_name = competition_name
        self.date = date
        self.host = host
        self.diciplin = diciplin
        self.firstlane = firstlane
        self.lastlane = lastlane
        self.shooters = []
        self.currentlane = round(0.5*(int(self.lastlane) + int(self.firstlane)))
        self.relays = {}
    
    def add_shooter(self, firstname, lastname, league, team,  result, relay):
        number_of_shooters = self.get_number_of_shooters_in_relay(relay)
        startnumber = str(number_of_shooters + 100)
        self.currentlane = (self.currentlane + 
                            ((-1)**(number_of_shooters + 1))*number_of_shooters)
        self.shooters.append(shooter(firstname, lastname, league, team, result, 
                                     self.diciplin, str(self.currentlane), startnumber, relay))
    def add_shooter_and_lane(self, firstname, lastname, league, team, result, relay, lane):
        startnumber = str(len(self.shooters) + 100)
        self.shooters.append(shooter(firstname, lastname, league, team, result, 
                                     self.diciplin, lane, startnumber, relay))
    
    def get_number_of_shooters_in_relay(self, relay):
        number_of_shooters = 0
        for shooter in self.shooters:
            if shooter.relay == relay:
                number_of_shooters += 1
        return number_of_shooters
    
    def add_relay(self, time : str):
        self.relays[str(len(self.relays) + 1)] = time
        #self.relays.append({len(self.relays) + 1: time})
    
    def export_to_hdf5(self, data : dict):
        with h5py.File("competitions\\" + self.competition_name + ".hdf5", "w") as f: 
            f.create_dataset("competition_info/name", data = self.competition_name)
            f.create_dataset("competition_info/date", data = self.date)
            f.create_dataset("competition_info/host", data = self.host)
            f.create_dataset("competition_info/diciplin", data = self.diciplin)
            for item in data.items():
                print(item)
            for shooter in self.shooters:
                f.create_dataset((shooter.firstname + shooter.lastname + "/first_name"), data = shooter.firstname)
                f.create_dataset((shooter.firstname + shooter.lastname + "/last_name"), data = shooter.lastname)
                f.create_dataset((shooter.firstname + shooter.lastname + "/league"), data = shooter.league)
                f.create_dataset((shooter.firstname + shooter.lastname + "/result"), data = shooter.result)
                f.create_dataset((shooter.firstname + shooter.lastname + "/diciplin"), data = shooter.diciplin)
                for series in shooter.series:
                    for shot in shooter.series[series]:
                        array = np.array(shooter.series[series][shot])
                        #print((shooter.firstname + shooter.lastname + "/" + series + "/" + shot).replace(" ", "_"))
                        #print(series)
                        #print(shooter.series[series][shot])
                        #print(array)
                        f.create_dataset((shooter.firstname + shooter.lastname + "/" + series + "/" + shot).replace(" ", "_"), data = array)
    
    def import_from_hdf5(self, hdf5path):
        current = os.getcwd()
        try:
            with h5py.File(current + "\\" + hdf5path, "r") as f:
                for key in list(f.keys()):
                    print(key)
                    print(list(f[key].keys()))
                #print(list(f.keys()))
                #print(f.values())
        except OSError:
            raise Exception("hdf5-file was not found")
    
    def create_import(self, path):
        with open(path + "\\" + self.competition_name.replace(" ", "_") + "_shooters.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for shooter in self.shooters:
                writer.writerow([";" + shooter.startnumber + ";" + shooter.firstname + 
                                 " " +  shooter.lastname + ";;;" + shooter.league + 
                                 ";0;0;" + shooter.team + ";;" +  shooter.lane + ";" +
                                 shooter.relay + ";" + self.relays[shooter.relay] + 
                                 ";0;1;0;0"])
    def create_startlist(self, path):
        pass
        
class issf_competition(competition):
    def __init__(self,
                 competition_name : str = "",
                 date : str = "",
                 host : str = "",
                 diciplin : str = ""
                 ):
        super().__init__(competition_name, date, host, diciplin)

class issf_competition_regular(issf_competition):
    
    def __init__(self,
                 competition_name : str = "",
                 date : str = "",
                 host : str = "",
                 diciplin : str = ""
                 ):
        super().__init__(competition_name, date, host, diciplin)
    

class issf_competition_doublematch(issf_competition):
    
    def __init__(self,
                 competition_name : str = "",
                 date : str = "",
                 host : str = "",
                 diciplin : str = ""
                 ):
        super().__init__(competition_name, date, host, diciplin)
"""
comp = issf_competition_regular("Nyköping Open", "18/7-2024", "Nyköpings Skyttegille", "FR60PR")
comp.add_shooter("Emil", "Alakulju", "18", "")
comp.add_shooter("Erik", "Alakulju", "18", "")
comp.shooters[0].add_shot([10.9, 10])
comp.shooters[0].add_shot([10.1, 10])
comp.shooters[0].add_shot([9.6, 9])

comp.shooters[1].add_shot([10.9, 10])
comp.shooters[1].add_shot([10.1, 10])
comp.shooters[1].add_shot([9.6, 9])

#print(comp.shooters[0].series)

comp.export_to_hdf5()
"""
#comp = issf_competition_regular()

#comp.import_from_hdf5("competitions\\Nyköping Open.hdf5")