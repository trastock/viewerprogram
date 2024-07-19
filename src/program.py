import copy

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
        self.slave_mode = False
        self.active_relay = "1"
        self.document_path = ""
    
    def create_competition(self, name = "", date = "", host = "", diciplin = "", first_lane = "", 
                           last_lane = "", logo_pic = "", sponsor_pic = "", hdf5_dir = "", hdf5_path = "", just_load = True):
        self.competition = competition(name, date, host, diciplin, 
                                                          first_lane, last_lane, logo_pic,
                                                          sponsor_pic, hdf5_dir, hdf5_path)
        if not just_load:
            self.competition.export_to_hdf5()
    def setup_socket(self):
        try:
            self.s = data_setup()
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            
    
    def update_competitions(self):
        if self.s:
            data = self.competition.raw_data
            old_data = copy.deepcopy(data)
            data = update_data(self.s, data)
            if data:
                flag = True
                if not "_SHOT" in old_data.keys():
                    if not "_SHOT" in data.keys():
                        return False
                    flag = False
                if flag:
                    if len(old_data["_SHOT"]) == len(data["_SHOT"]):
                        print("10")
                        return False
                
                self.competition.update(data)
                #print(self.competition.shooters["100"].relays["1"]["series"])
                #for total in self.competition.raw_data["_TOTL"]:
                #    print(len(total))
                #print(self.competition.raw_data["_TOTL"])
                #print(self.competition.raw_data["_SHOT"])
                #for shot in self.competition.raw_data["_SHOT"]:
                #    if len(shot) == 24:
                #        print(shot[9])
                
                if self.last_update_remain:
                    old_shot = self.competition.raw_data["_SHOT"].pop(self.last_update_shot)
                    for idx, element in enumerate(old_shot):
                        old_shot[idx] = element.replace("'", "")
                    remain_of_shot = self.competition.raw_data["_REAMAIN"].pop(self.last_update_remain)
                    #remain_of_shot_old = copy.copy(remain_of_shot)
                    remain_of_shot[0] = remain_of_shot[0].replace("b'", "")
                    if remain_of_shot[0] == "":
                        del remain_of_shot[0]
                    else:
                        old_shot[-1] += remain_of_shot[0]
                        del remain_of_shot[0]
                    new_shot = old_shot + remain_of_shot
                    #print(old_shot)
                    #print("Gamla remain")
                    #print(remain_of_shot_old)
                    #print("Nya remain")
                    #print(remain_of_shot)
                    
                    self.competition.raw_data["_SHOT"].insert(self.last_update_shot, new_shot)
                    self.last_update_remain = 0
                    
                for idx, shot in enumerate(self.competition.raw_data["_SHOT"]):
                    if len(shot) < 24:
                        self.last_update_shot = idx
                        self.last_update_remain = len(self.competition.raw_data["_REAMAIN"])
                self.competition.export_to_hdf5()
                return True
            else:
                print("8")
                return False
        else:
            print("9")
            return False
                