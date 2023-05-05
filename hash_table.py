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
            self.hash_function = lambda x: x % slots

        else:
            self.hash_function = hash_function

        # Initializes the table, in each slot an empty linked list is initialized
        self.table = [[] for _ in range(slots)]

    def __getitem__(self, key):
        return self.search(key)

    def __setitem__(self, key, value):
        sucess = self.update(key, value)
        if not sucess:
            raise IndexError(
                f"HashTable doesn't contain the key: {key}, unable to update it's value")

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


class OpenHashTable:

    """
    Hash Table using open adressing
    """

    # Initialization functions for all the probing methods
    def initialize_linear_probing(self, aux_hash, m):
        self.m = m
        self.hash_function = lambda k, i: (aux_hash(k) + i) % self.m
        self._initialize_table()
        return self

    def initialize_quadratic_probing(self, aux_hash, c1, c2, m):
        self.m = m
        self.hash_function = lambda k, i: (
            aux_hash(k) + c1 * i + c2 * i * i) % self.m
        self._initialize_table()
        return self

    def initialize_double_hashing(self, aux_hash1, aux_hash2, m):
        self.m = m
        self.hash_function = lambda k, i: (
            aux_hash1(k) + aux_hash2(k) * i) % self.m
        self._initialize_table()
        return self

    def _initialize_table(self):
        # Creates the empty table of length self.m, so self.m should be initialized
        self.table = [(None, None) for _ in range(self.m)]
        # Operator overloading

    def __getitem__(self, key):
        sucess = self.search(key)
        if sucess is None:
            raise Exception(f"Key: ({key} not found)")
        return sucess

    def __setitem__(self, key, value):

        # If already stored, modifies the value
        if self.contains(key):
            # Finds the key and modifies the value
            for i in range(self.m):
                hash_value = self.hash_function(key, i)

                if self.table[hash_value][0] == key:
                    self.table[hash_value] = (key, value)
                    return

            # Shouldnt get here
            assert False

        # Otherwise inserts
        self.insert(key, value)

    def __contains__(self, key):
        return self.contains(key)

    def insert(self, key, value):

        for i in range(self.m):
            hash_value = self.hash_function(key, i)

            table_tuple = self.table[hash_value]
            tuple_key = table_tuple[0]

            if tuple_key is None or tuple_key == "deleted_element":
                self.table[hash_value] = (key, value)
                return

        # No slot available
        raise Exception("Hash overflow")

    def search(self, key):

        for i in range(self.m):
            hash_value = self.hash_function(key, i)
            table_tuple = self.table[hash_value]
            tuple_key = table_tuple[0]

            if tuple_key == key:
                return table_tuple[1]

            if tuple_key is None:
                return None

    def delete(self, key):

        for i in range(self.m):
            hash_value = self.hash_function(key, i)

            if self.table[hash_value][0] == key:
                self.table[hash_value] = ("deleted_element", None)
                return True

        return False

    def contains(self, key):
        for i in range(self.m):
            hash_value = self.hash_function(key, i)

            if self.table[hash_value][0] == key:
                return True
        return False

    def display(self):
        for i in range(self.m):
            print(f"[{i}]: {self.table[i]}")
