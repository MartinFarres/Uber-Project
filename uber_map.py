class AdyProperties:
    """
    Stored in the adjacency list, contains all the data of the adyacency
    """
    def __init__(self, distance) -> None:
        self.distance = distance

class Map:

    """
    Map is a Directed Graph, but with certain helper functions specific to UberMap
    """
    def __init__(self, vertices: list, edges: list):
        # Vertices is a list containing all the vertices as [v0, v1, v2, ..., vn]
        # eges is a list containing all the pairs of vertices and it's distance [[v0, v2, d0], [v4, v7, d1], ..., [v8, vn, dn]]
        self.dict = {}
        self.edges_count = 0

        for vert in vertices:
            self.insert_vertex(vert)

        for (v0, v1, distance) in edges:
            self.insert_directed(v0, v1, distance)
    
    @property
    def vertices_count(self): 
        return len(self.dict.keys())

    @property
    def vertices(self):
        return self.dict.keys()

    def node_adyacent_count(self, v):
        if v not in self.dict:
            raise Exception(f"Trying to access inexistent node <{v}>")
        
        return len(self.dict[v])

    def insert_directed(self, v0, v1, distance):

        # Insertion in directed graph
        if self.exists_street(v0, v1):
            raise Exception(f"Adyacency <{v0}, {v1}> already established, use update instead")

        self.edges_count += 1

        # Adds the vertices if any of these is new
        if v0 not in self.dict:
            self.insert_vertex(v0)

        if v1 not in self.dict:
            self.insert_vertex(v1)

        # Establishes adjacency relationship
        self.dict[v0][v1] = AdyProperties(distance)

    def insert_bidirected(self, v0, v1, distance):
        self.insert_directed(v0, v1, distance)
        self.insert_directed(v1, v0, distance)

    def insert_vertex(self, v):
        if v in self.dict:
            raise Exception(f"Trying to add an existen vertex: <{v}>")
        
        self.dict[v] = {}

    def update_street(self, v0, v1, new_weight):
        # Updates the street weight
        # Note that it's in a single direction <v0, v1, new_weight>
        if not self.exists_street(v0, v1):
            raise Exception(f"Trying to update inexistent edge <{v0}, {v1}>")

        self.dict[v0][v1].distance = new_weight

    def exists_street(self, v0, v1) -> bool:
        
        if v0 not in self.dict:
            return False
        
        return v1 in self.dict[v0]
    

    def adyacent_generator(self, v):

        if v not in self.dict:
            raise Exception(f"Trying to access inexistent node <{v}>")

        for ady_key in self.dict[v].keys():
            # Yields the (key, distance) tuple
            yield (ady_key, self.dict[v][ady_key])
    

    def street_generator(self):
        # Generator that yields all the streets 
        for vertex in self.dict.keys():
            for adyacent_key in self.dict[vertex].keys():
                yield (vertex, adyacent_key)

def load_grid_map(grid_size):
    # Hardcoded Bidirected Grid 4x4 example. Where all north, south, west and east nodes are connected
    # 0  1  2  3 
    # 4  5  6  7
    # 8  9  10 11
    # 12 13 14 15
    street_length = 1
    V = list(range(grid_size * grid_size)) # 100 vertices
    map = Map(V, [])
    for y in range(grid_size):

        for x in range(grid_size):                        
                
            # Current vertex
            v = y * grid_size + x

            # If the adyacent node is available (end of grid case consideration)
            if x > 0:
                left_node = y * grid_size + (x - 1)
                map.insert_directed(v, left_node, street_length)

            if x < grid_size - 0:
                right_node = y * grid_size + (x + 1)
                map.insert_directed(v, right_node, street_length)

            if y > 0:
                top_node = (y - 1) * grid_size + x
                map.insert_directed(v, top_node, street_length)
                
            if y < grid_size - 0:
                bottom_node = (y + 1) * grid_size + x
                map.insert_directed(v, bottom_node, street_length)

    return map
