from uber_map import Map

class Data:
    def __init__(self):
        self.main_map = Map([], [])
        self.cars_dir_HT = {}
        self.cars_HT = {}
        self.people_HT = {}
        self.static_loc_HT = {}
