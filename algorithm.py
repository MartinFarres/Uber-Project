from min_heap import Heap
from uber_map import load_map, Map


def weight_insert(graph, node, ady_node, weight):
    
    # Adds both nodes to the graph
    if node not in graph:
        graph[node] = []

    if ady_node not in graph:
        graph[ady_node] = []

    # But the directed edge is node -> ady_node
    graph[node].append((ady_node, weight))


class Node:
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


def dijkstra(map, start_key, find_func, find_count_target):

    edges_count = sum(len(graph[node_key]) for node_key in graph.keys())

    # Stores the Node instances
    nodes = {}          

    # Heap used to get the min distance item
    heap = Heap(edges_count)

    # Initializes heap and nodes
    for node_key in graph.keys():
        nodes[node_key] = Node(node_key)
        heap.add(node_key, float("inf"))

    visited_keys = set()

    # Sets the d value of the starting node to 0
    # this way the heap pops the start first
    heap.update_key(start_key, 0)
    nodes[start_key].d = 0
    find_count = 0
    ends = []
    while len(heap):

        (node_key, d) = heap.pop()
        
        visited_keys.add(node_key)

        # Gets the node, containing d, and parent data
        node = nodes[node_key]

        # Tests if node id valid
        parent_key = node.parent.key if node.parent is not None else None
        if find_func(node_key, parent_key):
            find_count += 1
            ends.append(node)
            if find_count == find_count_target:
                break

        for ady, weight in graph[node_key]:

            if ady not in visited_keys:

                ady_node = nodes[ady]

                # Relax the adyacent
                modified = relax(node, ady_node, weight)

                # Only if the relax call modified the value
                if modified:
                    heap.update_key(ady, ady_node.d)

    results = []
    for end_node in ends:
        
        # Disconnected
        if end_node.parent is None:
            continue

        # Traverses the path backwards, using the parent attribute 
        path = []
        parent = end_node
        while parent is not None:
            path.append(parent.key)
            parent = parent.parent

        results.append(DijkstraOutput(path, end_node.d))

    return results

if __name__ == "__main__":

    map = Map([], [])
    graph = {}

    # Connected group
    map.insert_directed("s", "t", 10)
    map.insert_directed("s", "y", 5)
    map.insert_directed("t", "y", 2)
    map.insert_directed("t", "x", 1)
    map.insert_directed("y", "t", 3)
    map.insert_directed("y", "z", 2)
    map.insert_directed("y", "x", 9)
    map.insert_directed("z", "s", 7)
    map.insert_directed("z", "x", 6)
    map.insert_directed("x", "z", 4)

    # unconnected group
    map.insert_directed("m", "n", 4)

    dijkstra_results1 = dijkstra(map, "s", (lambda x, y : x == "x"), 1)

    if len(dijkstra_results1):
        print("Path from 's' to 'x':", dijkstra_results1[0].path, dijkstra_results1[0].weight)
    else:
        print("Unable to get to 'x' from 's'")

    dijkstra_results2 = dijkstra(map, "s", (lambda x, y : x == "n"), 1)

    if len(dijkstra_results2):
        print("Path from 's' to 'n':", dijkstra_results2[0].path, dijkstra_results2[0].weight)
    else:
        print("Unable to get to 'n' from 's'")