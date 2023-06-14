from uber_map import Map
from direction import Direction
from dynamic_location import DynamicLoc
from static_location import StaticLoc
import file_manager as fm
from min_heap import Heap


def create_map_core(path):
    mapVar = fm.read_map_var(path)
    return Map(mapVar[0], mapVar[1])


def load_fix_element_core(data, name, direction) -> bool:
    if name not in data.static_loc_HT:
        data.static_loc_HT[name] = StaticLoc(name, order_direction(data.map, direction))
        return True
    return False


def load_movil_element_core(data, name, direction, price) -> bool:
    if name[0].upper() == "C":
        if name in data.cars_HT:
            return False
        data.cars_HT[name] = DynamicLoc(name, order_direction(data.map, direction), int(price))

    if name[0].upper() == "P":
        if name in data.people_HT:
            return False
        data.people_HT[name] = DynamicLoc(name, order_direction(data.map, direction), int(price))
    return True

def create_trip_core(data, p: DynamicLoc, direction: Direction):
    p.direction = order_direction(data.map, p.direction)
    direction = order_direction(data.map, direction)

    # Unreachable
    if get_distance(data.map, p.direction, direction) is None:
        return False
    
    
    # Calculates the distances for all the cars and sorts with heap sort
    cars = Heap()
    for car in data.cars_HT.values():
        distance = get_distance(data.map, car.direction, p.direction)
        if distance is None:
            continue
        cars.add(car, distance)
    
    # Gets top 3
    sorted_cars = []
    for _ in range(min(len(cars), 3)):
        car = cars.pop()
        price = (car[1] + car[0].price) / 4.0

        # Can't afford car
        if price > p.price:
            continue

        sorted_cars.append((car[0], price))
        
    return sorted_cars

# Helping Function ------------------------------------------------------------------

def order_direction(map: Map, dir):
    if map.exists_street(dir.edge1, dir.edge2):
        if map.exists_street(dir.edge2, dir.edge1):
            if int(dir.edge1[1:]) > int(dir.edge2[1:]):
                return Direction(dir.edge2, dir.d2, dir.edge1, dir.d1) 
        return dir
    return Direction(dir.edge2, dir.d2, dir.edge1, dir.d1)


def get_distance(map: Map, d_start: Direction, d_end: Direction): 
    # When d_start and d_end are in the same street 
    if (d_start.edge1 == d_end.edge1) and (d_start.edge2 == d_end.edge2):
        
        # if d_end is in front of d_start, returns the distance
        dist = d_end.d1 - d_start.d1 

        # 1) If the distance is >= 0 it means that the person is in front of the car, and returns the distance
        # 2) If the street is bidirected, abs is requiered and returns the correct distance
        if dist >= 0 or map.exists_street(d_end.edge2, d_end.edge1):
            return abs(dist)

    acc1 = d_start.d2 + d_end.d1 #Accumulate distance 
    dist1 = map.get_edges_distance(d_start.edge2, d_end.edge1)
    min_dist = None
    
    if dist1 != None:
        dist1 += acc1
        min_dist = dist1

    # If Person is in a two ways Street
    if map.exists_street(d_end.edge2, d_end.edge1):
        acc2 = d_start.d2 + d_end.d2
        dist2 = map.get_edges_distance(d_start.edge2, d_end.edge2)
        if dist2 != None:
            dist2 += acc2
            if min_dist is None:
                min_dist = dist2
            elif min_dist > dist2:
                min_dist = dist2

    return min_dist



if __name__ == "__main__":
    data = fm.initialization_data()
    map = data.map

    # CASO SIMPLE res:170
    #car_dir = Direction("e1", 20, "e2", 80)
    #p_dir = Direction("e6", 40, "e7", 10)
    
    # Caso Posicion Misma Calle - (Discapacitado) - Auto por delante 
    # res: 170
    # p_dir = Direction("e10", 10, "e8", 40)
    # car_dir = Direction("e10", 40, "e8", 10)

    # Caso Posicion Misma Calle - (Discapacitado) - Persona por delante
    # res: 30
    # car_dir = Direction("e10", 10, "e8", 40)
    # p_dir = Direction("e10", 40, "e8", 10)

    # Caso que pasa por bidirigida - res:10
    p_dir = order_direction(map, Direction("e10", 20, "e11", 30))
    car_dir = order_direction(map, Direction("e6", 40, "e2", 10))
    
    print(get_distance(map, car_dir, p_dir))
   