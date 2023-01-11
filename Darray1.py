import ctypes as ct

class Darray:
    """Welcome to Darray class. the Darray is a low-level array with many feature like a list. 
        What can you do? :
            1. You can do anything like you're using a list.
            2. Extended feature such as
                1) Subtract a Darray with a Darray.
                2) __delitem__ is now extended to accept a negative index.
    """

    def __init__(self,*args):
        """Create an empty array."""
        self._n = 0                                                 # count actual elements
        self._capacity = 1                                          # default array capacity
        self._A = self._make_array(self._capacity)                  # low-level array
        for i in args:                                              # append all element to low level array
            self.append(i)

    def __len__(self):                                              # return length of the Darray, Example: len(arr)
        """Return number of elements stored in the array."""
        return self._n
    
    @property
    def length(self):                                               # return length of the Darray , Example: arr.length
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):                                       # access element
        """Return element at index k."""
        if (type(k) is int):
            if not -self._n <= k < self._n:
                raise IndexError("Index out of range.")
            if (k < 0):                                             # support index less than 0
                return self._A[self._n + k]                         # retrieve from array (k < 0)
            return self._A[k]                                       # retrieve from array
        elif (type(k) is slice):                                    # slice Darray
            start = k.start                                         # from start index (Default == None set to 0)
            stop = k.stop                                           # to end index (Default == None set to length)
            step = k.step                                           # with step of (Default == None set to 1)
            if (start == None):                             
                start = 0
            if (stop == None):
                stop = self.length
            if (step == None):
                step = 1
            if (step < 0):                                          # if step is negative, inverse start and stop
                start = -start-1
                stop = -stop-1
            temp = Darray()                                         # slicing by append to new Darray using for loop
            for i in range(start,stop,step):
                temp.append(self[i])
            return temp
        else:                                               
            raise TypeError("Unsupported type.")                    # if the type is not what it is intended to

    def __setitem__(self, k, var):                  
        """Assign or reassign element at index k."""
        if (type(k) is int):
            if not -self._n <= k < self._n:
                raise IndexError('Index out of range.')
            if (k < 0):                                             # support index less than 0
                self._A[self._n + k] = var                          # assign to array (k < 0)
            else:
                self._A[k] = var                                    # assign to array
        elif (type(k) is slice and type(var) in Darray(Darray,list,tuple)):
            start = k.start                                         # from start index (Default == None set to 0)
            stop = k.stop                                           # to end index (Default == None set to length)
            step = k.step                                           # with step of (Default == None set to 1)
            if (start == None):                             
                start = 0
            if (stop == None):
                stop = self.length
            if (step == None):
                step = 1
            if (step < 0):                                          # if step is negative, inverse start and stop
                start = -start-1
                stop = -stop-1
            if (abs((stop-start)//step) != len(var)):
                raise ValueError("The value is invalid.")
            index = 0
            for i in range(start,stop,step):
                self[i] = var[index]
                index += 1
            
    def __delitem__(self, k):
        """delete element of the Darray by given index or given slice."""
        if (type(k) is int):
            if not -self._n <= k < self._n:
                raise IndexError('Index out of range.')
            if (k < 0):                                             # support index less than 0
                self.pop(self.length+k)                             # remove for k < 0
            else:
                self.pop(k)                                         # remove
        elif (type(k) is slice):                                    # slice Darray
            start = k.start                                         # from start index (Default == None set to 0)
            stop = k.stop                                           # to end index (Default == None set to length)
            step = k.step                                           # with step of (Default == None set to 1)
            if (start == None):                             
                start = 0
            if (stop == None):
                stop = self.length
            if (step == None):
                step = 1
            if (step < 0):                                          # if step is negative, inverse start and stop
                start = -start-1
                stop = -stop-1
            none_index = Darray()                                   # to store deleted element's index
            for i in range(start,stop,step):
                self[i] = None
                if (i < 0):
                    none_index.append(self.length+i)
                else:
                    none_index.append(i)
            none_index.sort()                                       # sort it before begin decreasing the element
            # above is verified
            for i in range(none_index.length):
                for j in range(none_index[i]-i,self.length-1):
                    self[j], self[j+1] = self[j+1], self[j]
                self._n -= 1
            while (self._n <= self._capacity // 4):                 # shrink capacity if necessary
                self._resize(self._capacity // 2)
        else:                                               
            raise TypeError("Unsupported type.")                    # if the type is not what it is intended to
            
    def __reversed__(self):
        """reversed(Darray) method return its reversed without changing the original Darray"""
        temp = self.copy()
        temp.reverse()
        return temp
    
    def __str__(self):
        """Console output Darray when its called by print function."""                                      
        prompt = "<"                                                # start
        for k in range(self._n):   
            if (k < self._n-1):
                if (type(self._A[k]) is str):
                    prompt += "\"" + str(self._A[k]) + "\"" + ", "  # add "string" if the element is string
                else:
                    prompt += str(self._A[k]) + ", "                # else concat the element and ,
            else:                                                   # if it is the last element
                if (type(self._A[k]) is str):
                    prompt += "\"" + str(self._A[k]) + "\""         # add "string" if the element is string
                else:
                    prompt += str(self._A[k])                       # else concat the element and
        return prompt + ">"                                         # close
    
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
        return not self.__ne__(*darray_obj)
    
    def __contains__(self, obj):
        """Checking if the given object is indeed in the Darray."""
        for i in range(self.length):
            if (self[i] == obj):
                return True
        return False
    
    def copy(self):
        """Copy the Darray and return its identical."""                                       
        temp = Darray()                                             # create Darray named "copy"
        for i in range(self._n):                                    # loop for all element                       
            if (type(self[i]) in Darray(list,tuple,set,dict,Darray)): # append a copy of a element if the element is mutable
                temp.append(self[i].copy())
            else:                                                   # append a copy of a element if the element is immutable
                temp.append(self[i])                    
        return temp
    
    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity:                               # not enough room
            self._resize(2 * self._capacity)                        # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):                                           # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)                                     # new (bigger) array
        for k in range(self._n):                                    # for each existing value
            B[k] = self._A[k]
        self._A = B                                                 # use the bigger array
        self._capacity = c

    def _make_array(self, c):                                       # nonpublic utitity
        """Return new array with capacity c."""   
        return (c * ct.py_object)()                                 # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        if (0 <= k <= self._n):
            if self._n == self._capacity:                           # not enough room
                self._resize(2 * self._capacity)                    # so double capacity
            for j in range(self._n, k, -1):                         # shift rightmost first
                self[j] = self[j-1]
            self[k] = value                                         # store newest element
            self._n += 1
        else:
            raise IndexError("Index out of range.")
    
    def remove(self, value, ignore_value_error=False):
        """Remove first occurrence of value (or raise ValueError)."""
        for k in range(self._n):
            if self[k] == value:                                    # found a match!
                for j in range(k, self._n - 1):                     # shift others to fill gap
                    self[j] = self[j+1]
                self[self._n - 1] = None                            # help garbage collection
                self._n -= 1                                        # we have one less item
                if self._n == self._capacity // 4:                  # shrink capacity if necessary
                    self._resize(self._capacity // 2)
                return                                              # exit immediately
            if (not ignore_value_error):
                raise ValueError('Value not found.')                # only reached if no match
    
    def extend(self, darray_obj):
        """Extend the Darray by append."""
        if (type(darray_obj) is Darray):
            for i in range(darray_obj._n):
                self.append(darray_obj[i])
        else:
            raise TypeError("Only Darray type is accepted.")
    
    def count(self, obj):
        """Count the object in a Darray."""
        num = 0
        for i in range(self._n):
            if (self[i] == obj):
                num += 1
        return num
    
    def index(self, obj):
        """Find index of the object."""
        index_darray = Darray()
        for i in range(self._n):
            if (self[i] == obj):
                index_darray.append(i)
        return index_darray
    
    def clear(self):
        """Reset by reinitiate constructor."""
        self.__init__()
      
    def pop(self, index=None):
        """Remove and return element at index (default last)."""
        if index is None:
            index = self._n - 1
        if not -self._n <= index < self._n:
            raise IndexError('Index out of range.')
        value = self[index]
        for i in range(index, self._n - 1):                     # shift elements to fill the gap
            self[i] = self[i + 1]
        self._n -= 1
        if self._n == self._capacity // 4:                      # shrink capacity if necessary
            self._resize(self._capacity // 2)
        return value

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

        _quicksort(self._A, 0, len(self) - 1)
        if (reverse):                                           # will reverse after sorting if the user wanted to
            self.reverse()
        
    def reverse(self):
        """Reverse the element."""
        for i in range(self.length//2):
            self[i], self[self.length-i-1] = self[self.length-i-1], self[i]