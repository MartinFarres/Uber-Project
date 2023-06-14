from min_heap import Heap
from typing import List, Dict
from dynamic_location import DynamicLoc
from uber_map import Map
from core_functions import create_map_core

class DijkstraNode:
    def __init__(self, key) -> None:
        self.key = key
        self.d = float("inf")


def dijkstra(map, start_key):

    # Heap used to get the min distance item
    heap = Heap(map.vertices_count)

    # Initializes heap and nodes
    for node_key in map.vertices:
        heap.add(node_key, float("inf"))

    visited_keys = set()

    # Sets the d value of the starting node to 0
    # this way the heap pops the start first
    heap.update_key(start_key, 0)
    
    while len(heap):

        (node_key, node_distance) = heap.pop()

        print(f"Distance to {node_key}: {node_distance}")

        visited_keys.add(node_key)


        for (ady_key, properties) in map.adyacent_generator(node_key):

            if ady_key not in visited_keys:

                # Relax the adjacent
                ady_distance = heap.access(ady_key)
                if ady_distance > node_distance + properties.distance:
                    heap.update_key(ady_key, node_distance + properties.distance)


if __name__ == "__main__":

    
    map = create_map_core("map.txt")
    dijkstra(map, "e1")
    print(map)
