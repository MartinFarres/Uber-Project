class Heap:
    """
    Min heap, but stores a (key, value) pair
    This (key, value) structure is used in Prim and Kruskal 
    algorithms to store the node and the weight.
    Update and access use the key parameter. Performance is archieved
    by using an internal dictionary that holds the {key : index} pairs
    """
    def __init__(self, size: int):
        self._array = [None for _ in range(size)]
        self._size = size
        self._insert_index = 0
        self._key_positions = {} # Used to store the position of the key in the heap

    def __repr__(self) -> str:
        return repr(self._array)

    def __len__(self):
        return self._insert_index

    def __contains__(self, key):
        return key in self._key_positions

    def add(self, key, value):
        # Operation O(log(n))
        if self._size == self._insert_index:
            raise OverflowError(f"Overflow, array of size {self._size}")

        self._key_positions[key] = self._insert_index
        self._array[self._insert_index] = (key, value)
        self._insert_index += 1

        self._heapify_up()

    def pop(self):
        # O(log(n))
        # Removes the min element from the heap and returns
        pair = self._array[0]
        self._insert_index -= 1

        self._swap(0, self._insert_index)
        self._array[self._insert_index] = None
        self._heapify_down()
        del self._key_positions[pair[0]]
        return pair
    
    def access(self, key):
        # O(1)
        return self._array[self._key_positions[key]][1]
    
    def update_key(self, key, value):
        # O(log(n))
        """
        Used to modify the value of the key.
        Heapifies up or down, if the value is smaller
        or greater than the previous
        """
        index = self._key_positions[key]
        pair = self._array[index]

        self._array[index] = (key, value)
        if value < pair[1]:
            self._heapify_up(index)
        else:
            self._heapify_down(index)
    
    def _heapify_up(self, i=None):
        """
        Used after insert
        Starts from index i, usually the last added element
        and then heaps up, until the heap property is restored
        """
        if i is None:
            i = self._insert_index - 1

        while i > 0 and self._array[i][1] < self._array[self._parent(i)][1]:
            # Swaps
            parent_index = self._parent(i)
            self._swap(i, parent_index)
            i = parent_index

    def _heapify_down(self, i=0):
        """
        Used after delete
        Starts from index i, usually i = 0
        and then heaps down, until the heap property is restored
        """
        while self._has_left_child(i):
            
            # Gets the smallest child
            smaller_child_index = self._left_child(i)
            if self._has_right_child(i) and self._array[smaller_child_index][1] > self._array[self._right_child(i)][1]:
                smaller_child_index = self._right_child(i)

            # Finds the place
            if self._array[smaller_child_index][1] > self._array[i][1]:
                return
            
            self._swap(smaller_child_index, i)
            i = smaller_child_index

    """
    Acessing children and parent is made using 
    the matematical properties of Heap
    """
    def _left_child(self, index):
        return index * 2 + 1

    def _right_child(self, index):
        return index * 2 + 2

    def _parent(self, index):
        if index % 2 == 0:
            return (index - 2) // 2
        return (index - 1) // 2
    
    def _has_left_child(self, index):
        index = self._left_child(index)
        if index > self._size -1:
            return False
        
        return self._array[index] != None
    
    def _has_right_child(self, index):

        index = self._right_child(index)
        if index > self._size -1:
            return False
        return self._array[index] != None

    def _swap(self, index0, index1):

        self._key_positions[self._array[index0][0]] = index1
        self._key_positions[self._array[index1][0]] = index0

        temp = self._array[index1]
        self._array[index1] = self._array[index0]
        self._array[index0] = temp


if __name__ == "__main__":
    # Simple test

    weights = [2, 3, 9, 6, 1, -1]
    heap = Heap(len(weights))
    for i, weight in enumerate(weights):
        heap.add(i, weight)

    heap.update_key(2, -4)

    while len(heap):
        print(heap.pop())
        print(heap)