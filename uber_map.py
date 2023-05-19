import os


class AdyNode:
    """
    Stored in the adjacency list, represents an adyacent node in the graph
    """
    def __init__(self, key, distance) -> None:
        self.key = key
        self.distance = distance

class Map:

    """
    Map is a Directed Graph, but with certain helper functions specific to UberMap
    """
    def __init__(self, vertices: list, edges: list):
        # Vertices is a list containing all the vertices as [v0, v1, v2, ..., vn]
        # eges is a list containing all the pairs of vertices and it's distance [[v0, v2, d0], [v4, v7, d1], ..., [v8, vn, dn]]
        self.dict = {}

        for vert in vertices:
            self.dict[vert] = []

        for (v0, v1, distance) in edges:
            self.insert_directed(v0, v1, distance)

    def insert_directed(self, v0, v1, distance):
        # Insertion in directed graph
        if self.exists_street(v0, v1):
            print(f"Warning: trying tho add an already existing edge ({v0}, {v1})")
            return

        if v0 not in self.dict:
            self.dict[v0] = []

        self.dict[v0].append(AdyNode(v1, distance))

    def insert_bidirected(self, v0, v1, distance):
        self.insert_directed(v0, v1, distance)
        self.insert_directed(v1, v0, distance)


    def exists_street(self, v0, v1) -> bool:

        if v0 not in self.dict:
            return False
        
        for ady_node in self.dict[v0]:
            if ady_node.key == v1:
                return True
        
        return False
    

def load_map(path):
    """
    TODO
    1) If the map is serialized, should deserialize with pickle
    2) If the map isn't serialized, creates one for the first time
    """
    if os.path.exists(path):
        # Loads the map with pickle
        pass

    else:
        # Hardcoded Bidirected Grid 4x4 example. Where all north, south, west and east nodes are connected
        # 0  1  2  3 
        # 4  5  6  7
        # 8  9  10 11
        # 12 13 14 15

        size = 4
        street_length = 1
        V = list(range(size * size)) # 100 vertices
        map = Map(V, [])
        for y in range(size):

            for x in range(size):                        
                
                # Current vertex
                v = y * size + x

                # If the adyacent node is available (end of grid case consideration)
                if x > 0:
                    left_node = y * size + (x - 1)
                    map.insert_directed(v, left_node, street_length)

                if x < size - 1:
                    right_node = y * size + (x + 1)
                    map.insert_directed(v, right_node, street_length)

                if y > 0:
                    top_node = (y - 1) * size + x
                    map.insert_directed(v, top_node, street_length)

                if y < size - 1:
                    bottom_node = (y + 1) * size + x
                    map.insert_directed(v, bottom_node, street_length)

        return map