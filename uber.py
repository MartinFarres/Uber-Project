from hash_table import HashTable
from hash_table import OpenHashTable
# Uber+


def hash_function(key, m):
    # Simetric hash function, hash((v1, v2)) == hash((v2, v1))
    v1, v2 = key

    if v1.key < v2.key:
        v2, v1 = v1, v2

    return (v1.key + v2.key * 100) % m

class Map:
    slots = None
    dic = {}

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.slots = [[] for i in range(len(vertices))]

        for i in range(len(vertices)):
            self.dic[vertices[i]] = i

        for edge in edges:
            self.slots[self.dic[edge[0]]].append(edge[1])
            self.slots[self.dic[edge[1]]].append(edge[0])

class Direction:
    def __init__(self, edge1, d1, edge2, d2):
        self.edge1 = edge1
        self.edge2 = edge2
        self.d1 = d1
        self.d2 = d2

staticLocHT = OpenHashTable().initialize_linear_probing()
def load_fix_element(name, direction) -> bool:
    """
    """
            
    if name in staticLocHT:
        return False
    
    staticLocHT[name] = StaticLoc(name, direction)
    return True

