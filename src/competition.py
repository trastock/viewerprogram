from shooter import shooter
import numpy as np
import h5py 
import os

class competition():
    def __init__(self,
                 competition_name : str = "",
                 date : str = "",
                 host : str = "",
                 diciplin : str = ""
                 ):
    
        self.competition_name = competition_name
        self.date = date
        self.host = host
        self.diciplin = diciplin
        self.shooters = []
    
    def add_shooter(self, firstname, lastname, age, result):
        self.shooters.append(shooter(firstname, lastname, age, result, self.diciplin))
    
    def export_to_hdf5(self):
        with h5py.File("competitions\\" + self.competition_name + ".hdf5", "w") as f: 
            f.create_dataset("competition_info/name", data = self.competition_name)
            f.create_dataset("competition_info/date", data = self.date)
            f.create_dataset("competition_info/host", data = self.host)
            f.create_dataset("competition_info/diciplin", data = self.diciplin)
            for shooter in self.shooters:
                f.create_dataset((shooter.firstname + shooter.lastname + "/first_name"), data = shooter.firstname)
                f.create_dataset((shooter.firstname + shooter.lastname + "/last_name"), data = shooter.lastname)
                f.create_dataset((shooter.firstname + shooter.lastname + "/age"), data = shooter.age)
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
comp = issf_competition_regular()

comp.import_from_hdf5("competitions\\Nyköping Open.hdf5")