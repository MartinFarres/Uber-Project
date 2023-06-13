import sys
import file_manager as fm
from core_functions import create_map_core, load_fix_element_core, load_movil_element_core


def load_fix_element(data, fix_element_name, serialized_direction):
    # Deserializes the cmd argument and calls load_fix_element_core
    direction = deserialize_direction(serialized_direction)
    success = load_fix_element_core(
        fix_element_name, direction, data.static_loc_HT)

    if not success:
        print(f"A fix element named {fix_element_name} already exists")

    print("Test input data: ", fix_element_name, direction)


def load_movil_element(data, movil_name, serialized_direction):
    direction = deserialize_direction(serialized_direction)
    price = int(args[2])
    success = load_movil_element_core(
        movil_name, direction, price, data.cars_HT, data.people_HT)

    if not success:
        print(f"A Movil element named {movil_name} already exists")

    print("Test input data: ", movil_name, direction)


def create_trip(data, person_name, second_value):

    # Contains a direction
    if second_value[0] == '<':
        direction = deserialize_direction(second_value)
        print(person_name, direction)

    else:
        static_loc_name = second_value
        print(person_name, static_loc_name)


def create_map(data, local_path):
    data.main_map = create_map_core(local_path)
    print("map created successfully")


# Helping Functions ----------------------------------------------------------------------------------

def deserialize_direction(serialized_dir: str):
    # Serialized direction is a string in the following format
    # "<e8,10> <e10,40>"
    # This function transforms it to a Direction object instance

    def _deserialize_side(side: str):
        # Sample input: "<e8,10>"
        side = side[1:-1]                              # Removes '<>'
        edge_name, edge_distance_str = side.split(
            ',')  # Separates the edge and the distance
        # Returns the edge name and the integer distance
        return edge_name, int(edge_distance_str)

    left_side, right_side = serialized_dir.split(' ')

    (edge1, edge1_distance) = _deserialize_side(left_side)
    (edge2, edge2_distance) = _deserialize_side(right_side)

    # TODO - Should return direction
    return edge1, edge1_distance, edge2, edge2_distance


if __name__ == '__main__':
    data = fm.initialization_data()

    args = sys.argv
    func_name = args[1][1:]

    globals()[func_name](data, *sys.argv[2:])

    fm.save(data)
