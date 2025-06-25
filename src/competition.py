import csv
import math

try:
    from .shooter import shooter
    from .make_pdf import make_pdf
except:
    from shooter import shooter
    from make_pdf import make_pdf

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
                 lastlane : str = "",
                 logopic : str = "",
                 sponsorpic : str = "",
                 hdf5dir : str = "",
                 hdf5path : str = ""
                 ):
    
        self.competition_name = competition_name
        self.date = date
        self.host = host
        self.diciplin = diciplin
        self.firstlane = firstlane
        self.lastlane = lastlane
        self.shooters = {}
        #if self.firstlane and self.lastlane:
         #   self.currentlane = round(0.5*(int(self.lastlane) + int(self.firstlane)))
        #else:
         #   self.currentlane = 0
        self.relays = {}
        self.logopic = logopic
        self.sponsorpic = sponsorpic
        self.hdf5dir = hdf5dir
        if not hdf5path and self.competition_name:
            self.hdf5path = self.hdf5dir + "\\" + self.competition_name + ".hdf5"
        else:
            self.hdf5path = hdf5path
        self.number_of_shooters = 0
        self.raw_data = {}
        self.raw_shots = [] 
        self.raw_total = []
        self.import_mode = False
    def add_shooter(self, firstname, lastname, team, startnumber = ""):
        #number_of_shooters = self.get_number_of_shooters_in_relay(relay)
        startnumber = str(self.number_of_shooters + 100)
        #self.currentlane = (self.currentlane + 
                            #((-1)**(number_of_shooters + 1))*number_of_shooters)
        #self.shooters.append(shooter(firstname, lastname, league, team, result, 
                                     #self.diciplin, str(self.currentlane), startnumber, relay))
        self.shooters[startnumber] = shooter(firstname, lastname, team, startnumber)
        #print(self.number_of_shooters)
        #self.number_of_shooters += 1
        print("Startnummer: ", startnumber)
        if not self.import_mode:
            self.export_to_hdf5()
        self.number_of_shooters += 1
 
    def add_shooter_to_relay(self, startnumber, diciplin, league, relay, result = 0, inner_tens = 0, lane = ""):
        number_of_shooters = self.get_number_of_shooters_in_relay(relay)
        if not lane:
            #self.currentlane = (self.currentlane + 
            #                ((-1)**(number_of_shooters + 1))*number_of_shooters)
            self.relays[relay]["current_lane"] = (self.relays[relay]["current_lane"] + 
                            ((-1)**(number_of_shooters + 1))*number_of_shooters)
            lane = self.relays[relay]["current_lane"]
        self.shooters[startnumber].add_relay(relay, diciplin, league, result, inner_tens, lane)
        #for shooter in self.shooters:
         #   if shooter.startnumber == startnumber:
          #      shooter.add_relay(relay, diciplin, league, result, lane)
        if not self.import_mode:
            self.export_to_hdf5()
        
    """
    def add_shooter_and_lane(self, firstname, lastname, league, team, result, relay, lane):
        startnumber = str(len(self.shooters) + 100)
        self.shooters.append(shooter(firstname, lastname, league, team, result, 
                                     self.diciplin, lane, startnumber, relay))
    """
    def get_number_of_shooters_in_relay(self, relay):
        number_of_shooters = 0
        for shooter in self.shooters.values():
            if relay in shooter.relays.keys():
                number_of_shooters += 1
        return number_of_shooters
    
    def add_relay(self, time : str, relay_number):
        if not relay_number:
            self.relays[str(len(self.relays) + 1)] = {"time": time,
                                                      "current_lane": round(0.5*(int(self.lastlane) + int(self.firstlane))),
                                                      "relay_number": len(self.relays.keys()) + 1}
        else:
            self.relays[relay_number] = {"time": time,
                                                      "current_lane": round(0.5*(int(self.lastlane) + int(self.firstlane))),
                                                      "relay_number":    len(self.relays.keys()) + 1}
        
        if not self.import_mode:
            self.export_to_hdf5()
        #self.relays.append({len(self.relays) + 1: time})
    
    def export_to_hdf5(self):
        with h5py.File(self.hdf5path, "a") as f:
            try:
                f.create_dataset("competition_info/name", data = self.competition_name)
                f.create_dataset("competition_info/date", data = self.date)
                f.create_dataset("competition_info/host", data = self.host)
                f.create_dataset("competition_info/diciplin", data = self.diciplin)
                f.create_dataset("competition_info/firstlane", data = self.firstlane)
                f.create_dataset("competition_info/lastlane", data = self.lastlane)
                f.create_dataset("competition_info/logopic", data = self.logopic)
                f.create_dataset("competition_info/sponsorpic", data = self.sponsorpic)           
                f.create_dataset("competition_info/hdf5dir", data = self.hdf5dir) 
                f.create_dataset("competition_info/hdf5path", data = self.hdf5path)
                f.create_dataset("competition_info/number_of_shooters", data = str(self.number_of_shooters))
            except Exception as e:
                print(f"Exception: {e}")
            #f.create_dataset("competition_info/currentlane", data = str(self.currentlane))
            try:
                for relay in self.relays:
                    f.create_dataset("competition_info/relays/" + relay + "/time", 
                                    data = self.relays[relay]["time"])
                    f.create_dataset("competition_info/relays/" + relay + "/current_lane", 
                                    data = str(self.relays[relay]["current_lane"]))
                    f.create_dataset("competition_info/relays/" + relay + "/relay_number", 
                                    data = str(self.relays[relay]["relay_number"]))
            except Exception as e:
                print(f"Exception: {e}")
            try:
                for data_type in self.raw_data:
                    data_dir = "raw_data/" + data_type
                    for i, data in enumerate(self.raw_data[data_type]):
                        try:
                            new_data_dir = data_dir + "/" + str(i)
                            dt = h5py.string_dtype(encoding='utf-8')
                            string_array = np.array(data, dtype=dt)
                            f.create_dataset(new_data_dir, data=string_array)
                        except:
                            pass
            except Exception as e:
                print("fuck")
                print(f"Exception: {e}")
            try:
                for shooter in self.shooters.values():
                    current_dir = shooter.startnumber
                    f.create_dataset((shooter.startnumber + "/first_name"), data = shooter.firstname)
                    f.create_dataset((shooter.startnumber + "/last_name"), data = shooter.lastname)
                    f.create_dataset((shooter.startnumber + "/startnumber"), data = shooter.startnumber)
                    f.create_dataset((shooter.startnumber + "/team"), data = shooter.team)
                    
                    for relay in shooter.relays:
                        relay_dir = current_dir + "/" + relay
                        f.create_dataset((relay_dir + "/diciplin"), data = shooter.relays[relay]["dicipline"])
                        f.create_dataset((relay_dir + "/league"), data = shooter.relays[relay]["league"])
                        f.create_dataset((relay_dir + "/result"), data = str(shooter.relays[relay]["result"]))
                        f.create_dataset((relay_dir + "/lane"), data = str(shooter.relays[relay]["lane"]))
                        f.create_dataset((relay_dir + "/inner tens"), data = str(shooter.relays[relay]["inner tens"]))
                        for series in shooter.relays[relay]["series"]:
                            for shot in shooter.relays[relay]["series"][series]:
                                array = np.array(shooter.relays[relay]["series"][series][shot])
                                f.create_dataset((relay_dir + "/" + series + "/" + shot), data = array)
                    
            except Exception as e:
                print(f"Exception: {e}")
    def import_from_hdf5(self, path):
        self.import_mode = True
        try:
            with h5py.File(path, "r") as f:
                for key in list(f.keys()):
                    if key == "competition_info":
                        try:
                            self.competition_name = self.get_string(f, key + "/name")
                            self.date  = self.get_string(f, key + "/date")
                            self.host = self.get_string(f, key + "/host")
                            self.diciplin = self.get_string(f, key + "/diciplin")
                            self.firstlane = self.get_string(f, key + "/firstlane")
                            self.lastlane = self.get_string(f, key + "/lastlane")
                            #self.currentlane = int(self.get_string(f, key + "/currentlane"))
                            self.logopic = self.get_string(f, key + "/logopic")
                            self.sponsorpic = self.get_string(f, key + "/sponsorpic")
                            self.hdf5dir = self.get_string(f, key + "/hdf5dir")
                            self.number_of_shooters = int(self.get_string(f, key + "/number_of_shooters"))
                            self.hdf5path = self.hdf5dir + "\\" + self.competition_name + ".hdf5"
                        except Exception as e:
                            print(f"Exception: {e}")
                            self.import_mode = False
                        try:
                            for relay in list(f[key + "/relays"].keys()):
                                self.add_relay(self.get_string(f, key + "/relays/" + relay + "/time"), relay)
                                self.relays[relay]["current_lane"] = int(self.get_string(f, key + "/relays/" + relay + "/current_lane"))
                                self.relays[relay]["relay_number"] = int(self.get_string(f, key + "/relays/" + relay + "/relay_number"))
                        except Exception as e:
                            print(f"Exception: {e}")
                            self.import_mode = False
                    elif key == "raw_data":
                        self.raw_data = {}
                        for data_type in list(f[key].keys()):
                            self.raw_data[data_type] = []
                            for data in list(f[key + "/" + data_type].keys()):
                                string_array = f[key + "/" + data_type + "/" + data][:]
                                self.raw_data[data_type].append([s.decode('utf-8') for s in string_array])
                        
                        
                        #if "_SHOT" in self.raw_data.keys():
                         #   self.raw_shots = self.raw_data["_SHOT"]
                        #print(self.raw_data)
                    
                    else:
                        try:
                            self.add_shooter(self.get_string(f, key + "/first_name"), 
                                            self.get_string(f, key + "/last_name"),
                                            self.get_string(f, key + "/team"), 
                                            key) 
                            active_shooter = self.shooters[key] 
                            
                            #for shooter in self.shooters:
                            #           if shooter.startnumber == key:
                            #              active_shooter = shooter
                            for relay in list(f[key].keys()):
                                #int(relay)
                                if relay in list(f["competition_info/relays"].keys()):
                                    try:
                                        self.add_shooter_to_relay(key, 
                                                                self.get_string(f, key + "/" + relay + "/diciplin"),
                                                                self.get_string(f, key + "/" + relay + "/league"),
                                                                relay,
                                                                float(self.get_string(f, key + "/" + relay + "/result")),
                                                                int(self.get_string(f, key + "/" + relay + "/inner tens")),
                                                                self.get_string(f, key + "/" + relay + "/lane"))
                                        for series_key in list(f[key + "/" + relay].keys()):
                                            if type(f[key + "/" + relay + "/" + series_key]) == h5py._hl.group.Group:
                                                for shot_key in list(f[key + "/" + relay + "/" + series_key].keys()):
                                                    if type(f[key + "/" + relay + "/" + series_key + "/" + shot_key]) == h5py._hl.dataset.Dataset:
                                                        array = np.array(f[key + "/" + relay + "/" + series_key + "/" + shot_key])
                                                        active_shooter.relays[relay]["series"][series_key][shot_key] =  array.tolist()
                                    except Exception as e:
                                        #print("Failed to load series: " + str(e))
                                        self.import_mode = False
                                        pass
                        except Exception as e:
                            self.import_mode = False
                            print(f"Excp: {e}")
                        
                        
        except OSError:
            #raise Exception("hdf5-file was not found")
            self.import_mode = False
            return False
        self.update(self.raw_data)
        self.import_mode = False
        return True
    
    def get_string(self, f, path):
        dataset = f[path]
        data = dataset[()]
        if isinstance(data, bytes):
            # Convert bytes to string
            string_data = data.decode('utf-8')
        else:
        # If the dataset contains multiple strings or other data types, process accordingly
        # Here we assume it contains multiple strings
            string_data = [item.decode('utf-8') for item in data]

        return string_data

    
    def create_import(self, path, keep_results):
        with open(path + "\\" + self.competition_name.replace(" ", "_") + "_shooters.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for shooter in self.shooters.values():
                print("Här borde vi hamna 1")
                for relay in shooter.relays:
                    if relay in self.relays:
                        relay_number = self.relays[relay]["relay_number"] 
                        if shooter.relays[relay]["result"] == "" or (not keep_results):
                            result = "0"
                        writer.writerow([";" + shooter.startnumber + str(relay_number) + ";" + shooter.firstname + 
                                        " " +  shooter.lastname + ";;;" + shooter.relays[relay]["league"] + 
                                        ";0;0;" + shooter.team + ";;" +  str(shooter.relays[relay]["lane"]) + ";" +
                                        str(relay_number) + ";" + self.relays[relay]["time"] + 
                                        ";0;1;" + result + ";0;0"])
    
    def create_startlist(self, path, relay):
        header = ["Tavla", "Namn", "Förening", "Klass"]
        table = []
        for shooter in self.shooters.values():
            if relay in shooter.relays.keys():
                table.append([shooter.relays[relay]["lane"], shooter.firstname + " " +  shooter.lastname, 
                              shooter.team, shooter.relays[relay]["league"]])
        make_pdf(table, header, self.competition_name, self.host
                 , self.date, "Startlista", relay, 
                 self.logopic, self.sponsorpic, path, self.relays[relay]["time"], 0)
    
    def create_result(self, path, result_type, type_content):
        if result_type == "relay":
            header = ["Tavla", "Namn", "Förening", "Klass", "TOT", "Anm"]
            table = []
            for shooter in self.shooters.values():
                if type_content in shooter.relays.keys():
                    serie_part = []
                    for serie in shooter.relays[type_content]["series"]:
                        print(header)
                        if "Serie" in serie:
                            if serie not in header:
                                header.insert(-2, serie)
                            serie_part.append(shooter.relays[type_content]["series"][serie]["Tot"])
                    table.append([shooter.relays[type_content]["lane"], shooter.firstname + " " +  shooter.lastname, 
                                  shooter.team, shooter.relays[type_content]["league"]] + serie_part +
                                 [str(shooter.relays[type_content]["result"])])
            make_pdf(table, header, self.competition_name, self.host
                 , self.date, "Resultat", "" + type_content, 
                 self.logopic, self.sponsorpic, path, self.relays[type_content]["time"], -1)
                
        
    
    def update(self, raw_data):
        if raw_data is not None:
            self.raw_data = raw_data
            print("3")
            for item in raw_data.keys():
                print("4")
                if "SHOT" in item:
                    for shot in raw_data[item]:
                        #print(len(shot))
                        if len(shot) < 24:
                            break
                        elif (shot not in self.raw_shots) and (len(shot) == 24):
                            self.raw_shots.append(shot)
                            startnumber = shot[3][:3]
                            relay_number = shot[3][-1]
                            relay = ""
                            print(self.relays)
                            for relaykey in self.relays.keys():
                                #print(relaykey)
                                #print(self.relays[relaykey]["relay_number"])
                                #print(relay_number)
                                print(str(self.relays[relaykey]["relay_number"]))
                                if str(self.relays[relaykey]["relay_number"]) == str(relay_number):
                                    relay = relaykey
                                    break
                            
                            print("1")
                            print(relay_number)
                            print(relay)
                            if relay:
                                print("2")
                                if str(startnumber) in self.shooters.keys():
                                    try:
                                        if self.shooters[startnumber].relays[relay]["dec"] == 0:
                                            print("2")
                                            self.shooters[startnumber].add_shot([int(shot[10]), float(shot[11])/10, 
                                                                                float(shot[14]), float(shot[15]), 
                                                                                self.shooters[startnumber].check_if_innerten(float(shot[14]), float(shot[15]))], 
                                                                                relay, shot[9], shot[13])
                                        else:
                                            print("3")
                                            print(shot)
                                            self.shooters[startnumber].add_shot([float(shot[10])/10, float(shot[10])/10, 
                                                                                float(shot[14]), float(shot[15]), 
                                                                                self.shooters[startnumber].check_if_innerten(float(shot[14]), float(shot[15]))], 
                                                                                relay, shot[9], shot[13])
                                        #print(f"Nytt skott: {float(shot[11])/10}")
                                        #print(shot[9])
                                    
                                    
                                    except Exception as e:
                                        print(f"Problem {e}")
                                        self.raw_shots.pop(-1)
                                        #return False
                                        #print(f"Något gick fel: {e}")
                                        #print(shot)
                """           
                elif "TOTL" in item:
                    for total in raw_data[item]:
                        if total not in self.raw_total:
                            self.raw_total.append(total)
                """
                            
#  title        lane  startn            time_of_shot                    hel  dec         nr    x              y
['_SHOT', '11', '12', '1021', '60', '28', '18:12:35.80', '3', '1', '0', '9', '98', '0', '16', '0.00000000', '-0.00920000', '900', '0', '0', '655.35', '64832156', '65535', '0', '0']
["b'_SHOT", '11', '12', '1021', '60', '29', '18:17:30.26', '3', '1', '0', '9', '97', '0', '17', '0.00707107', '-0.00707107', '900', '0', '0', '655.35', '64836156', '65535', '0', '0']
["b'_SHOT", '11', '12', '1021', '60', '30', '18:19:06.68', '3', '1', '512', '10', '109', '0', '18', '0.00000000', '-0.00040000', '900', '0', '0', '655.35', '64840156', '65535', '0', '0']
['_SHOT', '11', '12', '1021', '60', '32', '19:54:34.29', '3', '1', '0', '10', '105', '0', '20', '0.00360000', '0.00000000', '900', '0', '0', '655.35', '64848156', '65535', '0', '0']
['_SHOT', '11', '12', '1021', '60', '35', '19:55:29.50', '3', '1', '512', '10', '109', '0', '21', '0.00028284', '-0.00028284', '900', '0', '0', '655.35', '64852156', '65535', '0', '0'], 
['_SHOT', '11', '12', '1021', '60', '36', '19:55:30.47', '3', '1', '0', '10', '101', '0', '22', '-0.00480833', '-0.00480833', '900', '0', '0', '655.35', '64856156', '65535', '0', '0']
#                                                                  prov? 
['_SHOT', '12', '13', '1002', '60', '87', '20:09:25.39', '3', '1', '32', '9', '97', '0', '1', '-0.00707107', '0.00707107', '900', '0', '0', '655.35', '65012390', '65535', '0', '0']
["b'_SHOT", '12', '13', '1002', '60', '88', '20:10:59.91', '3', '1', '32', '10', '104', '0', '2', '0.00000000', '-0.00440000', '900', '0', '0', '655.35', '65016390', '65535', '0', '0']


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