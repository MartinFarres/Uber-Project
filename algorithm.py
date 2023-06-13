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


