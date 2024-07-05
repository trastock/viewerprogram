

try:
    from .competition import competition
    from .client import data_setup, update_data
except:
    from competition import competition
    from client import data_setup, update_data

class Program():
    def __init__(self):
        self.s = None
        self.competition = None
    
    def create_competition(self, name, date, host, diciplin, first_lane,
                           last_lane, logo_pic, sponsor_pic, hdf5_dir):
        self.competition = competition(name, date, host, diciplin, 
                                                          first_lane, last_lane, logo_pic,
                                                          sponsor_pic, hdf5_dir)
    def setup_socket(self):
        try:
            self.s = data_setup()
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            
    
    def update_competitions(self):
        if self.s:
            data = update_data(self.s, self.competition.raw_data)
            if data:
                self.competition.update(data)
                #print(self.competition.shooters["100"].relays["1"])
                
                print("")
                print(len(self.competition.raw_shots))