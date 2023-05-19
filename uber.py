from hash_table import HashTable
from hash_table import OpenHashTable
from uber_map import Map, load_map
from direction import Direction
from dynamic_location import DynamicLoc
from static_location import StaticLoc


"""
Program data
"""
main_map = None
carsDirHT = {}
carsHT = {}
peopleHT = {}
staticLocHT = {}


"""
LOADING FUNCTIONS 
|----------------------------------------------------------|
"""
def load_fix_element(name, direction) -> bool:
    if name in staticLocHT:
        return False

    staticLocHT[name] = StaticLoc(name, direction)
    return True


def load_movil_element(name, direction, price) -> bool:
    """
    """
    if name[0].upper() == "C":
        if name in carsHT:
            return False
        carsHT[name] = DynamicLoc(name, direction, price)

    if name[0].upper() == "P":
        if name in peopleHT:
            return False
        peopleHT[name] = DynamicLoc(name, direction, price)
    return True


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

    