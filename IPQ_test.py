"""
Author: Dee Reddy
created: 3/19/2015
updated: 3/30/2015

Indexed priority queue (binary heap). Uses hash function for fast random look-ups.

DOES NOT SUPPORT multiple items with same priority value -- this is
because you are using hash[key] = array location.
Perhaps you can fix this?
Options:
0) use multi-dict
1) do nothing. create a check to see if key already exists
2) check if priority key already exists, if yes, then increment key by
.1 (this would effectively allow holding 10 items with same key)

supports:
-select key 				O(1)
-insert key 				O(log n)
-delete key 				O(log n)
-extract min 				O(log n)
-change key 				O(log n)
-select 					O(1)
-heapify (build heap) 	    O(n)
-print (unimplemented)      O(n + log n)

to do:
0) create print function that traverses down the tree to properly calculate correct spacing between each leaf
0) learn how to create a module, and how to import a class from a module/external file
0) see Coursera's programming tips on reducing code (you can use it to specify min/max heap with minimum extra lines)
0) add operation -- select item (i.e. find item by hash key)
0) add max heap (should we us negative keys?), and perhaps also use regular heap (w/o indexing) that doesn't use tuples
1) support for keys of same value
    1.5) support for inserting tuples/lists?
2) heapify should convert into tuples not single numbers. it doesn't support IPQ yet.
    2.5) make heapify use iterative loop rather than recursion
5) reword key, item, and element so that they're not confusing; i.e. the hash key is different from priority key. Perhaps just use the term 'priority' when refering to it.
6) perhaps tidy up the bubble up/down by explicitly using variable
7) use polymorphism so that we can use brackets (like in hashes) for our MinIPQ operations instead of method calls. E.g. pq["white devil"] = 666
8) add more heap operations: update/replace, merge.
9) create __rep__ and __print__ methods that displays the heap properly
"""
__author__ = ('Dee Reddy', 'd.reddy@yandex.com')


class MinIPQ():
    """Maps dict keys (keys) to priority keys (values), implemented as
    a list. Maintains an internal, heap data structure.
    """

    def __init__(self, default=None):
        """
        N: length of heap.
        heap: is array whose elements contain list of items and
        priority keys respectively.
        position is a hash whose keys are item and values are index
        positions in heap array.

        Examples:
        heap[4] >> ("Chanakya", 12)
        position["Chanakya"] >>> 4
        """
        if default is None:
            default = []

        self.heap = default
        self.position = {}
        self.N = 0

    def insert(self, item, key=None):
        """Inserts/pushes item, with priority, into heap. If no priority
            is given, the method tries to set the priority equal to the
            item (the item must then be numeric, otherwise raises error).

        Args:
            item: item to be stored as a dict key.
            key: item's priority key

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
        self._bubbleUp(self.N - 1, item)  # "N-1" because of 0-indexing

    def delete(self, item):
        """Deletes item from the heap.

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
        self._bubbleDown(index, element[0])

    def extractMin(self):
        """Pops and returns the root (top priority) from heap.

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
        """Returns root (top priority) without popping it from the heap."""
        return self.heap[0]

    def changeKey(self, item, key):  # maybe call this function "changePriority" instead
        """Updates the priority value of given item to new priority.

        Changes the priority of a given dict key to a new value
        while maintaining heap invariant.

        Args:
            item: the dictionary key
            key: the new priority key to be set
        """

        index = self.position[item]
        self.heap[index][-1] = key

        self._bubbleUp(self.position[item], item)
        self._bubbleDown(self.position[item], item)

        # need to convert elements into tuples to be consistant with other functions
        # we could make a seperate class for simple heap (rather than indexed heaps)

    # make sure you name 'heapify' appropriately: min/max, build/create heap? if it is part of MinIPQ -- then it should be min.
    def heapify(self, aArray):
        """Returns a new heap from a given list in O(n) time."""
        self.heap = aArray
        self.N = len(self.heap)

        for i in range((self.N - 2) // 2, -1, -1):  # in 0-based index, last-most parent must be (length-2)//2
            self._heapifyLoop(i)
        return self.heap

    #################################
    #       Helper Functions 		#
    #################################

    def _bubbleUp(self, i, item):
        """	@i 	 = index of item to bubble down"""

        while (i > 0) and self.heap[(i - 1) // 2][-1] > self.heap[i][-1]:  # might be more clean if we defined variable key = heap[i][-1]
            p = (i - 1) // 2  # formula for finding parent index (0-based index)
            i = self._swap(i, p)  # swap values and indices
        self.position[item] = i

    def _bubbleDown(self, i, item):
        """
        Args:
            i: index of item to bubble down.
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
            Also updates the child/parent hash to point to updated array position.
            @i = index of item to bubble
            @j = index of parent/child"""

        self.position[self.heap[j][0]] = i
        self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
        return j

    def _heapifyLoop(self, i):
        """ Starting from the penultimate level (height) of tree, we check if parent node
            is the smallest; if not, recurse (swap downward) until heap property is fulfilled"""

        l = (i * 2) + 1
        r = (i * 2) + 2
        min_ = i

        if (l <= self.N - 1) and (self.heap[l] < self.heap[i]): min_ = l
        if (r <= self.N - 1) and (self.heap[r] < self.heap[min_]): min_ = r

        if min_ != i:
            self.heap[i], self.heap[min_] = self.heap[min_], self.heap[i]
            self._heapifyLoop(min_)

#################################
#      Print Heap Function 		#
#################################

# why don't we just use padding format for strings? We can use padding after and padding before
import math


def printHeap(aList):
    if not aList: return
    height = int(math.log(len(aList), 2)) + 1

    iii = 0
    reps = 1
    for line in range(1, height + 1):
        print("  " * (height - line), end='')  # padding

        try:
            for _ in range(reps):
                print(aList[iii], end=' ')
                iii += 1
        except IndexError:
            pass
        print()
        reps *= 2

#####################################
#            test client            #
#####################################

# parameterize the class -- so that we can do this: "my_heap = MinIPQ([23,2563,7254,234]) >>> new heap"

if __name__ == '__main__':
    import random

    testArray = []
    for _ in range(20):
        randNumber = random.randrange(1, 2000)
        testArray.append(randNumber)

    my_heap = MinIPQ(testArray)
    my_heap = MinIPQ(testArray)

    print(my_heap.heap)
    printHeap(my_heap.heap)
    print(testArray)
