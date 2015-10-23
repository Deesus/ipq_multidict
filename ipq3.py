"""
Author: Dee Reddy
created: 3/19/2015
updated: 10/23/2015

Indexed priority queue (binary heap). Uses hash function for fast random look-ups.

Limitations:
    - Items inserted into heap must not be mutable objects (e.g. arrays,
    dicts, etc.)

You can support multiple keys with this data structure:
    {item: [index_in_heap [, index_in_heap_if_copies] }, priority_value

    -If you have collisions -- i.e. non-unique items the function will go
    through list of indices where the item resides in heap, move to that index,
    then pop that item from the hash-value (the list of heap indicies given
    object) as well as the heap

    -For example, suppose our heap looks like this:
    >>> my_heap = [['shiva', 35], ['lakshmi', 164], ['dee', 684], ['vlad', 285], ['dee', 275], ['dee', 824], ['shiva', 1132]]

    Internally, we have a hash of every item plus their position in the heap
    (the heap is a 2D array). The internal hash of index positions would be:
    {'vlad': [3], 'shiva': [0, 6], 'lakshmi': [1], 'dee': [5, 2, 4]}

    If we wanted to delete key, say, 'dee' from our heap, we would do this:
    >>> my_heap.delete('dee')

    The delete() method will lookup the key 'dee' in the internal hash; it
    will find the key and see that its associated value -- an array -- it will
    pop the last element in this array. If, after popping, the array is empty,
    the hash key will be deleted as well. The popped value is the position
    (index) in the heap -- which is also happens to be an array. Using this
    index, the function will pop the object -- ['dee', 275] -- from the heap
    array, then go on to maintain the heap invariance as expected.


supports:
-select key 				O(1)
-insert key 				O(log n)
-delete key 				O(log n)
-extract min 				O(log n)
-change key 				O(log n)
-peek (select)  			O(1)
-heapify (transform list)   O(n)
-print heap(UNIMPLEMENTED)  O(n)
-print size(UNIMPLEMENTED)  O(1)

to do:
1) create print function that traverses down the tree to properly calculate
    correct spacing between each leaf
2) learn how to create a module, and how to import a class from a module/
    external file
3) see programming tips on reducing code (you can use it to specify min/max
    heap with minimum extra lines)
4) add operation -- select item (i.e. find item by hash key)
5) add max heap (should we us negative keys?), and perhaps also use regular
    heap (w/o indexing) that doesn't use tuples
6) support for keys of same value
    6.5) support for inserting tuples/lists?
7) heapify should convert into tuples not single numbers. it doesn't support
    IPQ yet.
    7.5) make heapify use iterative loop rather than recursion
8) reword key, item, and element so that they're not confusing; i.e. the hash
    key is different from priority key. Perhaps just use the term 'priority'
    when refering to it.
9) perhaps tidy up the bubble up/down by explicitly using variable
10) use polymorphism so that we can use brackets (like in hashes) for our
    MinIPQ operations instead of method calls. E.g. pq["white devil"] = 666
11) add more heap operations: update/replace, merge.
12) create __rep__ and __print__ methods that displays the heap properly
"""
__author__ = ('Dee Reddy', 'github.com/Ogodei')

import math
import random


