from min_heap import Heap

class Map:

    """
    Map is a Directed Graph, but with certain helper functions specific to UberMap
    """

    def __init__(self, vertices: list, edges: list):
        # Vertices is a list containing all the vertices as [v0, v1, v2, ..., vn]
        # edges is a list containing all the pairs of vertices and it's distance [[v0, v2, d0], [v4, v7, d1], ..., [v8, vn, dn]]
        self.dict = {}
        self.distances = {}
        self.edges_count = 0

        for vert in vertices:
            self.insert_vertex(vert)

        for (v0, v1, distance) in edges:
            self.insert_directed(v0, v1, distance)

        self.precalculate_distances()

    def precalculate_distances(self):

        for start_key in self.vertices:
            
            self.distances[start_key] = {}

            # Heap used to get the min distance item
            heap = Heap(self.vertices_count)

            # Initializes heap and nodes
            for node_key in self.vertices:
                heap.add(node_key, float("inf"))

            visited_keys = set()

            # Sets the d value of the starting node to 0
            # this way the heap pops the start first
            heap.update_key(start_key, 0)
            
            while len(heap):

                (node_key, node_distance) = heap.pop()

                self.distances[start_key][node_key] = node_distance

                visited_keys.add(node_key)

                for (ady_key, street_length) in self.adjacent_generator(node_key):

                    if ady_key not in visited_keys:

                        # Relax the adjacent
                        ady_distance = heap.access(ady_key)
                        if ady_distance > node_distance + street_length:
                            heap.update_key(ady_key, node_distance + street_length)


    def __repr__(self) -> str:
        return f"Map: \n {self.dict}"

    @property
    def vertices_count(self):
        return len(self.dict.keys())

    @property
    def vertices(self):
        return self.dict.keys()

    def node_adjacent_count(self, v):
        if v not in self.dict:
            raise Exception(f"Trying to access inexistent node <{v}>")

        return len(self.dict[v])

    def insert_directed(self, v0, v1, distance):

        # Insertion in directed graph
        if self._exists_street(v0, v1):
            raise Exception(
                f"Adjacency <{v0}, {v1}> already established, use update instead")

        self.edges_count += 1

        # Adds the vertices if any of these is new
        if v0 not in self.dict:
            self.insert_vertex(v0)

        if v1 not in self.dict:
            self.insert_vertex(v1)

        # Establishes adjacency relationship
        self.dict[v0][v1] = distance

    def insert_vertex(self, v):
        if v in self.dict:
            raise Exception(f"Trying to add an existent vertex: <{v}>")

        self.dict[v] = {}

    def update_street(self, v0, v1, new_weight):
        # Updates the street weight
        # Note that it's in a single direction <v0, v1, new_weight>
        if not self._exists_street(v0, v1):
            raise Exception(f"Trying to update inexistent edge <{v0}, {v1}>")

        self.dict[v0][v1].distance = new_weight

    def _exists_street(self, v0, v1) -> bool:

        if v0 not in self.dict:
            return False

        return v1 in self.dict[v0]

    def adjacent_generator(self, v):

        if v not in self.dict:
            raise Exception(f"Trying to access inexistent node <{v}>")

        for ady_key in self.dict[v].keys():
            # Yields the (key, distance) tuple
            yield (ady_key, self.dict[v][ady_key])