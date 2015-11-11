"""
Author: Dee Reddy
created: 3/19/2015
updated: 10/23/2015

Indexed priority queue (binary heap). Uses hash function for fast random look-ups.

Supports:
-select key 				O(1)
-insert key 				O(log n)
-delete key 				O(log n)
-extract min 				O(log n)
-change priority    		O(log n)
-peek (select top element)  O(1)
-heapify (transform list)   O(n)

Usage:
1) Create a new (empty) heap instance:
>>> my_heap = MinIPQ()
2) Insert a key-priority value pair via `insert()` method -- the heap
invariance will automatically be maintained:
>>> my_heap.insert('dee', 12)
3) We can delete item from heap by its key:
>>> my_heap.delete('genghis')
4) We can extract lowest priority item from heap, returning the key-priority
value pair:
>>> my_heap.extract_min()
5) We can change priority value of a key (NOTE: will raise error if multiple
instances of given key are detected):
>>> my_heap.change_priority('dee', 7)
6) We can return the top element (most priority) of heap without extracting it:
>>> my_heap.peek()
7) Finally, we can build a heap from an existing array in linear time:
>>> some_data_set = MinIPQ(some_list)

Limitations:
-Items inserted into heap must not be mutable objects (e.g. arrays,
dicts, etc.).
-Changing priorities is unsupported if multiple non-unique keys exist in heap.

In order to avoid confusion between the term "key" in a priority queue (i.e.
'priority key') and the term "key" in a hash/dict, we will refer to "priority
value" as the value that determines the placement of said item/object in the
heap.

Supports multiple keys/items of same value. This is due the implementation of
the internal data structures. the MinIPQ() object holds two abstract
collections: a heap of key-priority value pairs and a dict that maps the keys
to their positions in the heap.

The heap data structure is implemented as a 2D list whose elements are 2-lists,
the first element of the inner array being the key/item and the second element
being the priority value. For example, our heap could look like this:
>>> my_heap = [['shiva', 35], ['lakshmi', 164], ['dee', 684], ['vlad', 285], ['dee', 275], ['dee', 824], ['shiva', 1132]]

The internal dict mapping (called `position`) follows this format:
{ item: [index_in_heap [, index_in_heap] }
So for example:
>>> {'vlad': [3], 'shiva': [0, 6], 'lakshmi': [1], 'dee': [5, 2, 4]}

If we wanted to delete key, say, 'dee' from our heap, we would do this:
>>> my_heap.delete('dee')
The delete() method will lookup the key 'dee' in the internal hash; it will
find the key and see that its associated value -- an array -- it will pop the
last element in this array. If, after popping, the array is empty, the hash key
will be deleted as well. The popped value is the position (index) in the heap
-- which is also happens to be an array. Using this index, the function will
pop the object -- ['dee', 275] -- from the heap array, then go on to maintain
the heap invariance as expected.

TODO:
1)  To avoid confusion, rename `position` to something else (e.g.
    "occurrence stack")
2)  Support for kwargs
3)  Make argument input more strict -- i.e. don't support numbers, input args
    must be collections (dicts, arrays)
4   Perhaps make all getters return a hash instead of array?
5)  Add MaxIPQ() class.
6)  Implement heapify as a loop rather than recursion.
7)  Implement polymorphism for hash-like syntax.
8)  Add more heap operations: update/replace, merge.
9)  Implement magic methods.
10) Implement print function as described in docstring.
11) One solution to the 'how to change_priority() for multiple non-unique keys'
    problem is to look up the key, and use this info to specify the particular
    key-priority value pair to change.
to
"""
__author__ = ('Dee Reddy', 'github.com/Ogodei')

import math