class MinIPQ:
    """ Maps dict keys (keys) to priority keys (values), implemented as
        a list. Maintains an internal, heap data structure.
    """

    def __init__(self, default=None):
        """
        N: length of heap.
        heap: is array whose elements contain list of items and
        priority keys respectively.
        position is a hash whose keys are the inserted items and values are
        index positions in heap array.
        """

        self.position = {}
        if default is None:
            self.N = 0
            self.heap = []
        elif type(default) == list:
            self._heapify(default)

    def insert(self, item, key=None):
        """ Inserts/pushes item, with priority, into heap. If no priority
            is given, the method tries to set the priority equal to the
            item (the item must then be numeric, otherwise raises error).

            No

        Args:
            item: item to be into heap.
            key: item's priority key

        Example:
            my_data = MinIPQ()                  # create empty heap instance
            my_data.insert('Deesus', 7)         # inserts string 'Deesus' with a priority of 7
            my_data.insert('Tamerlane', 121)    # inserts string 'Tamerlane' with a priority of 121

        Raises:
            TypeError: missing required argument.
            TypeError: priority key not be a numeric value.
            ValueError: if item already exists in dict
        """

        if key is None:
            key = item
        if not (type(key) is int or type(key) is float):
            raise TypeError("Priority key must be a numeric value.")
        elif item in self.position:
            raise KeyError("Item already exists in heap.")

        self.position[item] = self.N  # set position to heap index (length-1) before incrementing length
        self.N += 1
        self.heap.append([item, key])
        self._bubble_up(self.N - 1, item)  # "N-1" because of 0-indexing

    def delete(self, item):
        """ Deletes item from the heap.

        Given a particular dict key, the function removes the item
        (key-value pair) from the heap while maintaining the heap invariant.

        Args:
            item: the dict key to be deleted (not to be confused with the
            heap's internal priority key). For example, given a heap of student
            names, we can delete a specific entry with the following:

            ipq_instance.delete("Yuji")

        Raises:
            KeyError: if item-key does not exist in the heap.
        """

        if item not in self.position:
            raise KeyError("Item does not exist in the heap.")

        self.N -= 1
        index = self.position[item]
        del self.position[item]
        element = self.heap.pop()

        # if we pop the item we wanted to delete (last-most item), we can end
        if index == self.N:
            return

        # replace with item at end of heap & bubble down:
        self.heap[index] = element
        self._bubble_down(index, element[0])

    def extract_min(self):
        """ Pops and returns the root (top priority) from heap.

        Returns:
            A a list of item (key) and its associated priority (value).
            For example: ['Oranges', 17]
        Raises:
            ValueError: if heap is empty.
        """

        if self.N == 0:
            raise ValueError("heap is empty")

        element = self.heap[0]
        self.delete(element[0])
        return element

    def peek(self):
        """ Returns root (top priority) without popping it from the heap."""
        return self.heap[0]

    def change_priority(self, item, key):
        """ Updates the priority value of given item to new priority.

        In order to avoid confusion between the term "key" in a priority queue
        and the term "key" in a hash/dict, we will refer to "priority" as the
        value that determines the placement of said value/item in the heap.

        Changes the priority of a given dict key to a new value
        while maintaining heap invariant.

        Args:
            item: the dictionary key
            key: the new priority key to be set
        """

        index = self.position[item]
        self.heap[index][-1] = key

        self._bubble_up(self.position[item], item)
        self._bubble_down(self.position[item], item)

        # need to convert elements into tuples to be consistent with other
        # functions; we could make a separate class for simple heap (rather
        # than indexed heaps)

    #################################
    #       Helper Functions 		#
    #################################

    def _bubble_up(self, i, item):
        """
            Args:
                i: index (i.e. priority) of item to bubble down
        """

        while (i > 0) and self.heap[(i - 1) // 2][-1] > self.heap[i][-1]:  # might be more clean if we defined variable key = heap[i][-1]
            p = (i - 1) // 2  # formula for finding parent index (0-based index)
            i = self._swap(i, p)  # swap values and indices
        self.position[item] = i

    def _bubble_down(self, i, item):
        """
            Args:
                i: index (i.e. priority) of item to bubble down.
                c: child index.
        """

        while 2 * i + 1 < self.N:  # equality ensures that there is at least the left index
            c = 2 * i + 1  # formula for left child (0-based indexing)

            # (c+1 < N) ensures a right child; select the smallest to bubble down:
            if (c + 1 < self.N) and self.heap[c + 1][-1] < self.heap[c][-1]:  # if right child is smaller, update c to be right (c+1)
                c += 1
            # check if heap property is fulfilled:
            if self.heap[i][-1] < self.heap[c][-1]:
                break

            i = self._swap(i, c)  # swap values and indices
        self.position[item] = i

    def _swap(self, i, j):
        """ Swaps heap items for both bubbling up/down; returns swapped index (j).
            Also updates child/parent hash to point to updated array position.
            
            Args:
                i = index of item to bubble
                j = index of parent/child
        """

        self.position[self.heap[j][0]] = i
        self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
        return j

    # make sure you name 'heapify' appropriately: min/max, build/create heap?
    # if it is part of MinIPQ -- then it should be min.
    def _heapify(self, aArray):
        """Returns a new heap from a given list in O(n) time."""
        self.heap = aArray
        self.N = len(self.heap)

        for i in range((self.N - 2) // 2, -1, -1):  # in 0-based index, last-most parent must be (length-2)//2
            self._heapify_loop(i)
        return self.heap

    def _heapify_loop(self, i):
        """ Starting from the penultimate level (height) of tree, we check if 
            parent node is the smallest; if not, recurse (swap downward) until 
            heap property is fulfilled
        """

        l = (i * 2) + 1
        r = (i * 2) + 2
        min_ = i

        if (l <= self.N - 1) and (self.heap[l] < self.heap[i]):
            min_ = l
        if (r <= self.N - 1) and (self.heap[r] < self.heap[min_]):
            min_ = r

        if min_ != i:
            self.heap[i], self.heap[min_] = self.heap[min_], self.heap[i]
            self._heapify_loop(min_)

    def print_heap(self):
        """ A visualization tool to print given heap in a pyramid shape.

            A simple printout function that represents the object in the more
            visually appropriate 'heap-like' shape -- i.e. a pyramid. For example:

                     470
              1475          143
            94   1829   1306   12   738

            In order to calculate the correct padding/spacing for each item, the
            function iterates through the entire data structure, computing the
            total number of characters of the item (both the priority as well as
            the value associated with it). After the first pass, the priority-item
            pair with the most characters is determined. This max value is used
            to determine the spacing/padding evenly for each value-pair at each
            level of the heap. Aside: since `print_heap` requires two passes, the
            time complexity is technically O(2n).
        """
        # why don't we just use padding format for strings? We can use padding
        # after and padding before

        if not self.heap:
            return
        height = int(math.log(len(self.heap), 2)) + 1

        iii = 0
        reps = 1
        for line in range(1, height + 1):
            print("  " * (height - line), end='')  # padding

            try:
                for _ in range(reps):
                    print(self.heap[iii], end=' ')
                    iii += 1
            except IndexError:
                pass
            print()
            reps *= 2

#####################################
#            test client            #
#####################################

# parametrize the class -- so that we can do this:
# "my_heap = MinIPQ([23,2563,7254,234]) >>> new heap"

if __name__ == '__main__':
    pass
    # # test heapified array:
    # testArray = []
    # for _ in range(20):
    #     randNumber = random.randrange(1, 2000)
    #     testArray.append(randNumber)
    #
    # arr_to_heap = MinIPQ(testArray)
    # print(arr_to_heap.heap, '\n')
    # arr_to_heap.print_heap()
    # print('-'*60, '\n')
    #
    # # test serialized heap:
    serialized_heap = MinIPQ()
    array = []
    for _ in range(20):
        input = 'x' + str(_) + str(random.randrange(200))
        array.append(input)
        serialized_heap.insert(input, random.randrange(1, 2000))

    print(array, '\n')
    serialized_heap.print_heap()

    #####################
    # test must accept (must heapify) key-val pairs and dicts

    # datastructure must be stored in a hash, not array
    # pdict is implemented as follows: {item: priority, item2: priority}

    # if we use dict, then we can't have arrays/hashes/collections as item since hash doesn't allow mutable types as hash key

    #data = [[2, []]]
