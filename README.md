## ipq_multidict
----------------------------

###### [Indexed priority queue (binary heap)](http://algs4.cs.princeton.edu/24pq/). Uses hash function for fast, random look-ups. Supports non-unique keys.

#### Supports:
- select key.................._O(1)_
- insert key.................._O(log n)_
- delete key.................._O(log n)_
- extract min................._O(log n)_
- change priority............._O(log n)_
- peek (select top element)..._O(1)_
- heapify (transform list)...._O(n)_

#### Usage:
1) Create a new (empty) heap instance:
```
my_heap = MinIPQ()
```
2) Insert a key-priority value pair via `insert()` method -- the heap
invariance will automatically be maintained:
```
my_heap.insert('dee', 12)
```
3) We can delete item from heap by its key:
```
my_heap.delete('genghis')
```
4) We can extract lowest priority item from heap, returning the key-priority
value pair:
```
my_heap.extract_min()
```
5) We can change priority value of a key (NOTE: will raise error if multiple
instances of given key are detected):
```
my_heap.change_priority('dee', 7)
```
6) We can return the top element (most priority) of heap without extracting it:
```
my_heap.peek()
```
7) Finally, we can build a heap from an existing array in linear time:
```
some_data_set = MinIPQ(some_list)
```

#### Limitations:
- Items inserted into heap must not be mutable objects (e.g. arrays,
dicts, etc.).
- Changing priorities is unsupported if multiple non-unique keys exist in heap.

#### Additional Info:
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
```
my_heap = [['shiva', 35], ['lakshmi', 164], ['dee', 684], ['vlad', 285], ['dee', 275], ['dee', 824], ['shiva', 1132]]
```

The internal dict mapping (called `position`) follows this format:
_{ item: [index_in_heap [, index_in_heap] }_
So for example:
```
{'vlad': [3], 'shiva': [0, 6], 'lakshmi': [1], 'dee': [5, 2, 4]}
```

If we wanted to delete key, say, 'dee' from our heap, we would do this:
`my_heap.delete('dee')`
The delete() method will lookup the key 'dee' in the internal hash; it will
find the key and see that its associated value -- an array -- it will pop the
last element in this array. If, after popping, the array is empty, the hash key
will be deleted as well. The popped value is the position (index) in the heap
-- which is also happens to be an array. Using this index, the function will
pop the object -- `['dee', 275]` -- from the heap array, then go on to maintain
the heap invariance as expected.

#### TODO:
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

#### License:
Released under the Apache License. Copyright (c) 2015 Dee Reddy.