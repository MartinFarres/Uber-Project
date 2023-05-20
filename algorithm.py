from min_heap import Heap
from typing import List, Dict
from dynamic_location import DynamicLoc


class DijkstraNode:
    def __init__(self, key) -> None:
        self.key = key
        self.d = float("inf")
        self.parent = None


def relax(node_u, node_v, weight):

    if node_v.d > node_u.d + weight:
        node_v.d = node_u.d + weight
        node_v.parent = node_u
        return True
    
    return False


class DijkstraOutput:
    def __init__(self, path, weight) -> None:
        self.path = path
        self.weight = weight


def dijkstra(map, start_key, end_key) -> DijkstraOutput:
    """
    Returns the shortest path between start and end it's weight
    Note that the return list is [end, ..., start] is reversed
    """
    # Stores the DijkstraNode instances
    nodes = {}          

    # Heap used to get the min distance item
    heap = Heap(map.vertices_count)

    # Initializes heap and nodes
    for node_key in map.vertices:
        nodes[node_key] = DijkstraNode(node_key)
        heap.add(node_key, float("inf"))

    visited_keys = set()

    # Sets the d value of the starting node to 0
    # this way the heap pops the start first
    heap.update_key(start_key, 0)
    nodes[start_key].d = 0
    while len(heap):

        (node_key, d) = heap.pop()
        
        visited_keys.add(node_key)

        # Gets the node, containing d, and parent data
        node = nodes[node_key]

        # Tests if the end is reached
        if node_key == end_key:
            break

        for (ady_key, properties) in map.adyacent_generator(node_key):
            
            if ady_key not in visited_keys:
                
                # This node contains the Dijkstra requiered attributes (.d)
                ady_dijkstra_node = nodes[ady_key]

                # Relax the adyacent
                modified = relax(node, ady_dijkstra_node, properties.distance)

                # Only if the relax call modified the value
                if modified:
                    heap.update_key(ady_key, ady_dijkstra_node.d)

    # Traverses the path backwards, using the parent attribute 
    end_node = nodes[end_key]
    path = []

    if end_node.parent is None:
        return None

    parent = end_node
    while parent is not None:
        path.append(parent.key)
        parent = parent.parent

    return DijkstraOutput(path, end_node.d)


class FindCarsOutput:
    def __init__(self, car, path, price) -> None:
        self.car_name = car
        self.path = path
        self.price = price


def find_nearest_cars(map, cars: Dict[str, DynamicLoc], person: DynamicLoc, max_cars_count, price_function) -> List[FindCarsOutput]:

    """
    Returns a list of FindCarsOutput in order, where the first element is the nearest and the last the furthest
    """

    # Used to sort the cars based on the final price
    heap = Heap(len(cars))

    # Contains path for each result
    results = dict()

    for car in cars.values():
        
        # Picks the second node of the directed edge (u, v)
        start_node = car.direction.edge2

        # The car should be able to access where the person is,
        # that's why the end node is the firt node
        end_node = person.direction.edge1

        # If we access this nodes, we are missing the following distances
        missed_distance = car.direction.d2 + person.direction.d1

        # Now used dijkstra
        dijkstra_result = dijkstra(map, start_node, end_node)

        # Car unable to get to person
        if dijkstra_result is None:
            continue

        total_distance = missed_distance + dijkstra_result.weight
        results[car.name] = dijkstra_result.path 
        heap.add(car.name, total_distance)

    # Sorts with heap sort
    added_cars_count = 0
    sorted_cars = []
    while added_cars_count < max_cars_count and len(heap) > 0:

        (car_name, distance) = heap.pop()
        car_path = results[car_name]
        price = price_function(cars[car_name], distance)
        sorted_cars.append(FindCarsOutput(car_name, car_path, price))

    return sorted_cars
