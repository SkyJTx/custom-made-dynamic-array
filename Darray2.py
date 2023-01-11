import ctypes as ct

class Darray:
    """ Welcome to Darray class. the Darray is a low-level array with many feature like a list. 
        You can do anything like you're using a list with extended features.
        All features:
            1) get the length of the Darray using len() method or .length method
            2) get element(s), set element(s), and delete an element(s)
            3) ability to reverse
            4) able to print a Darray
            5) concatenation
            6) remove through subtraction
            7) duplicate all element using multiplication
            8) equal and unequal checking
            9) able to check if the item is inside the Darray
            10) able to copy itself
            11) able to add an element to the last index
            12) able to insert an element by a given index
            13) able to remove an element
            14) able to delete an element by a given index
            15) able to extend the Darray by a given Darray
            16) able to count an element in the Darray
            17) able to find the index of an element
            18) able to reset the Darray
            19) able to pop an element out of the Darray
            20) able to push an element to the first element
            21) able to sort all the elements in the Darray
            22) able to reinitiate the Darray and set the given element(s) to the Darray
            22) able to iterate the Darray
        Next Feature:
            1) subset
            2) divide
            3) multiplication with the Darray (matrix multiplication)
    """

    def __init__(self,*args):
        """Create an empty array."""
        self._length = 0                                            # store numbers of elements
        self._cap = 1                                               # store array capacity
        self._array = self._make_array(self._cap)                   # create low-level array
        for i in args:                                              # append all element to low level array
            self.append(i)

    def __len__(self):                                              # return length of the Darray, Example: len(arr)
        """Return number of elements stored in the array."""
        return self._length
    
    @property
    def length(self):                                               # return length of the Darray , Example: arr.length
        """Return number of elements stored in the array."""
        return self._length

    def __getitem__(self, k):                                       # access element
        """Return element at index k."""
        if (type(k) is int):
            if not -self.length <= k < self.length:
                raise IndexError("Index out of range.")
            return self._array[k % self.length]                     # retrieve from array
        elif (type(k) is slice):                                    # slice Darray
            start, stop, step = k.start, k.stop, k.step             
            if (start == None): start = 0                           # (Default == None set to 0)
            if (stop == None): stop = self.length                   # (Default == None set to length)
            if (step == None): step = 1                             # (Default == None set to 1)
            temp = Darray()                                         # slicing by append to new Darray using for loop
            for i in range(start,stop,step): 
                temp.append(self[i])
            return temp
        else:                                               
            raise TypeError("Unsupported type.")                    # if the type is not what it is intended to

    def __setitem__(self, k, var):                  
        """Assign or reassign element at index k."""
        if (type(k) is int):
            if not -self.length <= k < self.length:
                raise IndexError("Index out of range.")
            self._array[k % self.length] = var                      # assign to array
        elif (type(k) is slice and type(var) in Darray(Darray,list,tuple,str)):
            start, stop, step = k.start, k.stop, k.step             
            if (start == None): start = 0                           # (Default == None set to 0)
            if (stop == None): stop = self.length                   # (Default == None set to length)
            if (step == None): step = 1                             # (Default == None set to 1)
            if (abs((stop-start)//step) != len(var)):
                raise ValueError("The value is invalid.")
            index = 0
            for i in range(start,stop,step):
                self[i] = var[index]
                index += 1
        else:
            raise TypeError("Unsupported type.")                    # if the type is not what it is intended to
            
    def __delitem__(self, k):
        """delete element of the Darray by given index or given slice."""
        if (type(k) is int):
            if not -self.length <= k < self.length:
                raise IndexError("Index out of range.")
            self.delete(k)                                          # remove
        elif (type(k) is slice):                                    # slice Darray
            start, stop, step = k.start, k.stop, k.step             
            if (start == None): start = 0                           # (Default == None set to 0)
            if (stop == None): stop = self.length                   # (Default == None set to length)
            if (step == None): step = 1                             # (Default == None set to 1)
            none_index = Darray()                                   # to store deleted element's index
            for i in range(start,stop,step):
                self[i] = None
                none_index.append(i % self.length)
            none_index.sort()                                       # sort it before begin decreasing the element
            # above is verified
            for index in range(none_index.length):
                for j in range(none_index[index]-index,self.length-1):
                    self[j], self[j+1] = self[j+1], self[j]
                self._length -= 1
            while (self._length < self._cap // 4):                  # shrink capacity if necessary
                self._resize(self._cap // 2)
        else:                                               
            raise TypeError("Unsupported type.")                    # if the type is not what it is intended to
            
    def __reversed__(self):
        """reversed(Darray) method return its reversed without changing the original Darray"""
        temp = self.copy()
        temp.reverse()
        return temp
    
    def __str__(self):
        """Console output Darray when its called by print function."""                                      
        prompt = "<"                                                    # start
        for k in range(self._length):   
            if (k < self._length-1):
                if (type(self._array[k]) is str):
                    prompt += "\"" + str(self._array[k]) + "\"" + ", "  # add "string" if the element is string
                else:
                    prompt += str(self._array[k]) + ", "                # else concat the element and ,
            else:                                                       # if it is the last element
                if (type(self._array[k]) is str):
                    prompt += "\"" + str(self._array[k]) + "\""         # add "string" if the element is string
                else:
                    prompt += str(self._array[k])                       # else concat the element and
        return prompt + ">"                                             # close
    
    def __repr__(self):
        """Console output of the class."""
        return self.__str__()

    def __add__(self, *darray_obj):
        """Concatenation."""
        temp = self.copy()                                          # copy
        for i in darray_obj:
            temp.extend(i)                                          # add by append
        return temp
    
    def __sub__(self, *obj):
        """Remove given elements in the Darray. Example: <5,4,3,5> - <5> output <4,3,5>"""
        temp = self.copy()                                          # copy
        for i in obj:
            if (type(i) is Darray):
                for j in range(i.length):
                    temp.remove(i[j],ignore_value_error=True)       # remove each element based on given Darray
            else:
                raise TypeError("Only Darray type is accepted.")
        return temp
    
    def __mul__(self, size_mul):
        """Extend and repeat itself with given integer."""
        if (type(size_mul) is int):
            temp = self.copy()                                      # copy
            for _ in range(size_mul-1):
                temp = temp + self                                  # concat for given multiplier
            return temp
        else:
            raise TypeError("Only Darray and int type is accepted")
    
    def __eq__(self, *darray_obj):
        """Checking if the given Darrays is the same."""
        for i in darray_obj:
            if (type(i) is Darray):
                if (self.length != i.length):                       # return False if it doesn't have the same size
                    return False
                for j in range(self.length):                        # check if all elements is the same
                    if (self[j] != i[j]):
                        return False
            else:
                return False
        return True
    
    def __ne__(self, *darray_obj):
        """Checking if the given Darrays is not the same."""
        return not self.__eq__(*darray_obj)
    
    def __contains__(self, obj):
        """Checking if the given object is indeed in the Darray."""
        for i in range(self.length):
            if (self._array[i] == obj):
                return True
        return False

    def __iter__(self):
        """return a generator of the Darray"""
        if (self._cap != self._length):
            self._resize(self.length)
        yield from self._array
        
    def __bytes__(self):
        return b'123456789'
    
    def copy(self):
        """Copy the Darray and return its identical."""                                       
        temp = Darray()                                                 # create Darray named "copy"
        for i in range(self._length):                                   # loop for all element                       
            if (type(self[i]) in Darray(list,tuple,set,dict,Darray)):   # append a copy of a element if the element is mutable
                temp.append(self[i].copy())
            else:                                                       # append a copy of a element if the element is immutable
                temp.append(self[i])                    
        return temp
    
    def append(self, obj):
        """Add object to end of the array."""
        if (self._length == self._cap):                             # not enough room
            self._resize(2 * self._cap)                             # so double capacity
        self._array[self._length] = obj
        self._length += 1

    def _resize(self, c):                                           # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)                                     # new (bigger) array
        for k in range(self._length):                               # for each existing value
            B[k] = self._array[k]
        self._array = B                                             # use the bigger array
        self._cap = c

    def _make_array(self, c):                                       # nonpublic utitity
        """Return new array with capacity c."""   
        return (c * ct.py_object)()                                 # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        if not -self.length <= k < self.length:
            raise IndexError("Index out of range.")
        k = k % self.length
        if self.length == self._cap:                                # not enough room
            self._resize(2 * self._cap)                             # so double capacity
        for j in range(self._length, k, -1):                        # shift rightmost first
            self[j] = self[j-1]
        self[k] = value                                             # store newest element
        self._length += 1
    
    def remove(self, value, ignore_value_error=False):
        """Remove first occurrence of value (or raise ValueError)."""
        for k in range(self._length):
            if self[k] == value:                                    # found a match!
                for j in range(k, self._length - 1):                # shift others to fill gap
                    self[j] = self[j+1]
                self[self._length - 1] = None                       # help garbage collection
                self._length -= 1                                   # we have one less item
                if self._length == self._cap // 4:                  # shrink capacity if necessary
                    self._resize(self._cap // 2)
                return                                              # exit immediately
            if (not ignore_value_error):
                raise ValueError('Value not found.')                # only reached if no match
    
    def extend(self, obj):
        """Extend the Darray by append."""
        if (type(obj) in Darray(Darray,list,tuple,str)):
            for i in obj:
                self.append(i)
        else:
            raise TypeError("Only Darray, list, tuple and str types are accepted.")
    
    def count(self, obj):
        """Count the object in a Darray."""
        num = 0
        for i in self:
            if (i == obj):
                num += 1
        return num
    
    def index(self, obj):
        """Find index of the object."""
        index_darray = Darray()
        for i in range(self.length):
            if (self[i] == obj):
                index_darray.append(i)
        return index_darray
    
    def clear(self):
        """Reset by reinitiate constructor."""
        self.__init__()
    
    def pop(self, index=None):
        """Remove and return element at index (default last)."""
        if index is None:
            index = self._length - 1
        if not -self.length <= index < self.length:
            raise IndexError("Index out of range.")
        index = index % self._length
        value = self[index]
        for i in range(index, self._length - 1):                    # shift elements to fill the gap
            self[i] = self[i + 1]
        self._length -= 1
        if self._length == self._cap // 4:                          # shrink capacity if necessary
            self._resize(self._cap // 2)
        return value
    
    def push(self, obj):
        if self.length == self._cap:                                # not enough room
            self._resize(2 * self._cap)                             # so double capacity
        for j in range(self._length, -1, -1):                       # shift rightmost first
            self[j] = self[j-1]
        self[0] = obj                                               # store newest element
        self._length += 1
    
    def delete(self, index):
        if index is None:
            index = self._length - 1
        if not -self.length <= index < self.length:
            raise IndexError("Index out of range.")
        index = index % self._length
        for i in range(index, self._length - 1):                    # shift elements to fill the gap
            self[i] = self[i + 1]
        self._length -= 1
        if self._length == self._cap // 4:                          # shrink capacity if necessary
            self._resize(self._cap // 2)

    def redef(self, *args):
        """Reinitiate constructor and assign totally new elements."""
        self.__init__(*args)

    def sort(self,reverse=False):
        """Sort the elements of the array in ascending order using quicksort."""
        def _quicksort(A, low, high):
            if low < high:
                pivot = partition(A, low, high)                 # pivot index from low = 0 to high = length
                _quicksort(A, low, pivot - 1)                   # quicksort the left of the pivot
                _quicksort(A, pivot + 1, high)                  # quicksort the right of the pivot

        def partition(A, low, high):
            pivot = A[high]                                     # let pivot to be the rightmost element
            i = low - 1                                         # let i to be the lowest index that we start to sort. usually the leftmost element
            for j in range(low, high):
                if A[j] < pivot:
                    i += 1                                      # i is incresed by i. it eventually reach the index before the pivot
                    A[i], A[j] = A[j], A[i]                     # swap the element that is lower than the pivot with the he element that is higher than the pivot
            A[i + 1], A[high] = A[high], A[i + 1]               # swap the element that is before the pivot with the pivot
            return i + 1                                        # return i + 1 (pivot index)

        _quicksort(self._array, 0, len(self) - 1)
        if (reverse):                                           # will reverse after sorting if the user wanted to
            self.reverse()
    
    def reverse(self):
        """Reverse the element."""
        for i in range(self.length//2):
            self[i], self[self.length-i-1] = self[self.length-i-1], self[i]