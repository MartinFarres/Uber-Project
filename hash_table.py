class HashTable:
    
    """
    Hash Table where the collisions are handled with chaining
    """

    def __init__(self, hash_function=None, slots=None):

        # Defines the hash function, if not provided
        # In this implementation, the default is the module fuction
        # The table contians n slots

        if slots is None:
            slots = 9

        if hash_function is None:
            self.hash_function = lambda x : x % slots
        
        else:
            self.hash_function = hash_function


        # Initializes the table, in each slot an empty linked list is initialized
        self.table = [[] for _ in range(slots)]      
            

    def __getitem__(self, key):
        return self.search(key)
    
    def __setitem__(self, key, value):
        sucess = self.update(key, value)
        if not sucess:
            raise IndexError(f"HashTable doesn't contain the key: {key}, unable to update it's value")
    
    def __contains__(self, key):
        return self.contains(key)

    def contains(self, key):
        hash_value = self.hash_function(key)
        linked_list = self.table[hash_value]

        for node in linked_list:
            node_key = node[0]
            if node_key == key:
                return True
        return False

    def update(self, key, value):
        hash_value = self.hash_function(key)
        linked_list = self.table[hash_value]

        for node in linked_list:
            node_key = node[0]
            if node_key == key:
                node[1] = value
                return True
        return False


    def insert(self, key, value):
        """Insertion. Appends the tuple (key, value) to the corresponding list"""
        hash_value = self.hash_function(key)
        self.table[hash_value].append([key, value])


    def search(self, key):
        """Given the key of the element, tries to find it's
        value inside the corresponding list"""
        hash_value = self.hash_function(key)

        linked_list = self.table[hash_value]

        for node in linked_list:
            node_key = node[0]
            if node_key == key:
                return node[1]
            

    def delete(self, key):
        """Removes the element from the list"""
        # This implementation of Dictiorary allows repeated
        # keys, that's why only one of those is removed, 
        # following FIFO
        hash_value = self.hash_function(key)
        linked_list = self.table[hash_value]

        # Tries to find the key inside the 
        node_index = -1

        for i, node in enumerate(linked_list):
            node_key = node[0]
            if node_key == key:
                node_index = i
                break
            
        if node_index == -1:
            return 
        
        del linked_list[node_index]

    def display(self):
        for i, l in enumerate(self.table):
            message = f"[{i}]" + repr(l)
            print(message)