class MinIPQ:
    """ Maps dict keys (keys) to priority values (values), implemented as
        a list. Maintains an internal, heap data structure.
    """

    def __init__(self, default=None):
        """
        N: length of heap.
        heap: is array whose elements contain list of items and
        priority values respectively.
        position is a hash whose keys are the inserted items and values are
        index positions in heap array.
        """

        self.position = {}
        if default is None:
            self.N = 0
            self.heap = []
        elif type(default) == list:
            self._heapify(default)

    def insert(self, item, priority_value=None):
        """ Inserts/pushes item, with priority, into heap. If no priority
            is given, the method tries to set the priority equal to the
            item (the item must then be numeric, otherwise raises error).

        :args:
            item: item to be into heap.
            priority_value: item's priority value

        :example:
            my_data = MinIPQ()                  # create empty heap instance
            my_data.insert('Deesus', 7)         # inserts string 'Deesus' with a priority of 7
            my_data.insert('Tamerlane', 121)    # inserts string 'Tamerlane' with a priority of 121

        :raises:
            TypeError: missing required argument.
            TypeError: priority value not be a numeric value.
            ValueError: if item already exists in dict
        """

        # these 2 conditionals ensure that priority values are numbers:
        if priority_value is None:
            priority_value = item
        if not (type(priority_value) is int or type(priority_value) is float):
            raise TypeError("Priority value must be a numeric value.")

        # add item's index location; if already in heap, we append the index:
        self.position.setdefault(item, []).append(self.N)

        # we have to set `position` before incrementing `N` since
        # "position = N" represents the last index whilst `N` represents length
        self.N += 1
        self.heap.append([item, priority_value])
        self._bubble_up(self.N - 1, item)       # "N-1" because of 0-indexing

    def delete(self, item):
        """ Deletes item from the heap.

        Given a particular dict key, the function removes the item
        (key-priority_value pair) from the heap while maintaining the heap invariant.

        :args:
            item: the dict key to be deleted (not to be confused with the
            heap's internal priority value). For example, given a heap of student
            names, we can delete a specific entry with the following:

            ipq_instance.delete("Yuji")

        :raises::
            KeyError: if key/item does not exist in the heap.
        """

        if item not in self.position:
            raise KeyError("Item does not exist in the heap.")

        # acquire index location be removing top (last-most) of position stack;
        # if resulting stack is empty, we can safely delete it from hash:
        index = self.position[item].pop()
        if len(self.position[item]) == 0:
            del self.position[item]

        element = self.heap.pop()
        self.N -= 1
        # if we pop the item we wanted to delete (last-most item), we can end:
        if index == self.N:
            return

        # replace deleted item with the last-most item in heap, & bubble down:
        self.heap[index] = element
        self._bubble_down(index, element[0])

    def extract_min(self):
        """ Pops and returns the root (top priority) from heap.

        :returns:
            A list of item (key) and its associated priority (value).
            For example: ['Oranges', 17]
        :raises:
            ValueError: if heap is empty.
        """

        if self.N == 0:
            raise ValueError("heap is empty")

        element = self.heap[0]
        self.delete(element[0])
        return element

    def change_priority(self, item, priority_value):
        """ Updates the priority value of given item to new priority.

        Changes the priority of a given dict key to a new value
        while maintaining heap invariant.

        :args:
            item: the dictionary key
            priority_value: the new priority value to be set
        :raises
            IndexError: if multiple items of same key exist in heap.
        """

        if len(self.position[item]) > 1:
            raise IndexError("Multiple instances of key detected")

        index = self.position[item][-1]
        self.heap[index][-1] = priority_value

        self._bubble_up(self.position[item][0], item)
        self._bubble_down(self.position[item][0], item)

    def peek(self):
        """ Returns root (top priority) without popping it from the heap."""
        return self.heap[0]

    def select(self, key):
        """
            :args:
                key: dict key -- i.e. the item to be stored in heap.
            :returns:
                a list where the first element is the item lookup (key), and
                the second element is an array of one or more priority values.

            In order to maintain consistency, the method outputs the priority
            values of the item as an array even if only a single instance of
            item exists in heap.
        """

        if key not in self.position:
            raise KeyError("Item does not exist in the heap.")

        return [key, [self.heap[i][-1] for i in self.position[key]]]

    #################################
    #       Helper Functions 		#
    #################################

    def _bubble_up(self, i, item):
        """
            :args:
                i: index (i.e. priority) of item to bubble down
        """

        # n.b. `heap[i][-1]` = priority value
        while (i > 0) and self.heap[(i - 1) // 2][-1] > self.heap[i][-1]:
            # formula for finding parent (0-based index):
            p = (i - 1) // 2
            # swap values and indices:
            i = self._swap(i, p)
        self.position[item][-1] = i

    def _bubble_down(self, i, item):
        """
            :args:
                i: index (i.e. priority) of item to bubble down.
                c: child index.
        """

        # this conditional ensures that there is at least the left index:
        while 2 * i + 1 < self.N:
            c = 2 * i + 1  # formula for left child (0-based indexing)

            # (c+1 < N) ensures a right child; select the smallest to bubble down:
            # if right child is smaller, update c to be right (c+1):
            if (c + 1 < self.N) and self.heap[c + 1][-1] < self.heap[c][-1]:
                c += 1
            # check if heap property is fulfilled:
            if self.heap[i][-1] < self.heap[c][-1]:
                break
            # swap values and indices:
            i = self._swap(i, c)

        # recall `self.position[item][-1]` = index location (last/top of stack):
        self.position[item][-1] = i

    def _swap(self, i, j):
        """ Swaps heap items for both bubbling up/down; returns swapped index (j).
            Also updates child/parent hash to point to updated array position.

            :args:
                i: index of item to bubble
                j: index of parent/child
        """

        self.position[self.heap[j][0]][-1] = i
        self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
        return j

    def _heapify(self, arr):
        """ Returns a new heap from a given list in O(n) time.

            :args:
                arr: array -- can be array of numbers or a 2D array of
                     key-priority pairs -- e.g. [['dee', 234], ['yang', 8]]
        """
        self.heap = arr
        self.N = len(self.heap)

        # loop from last-most parent:
        # in 0-based index, last-most parent must be (length-2)//2
        for i in range((self.N - 2) // 2, -1, -1):
            self._heapify_loop(i)

        for i, item in enumerate(self.heap):
            self.position.setdefault(item[0], []).append(i)

        return self.heap

    def _heapify_loop(self, i):
        """ Starting from the penultimate level (height) of tree, we check if
            parent node is the smallest; if not, recurse (swap downward) until
            heap property is fulfilled

            :args:
                i: index of heap
        """
        # left, right, and smallest (min_) index in CURRENT iteration:
        l = (i * 2) + 1
        r = (i * 2) + 2
        min_ = i

        # convert numbers to [key, priority_value] array:
        for x in (l, r, i):
            if (x <= self.N - 1) and (type(self.heap[x]) == int or type(self.heap[x]) == float):
                self.heap[x] = [self.heap[x], self.heap[x]]

        if (l <= self.N - 1) and (self.heap[l][-1] < self.heap[i][-1]):
            min_ = l
        if (r <= self.N - 1) and (self.heap[r][-1] < self.heap[min_][-1]):
            min_ = r

        if min_ != i:
            self.heap[i], self.heap[min_] = self.heap[min_], self.heap[i]
            self._heapify_loop(min_)

    # TODO: implement the print function as described in docstring
    def print_heap(self):
        """ A visualization tool to print given heap in a pyramid shape.

            :future implementation:
                A simple printout function that represents the object in the
                more visually appropriate 'heap-like' shape -- i.e. a pyramid.
                For example:

                         470
                  1475          143
                94   1829   1306   12   738

                In order to calculate the correct padding/spacing for each item,
                the function iterates through the entire data structure, computing
                the total number of characters of the item (both the priority as
                well as the value associated with it). After the first pass, the
                priority-item pair with the most characters is determined. This max
                value is used to determine the spacing/padding evenly for each
                value-pair at each level of the heap. Aside: since `print_heap`
                requires two passes, the time complexity is technically O(2n).
            """

        if not self.heap:
            return
        height = int(math.log(len(self.heap), 2)) + 1

        iii = 0
        reps = 1
        for line in range(1, height + 1):
            # padding:
            print("  " * (height - line), end='')

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

if __name__ == '__main__':
    array = [['chang', 17], ['sheng', 5], ['alhazen', 8], ['dee', 10],
             ['guang', 14], ['jin', 15], ['dee', 8]]

    my_heap = MinIPQ(array)
    my_heap.print_heap()
