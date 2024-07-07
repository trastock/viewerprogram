

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
        self.last_update_shot = 0
        self.last_update_remain = 0
    
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
                #print(self.competition.raw_data["_SHOT"])
                
                if self.last_update_remain:
                    old_shot = self.competition.raw_data["_SHOT"].pop(self.last_update_shot)
                    for idx, element in enumerate(old_shot):
                        old_shot[idx] = element.replace("'", "")
                    remain_of_shot = self.competition.raw_data["_REAMAIN"].pop(self.last_update_remain)
                    del remain_of_shot[0]
                    new_shot = old_shot + remain_of_shot
                    self.competition.raw_data["_SHOT"].insert(self.last_update_shot, new_shot)
                    self.last_update_remain = 0
                    
                for idx, shot in enumerate(self.competition.raw_data["_SHOT"]):
                    if len(shot) < 24:
                        self.last_update_shot = idx
                        self.last_update_remain = len(self.competition.raw_data["_REAMAIN"])
                