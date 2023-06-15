import sys
import file_manager as fm
from core_functions import create_map_core, load_fix_element_core, load_movil_element_core, create_trip_core
from direction import Direction


def load_fix_element(data, fix_element_name, serialized_direction):
    # Deserializes the cmd argument and calls load_fix_element_core
    direction = deserialize_direction(serialized_direction)
    success = load_fix_element_core(data, 
        fix_element_name, direction)

    if not success:
        print(f"Ya existe una ubicación fija llamada: {fix_element_name}")


def load_movil_element(data, movil_name, serialized_direction, price):
    direction = deserialize_direction(serialized_direction)
    success = load_movil_element_core(data,
        movil_name, direction, price )

    if not success:
        print(f"Ya existe una ubicación móvil llamada: {movil_name}")


def create_trip(data, person_name, second_value):
    # Contains a direction
    if second_value[0] == '<':
        direction = deserialize_direction(second_value)
    else:
        static_loc_name = second_value
        static_loc = data.static_loc_HT[static_loc_name]
        direction = static_loc.direction
        
    person = data.people_HT[person_name]
    sorted_cars = create_trip_core(data, person, direction)
    
    if len(sorted_cars) == 0:
        print("Monto insuficiente o Ningun auto disponible")
        return
    
    print("A que auto quieres llamar?")
    for i, (car, price) in enumerate(sorted_cars):
        print(f"{i + 1}. {car.name} con un precio de ${price}")
    inp = input("Seleccione utilizando números: ")
    
    try:
        if int(inp) > len(sorted_cars):
            print("Viaje cancelado, opción inválida")
            return
    except:
        print("Viaje cancelado, la opción debe ser un número entero")
        return

    selected_car = sorted_cars[int(inp) - 1][0]
    selected_car_price = sorted_cars[int(inp) - 1][1]
    
    # Moves to the new direction
    person.direction = direction
    selected_car.direction = direction

    # Updates person's money
    person.price -= selected_car_price
    

def create_map(data, local_path):
    data.map = create_map_core(local_path)
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

    return Direction(edge1, edge1_distance, edge2, edge2_distance)


if __name__ == '__main__':
    data = fm.initialization_data()
    args = sys.argv
    func_name = args[1][1:]

    globals()[func_name](data, *sys.argv[2:])

    fm.saves_data(data)
