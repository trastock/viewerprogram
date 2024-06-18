from shooter import shooter
import numpy as np
import h5py 

class competition():
    #TODO: gör en sportklass som ärver från denna
    def __init__(self,
                 competition_name : str,
                 date : str,
                 host : str,
                 diciplin : str
                 ):
    
        self.competition_name = competition_name
        self.date = date
        self.host = host
        self.diciplin = diciplin
        self.shooters = []
    
    def add_shooter(self, firstname, lastname, age, result, diciplin):
        self.shooters.append(shooter(firstname, lastname, age, result, diciplin))
    
    def export_to_hdf5(self):
        with h5py.File("competition\\" + self.competition_name + ".hdf5", "w") as f: 
            for shooter in self.shooters:
                for series in shooter.series:
                    for shot in shooter.series[series]:
                        array = np.array(shooter.series[series][shot])
                        #print((shooter.firstname + shooter.lastname + "/" + series + "/" + shot).replace(" ", "_"))
                        #print(series)
                        #print(shooter.series[series][shot])
                        #print(array)
                        dset = f.create_dataset((shooter.firstname + shooter.lastname + "/" + series + "/" + shot).replace(" ", "_"), data = array)
                
        
class issf_competition(competition):
    def __init__(self,
                 competition_name : str,
                 date : str,
                 host : str,
                 diciplin : str):
        super().__init__(competition_name, date, host, diciplin)

class issf_competition_regular(issf_competition):
    
    def __init__(self,
                 competition_name : str,
                 date : str,
                 host : str,
                 diciplin : str):
        super().__init__(competition_name, date, host, diciplin)
    

class issf_competition_doublematch(issf_competition):
    
    def __init__(self,
                 competition_name : str,
                 date : str,
                 host : str,
                 diciplin : str):
        super().__init__(competition_name, date, host, diciplin)

comp = issf_competition_regular("Nyköping Open", "18/7-2024", "Nyköpings Skyttegille", "FR60PR")
comp.add_shooter("Emil", "Alakulju", "18", "", "FR60PR")
comp.add_shooter("Erik", "Alakulju", "18", "", "FR60PR")
comp.shooters[0].add_shot([10.9, 10])
comp.shooters[0].add_shot([10.1, 10])
comp.shooters[0].add_shot([9.6, 9])

comp.shooters[1].add_shot([10.9, 10])
comp.shooters[1].add_shot([10.1, 10])
comp.shooters[1].add_shot([9.6, 9])

#print(comp.shooters[0].series)

comp.export_to_hdf5()