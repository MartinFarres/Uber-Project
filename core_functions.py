from hash_table import HashTable
from hash_table import OpenHashTable
from uber_map import Map, load_map
from direction import Direction
from dynamic_location import DynamicLoc
from static_location import StaticLoc
import file_manager as fm


def create_map_core(path):
    mapVar = fm.read_map_var(path)
    return Map(mapVar[0], mapVar[1])


def load_fix_element_core(name, direction, static_loc_HT) -> bool:
    if name not in static_loc_HT:
        static_loc_HT[name] = StaticLoc(name, direction)
        return True
    return False


def load_movil_element_core(name, direction, price, cars_HT, people_HT) -> bool:
    if name[0].upper() == "C":
        if name in cars_HT:
            return False
        cars_HT[name] = DynamicLoc(name, direction, price)

    if name[0].upper() == "P":
        if name in people_HT:
            return False
        people_HT[name] = DynamicLoc(name, direction, price)
    return True
