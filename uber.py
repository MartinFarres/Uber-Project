from hash_table import HashTable
from hash_table import OpenHashTable
from uber_map import Map, load_map
from direction import Direction
from dynamic_location import DynamicLoc
from static_location import StaticLoc
import file_manager as fm


"""
Program data
"""
data = fm.initialization_data()
static_loc_HT = data.static_loc_HT
cars_HT = data.cars_HT
cars_dir_HT = data.cars_dir_HT
people_HT = data.people_HT
main_map = data.main_map


"""
LOADING FUNCTIONS 
|----------------------------------------------------------|
"""


def create_map(path):
    if main_map != None:
        inp = ""
        while inp != "Y" and inp != "N":
            inp = input(
                "There's already a saved Map. Are you sure you want to overwrite it? (Y/N)")
        if inp == "N":
            return
    mapVar = fm.read_map_var()
    main_map = Map(mapVar[0], mapVar[1])


def load_fix_element(name, direction) -> bool:
    if name in static_loc_HT:
        return False

    static_loc_HT[name] = StaticLoc(name, direction)
    return True


def load_movil_element(name, direction, price) -> bool:
    """
    """
    if name[0].upper() == "C":
        if name in cars_HT:
            return False
        cars_HT[name] = DynamicLoc(name, direction, price)

    if name[0].upper() == "P":
        if name in people_HT:
            return False
        people_HT[name] = DynamicLoc(name, direction, price)
    return True


"""
TESTING  
|----------------------------------------------------------|
"""

if __name__ == "__main__":
    main_map = load_map("map_serialization.txt")

    # Car loading test - The list contains the arguments to load_movil_element
    cars = [
        ("C1", Direction(10, 0.3, 11, 0.7), 1),
        ("C2", Direction(12, 0.3, 13, 0.7), 1),
        ("C3", Direction(0, 0.3, 1, 0.7), 1),
        ("C4", Direction(6, 0.3, 7, 0.7), 1)
    ]

    for car_args in cars:
        # (*car_args) Python argument unpacking
        sucess = load_movil_element(*car_args)

        if not sucess:
            print(f"Unable to load car named {car_args[0]}, already added")
