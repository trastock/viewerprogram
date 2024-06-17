from shooter import shooter

class competition():
    #TODO: gör en sportklass som ärver från denna
    def __init__(self,
                 competition_name : str,
                 date : str,
                 host : str
                 ):
        self.competition_name = competition_name
        self.date = date
        self.host = host
        self.shooters = []
    
    def add_shooter(self, firstname, lastname, age, result, diciplin):
        self.shooters.append(firstname, lastname, age, result, diciplin)
    