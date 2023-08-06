"""
How to use: create a DataCube with a n-d array of floats, and n lists of strings representing the 
values each axis refers to. Access values as arrays by name from the float list. Recursively applies in 
any number of dimensions at once.

Example script:

import numpy as np
from research_personal.data_cube import DataCube

xs = ['a','b']              #string identifiers
ys = ['y1.0','y2.0','y3.0'] #numerical data is supported, but only in 
                            #the form of strings (so prepending variable
                            #to number is recommended)
zs = np.array([[0,1,2],[3,4,5]]) #some data
dc = DataCube(zs,[xs,ys])
dc['a'].data                #gets all elements in first array
>>>array([0, 1, 2])

dc['y1.0'].data             #gets first element along each array
>>>array([0, 3])

dc['b','y1.0']              #if all axes are specified, returns a number 
                            #instead of a DataCube, so ".data" not needed
>>>3

dc['b','y1.0-y2.0'].data    #can pass in a range as well, will reduce data to that range
>>>array([3, 4])

dc2 = DataCube(zs,[xs,ys])
new_cube = 5*dc-dc2/(zs+1)  #simple math can be performed with DataCubes
new_cube['a'].data          #returns a DataCube with the same axes/names
>>>array([0.        , 4.5       , 9.33333333])
"""

import numpy as np

class InvalidDataError(Exception):    
    def __init__(self, message):
        self.message = message

class InvalidMathError(Exception):    
    def __init__(self, message):
        self.message = message

class DataCube:
    def __init__(self,data,string_lists):
        if isinstance(data,np.ndarray):
            self.data = data
        elif isinstance(data,list):
            data = np.array(data)
            self.data = data
        else:
            raise InvalidDataError('Array-shaped data is required.')
        self.d = self.data
        self.string_lists = string_lists
        #check the number of string lists is equal to the number of axes
        if len(string_lists) != len(data.shape):
            raise InvalidDataError('len(string_lists) must equal len(data.shape),'+\
                    'yours were %d and %d. Lists:%s and %s'%(len(string_lists),len(data.shape),string_lists,data.shape))
        used_labels = []
        #check each string list has the correct number of items, and no label is reused or contains "-" 
        #(which is used for .__getitem__ so cannot be in the name)
        for i,l in enumerate(string_lists):
            if len(l) != data.shape[i]:
                raise InvalidDataError('column %d has length %d, but %d labels were given. (labels:%s)'%(i,data.shape[i],len(l),l))
            for string in l:
                if '-' in string:
                    raise InvalidDataError('Not allowed to use variable names containing "-". [violator: %s]'%string)
                if string in used_labels:
                    raise InvalidDataError('Not allowed to reuse variable names. [violator: %s]'%string)
                used_labels.append(string)
        #each list is internally referred to by its first element 
        #(unique because names cannot be reused anyways)
        self.string_list_names = [l[0] for l in string_lists]
        #the list's original axes info is saved, so each first element refers to the
        #axis of its list
        self.string_list_numbers = {}
        for i,name in enumerate(self.string_list_names):
            self.string_list_numbers[name] = i
        self.shape = self.data.shape
        
    def __getitem__(self,*args):
        to_return = self.data
        #if lists are used but not fully removed (i.e. you ask for a range), it can
        #modify what counts as the "first element" of its list, and thus these references
        #need to change. Copying that info here to modify later without changing the original 
        #DataCube
        current_string_lists = list(self.string_lists)
        current_string_list_names = list(self.string_list_names)
        current_string_list_numbers = dict(self.string_list_numbers)
        #we will track which lists have already been used (by their first elements)
        #"used" is lists which are fully removed (selected), "modified" means 
        #a range was applied to an axis, but the returned DataCube will still have that axis
        used,modified = [],[]
        #can call this with a tuple or just several string arguments
        if len(args) == 1 and isinstance(args[0],tuple):
            args = args[0]
        for k in args:
            if not isinstance(k,str):
                raise IndexError("arguments '%s' cannot be understood. Call with either "%(args,)+\
                            "strings or tuple of strings")
        for arg in args:
            #only reference each axis once per item call, "not_used" are the axes to continue checking
            not_used = list(set(current_string_list_names)-set(used))
            str_list_indices_to_use = sorted([current_string_list_numbers[k] for k in not_used])
            str_lists_to_use = [current_string_lists[k] for k in str_list_indices_to_use]
            #we are looking for a range, not a full axis call
            if '-' in arg:
                element0,element1 = None,None
                low,high = arg.split('-')
                for i,l in enumerate(str_lists_to_use):
                    #will just search for "low" and check that high is there with it
                    #check each axis until it finds correct one, then break.
                    if low in l:
                        if l in modified+used:
                            raise InvalidDataError('cannot use the same axis multiple times within '+\
                                            'a single call! axis:%s'%arg)
                        element0 = l.index(low)
                        element1 = l.index(high)+1
                        #range must be in same order as original string_list along that axis
                        if element1<=element0:
                            raise IndexError('%s is not a valid continuum arg, elements are not in order'%arg)
                        modified.append(low)
                        #this modification changes the string_lists, and possibly changes the first element. 
                        #Therefore it needs to fix that information
                        current_string_lists[current_string_list_numbers[l[0]]] = l[element0:element1]
                        #switch out reference name (if l[0] = low, this does nothing)
                        current_string_list_names[current_string_list_numbers[l[0]]] = low
                        #keep axis the same
                        current_string_list_numbers[low] = i
                        #clean up the dictionary (for debugging purposes, though 
                        #current_string_list_numbers[l[0]] should never be used)
                        if low != l[0]:
                            current_string_list_numbers.pop(l[0])
                        break
                #for loop completed without breaking, the requested element was not in any list
                if element0 is None:
                    raise IndexError('arg %s not in any list of remaining elements: %s'%(arg,str_lists_to_use))
                #we will access the numpy array by constructing a string with the right number
                #of colons and commas (determined by the axis "i" at time of break), and the 
                #right elements of the range ("element0","element1")
                element_access_str = ':,'*i+'%d:%d,'%(element0,element1)+':,'*(len(str_lists_to_use)-i-1)
            #we are looking for a full axis call, not a range
            else:
                element = None
                #check each axis until it finds correct one, then break.
                for i,l in enumerate(str_lists_to_use):
                    if arg in l:
                        if l in modified+used:
                            raise InvalidDataError('cannot use the same axis multiple times within '+\
                                            'a single call! axis:%s'%arg)
                        element = l.index(arg)
                        used.append(l[0])
                        break
                #for loop completed without breaking, the requested element was not in any list
                if element is None:
                    raise IndexError('arg %s not in any list of remaining elements: %s'%(arg,str_lists_to_use))
                #we will access the numpy array by constructing a string with the right number
                #of colons and commas (determined by the axis "i" at time of break), and the 
                #right element of the selected axis ("element")
                element_access_str = ':,'*i+'%d,'%element+':,'*(len(str_lists_to_use)-i-1)
            #[:-1] is because "element_access_str" will always have an excess comma at end
            #this shrinks the array by one axis, or narrows one axis and retains shape
            #since "str_lists_to_use" is kept in order, this will work again in each run
            #of the for loop
            to_return = eval('to_return[%s]'%element_access_str[:-1])
        #one last clean-up of the current string lists still not accessed,
        #will create a new DataCube with these as arguments
        not_used = list(set(current_string_list_names)-set(used))
        str_list_indices_to_use = sorted([current_string_list_numbers[k] for k in not_used])
        str_lists_to_use = [current_string_lists[k] for k in str_list_indices_to_use]
        #there is no 0-D DataCube, just return the value.
        if len(to_return.shape) == 0:
            return to_return
        return DataCube(to_return,str_lists_to_use)

    def __repr__(self):
        #more useful to show the axes names than the underlying data, I think
        list_reprs = []
        for string_list in self.string_lists:
            r = '['
            #long lists show like "[0, 1, 2, ..., n]"
            if len(string_list)>8:
                for i,l in enumerate(string_list):
                    if i<3:
                        r+="'%s', "%l
                    elif i==3:
                        r+="'%s', ..., "%l
                    #skip item 3 < i < last item
                    elif i==len(string_list)-1:
                        r+="'%s'"%l
            #short lists show like "[0, 1, 2, 3]"
            else:
                r += str(string_list).strip('[]')
            list_reprs.append(r+']')
        return "<%d-D DataCube with categories %s>"%(len(self.string_lists),str(list_reprs).replace('"',''))
    
    def print_lists(self):
        #like "__repr__", but showing all axes/names, not just a managably small number
        print("%d-D DataCube:"%len(self.string_lists))
        for string_list in self.string_lists:
            print(string_list)

    #DataCubes can do basic math with each other, with same-shaped arrays, or with scalars. 
    #Will throw InvalidMathError if the shapes are wrong, or the other has different string_lists 
    def check_string_lists_equal(self,other):
        if isinstance(other,DataCube):
            for i,sl in enumerate(self.string_lists):
                if len(sl)!=len(other.string_lists[i]):
                        raise InvalidMathError("The two DataCubes '%s' and '%s'"%(self,other)+\
                                        " did not have the same string_lists, and cannot be combined.")
                for j,s in enumerate(sl):
                    if other.string_lists[i][j] != s:
                        raise InvalidMathError("The two DataCubes '%s' and '%s'"%(self,other)+\
                                        " did not have the same string_lists, and cannot be combined.")
        elif isinstance(other,np.ndarray):
            for i,sl in enumerate(self.string_lists):
                if other.shape[i] != len(sl):
                    raise InvalidMathError("The DataCube '%s' did not have"%(self)+\
                                        " the same shape as the array '"+repr(other)+\
                                          "', and cannot be combined.")
        elif isinstance(other,(int,float)):
            pass
        else:
            raise InvalidMathError("Cannot perform math on items except DataCubes, numpy arrays, or real numbers.")
    def __add__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data+other.data
        else:
            ret_array = self.data+other
        return DataCube(ret_array,self.string_lists)
    def __radd__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data+other.data
        else:
            ret_array = self.data+other
        return DataCube(ret_array,self.string_lists)
    def __sub__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data-other.data
        else:
            ret_array = self.data-other
        return DataCube(ret_array,self.string_lists)
    def __rsub__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = other.data-self.data
        else:
            ret_array = other-self.data
        return DataCube(ret_array,self.string_lists)
    def __truediv__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data/other.data
        else:
            ret_array = self.data/other
        return DataCube(ret_array,self.string_lists)
    def __rtruediv__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = other.data/self.data
        else:
            ret_array = other/self.data
        return DataCube(ret_array,self.string_lists)
    def __mul__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data*other.data
        else:
            ret_array = self.data*other
        return DataCube(ret_array,self.string_lists)
    def __rmul__(self,other):
        self.check_string_lists_equal(other)
        if isinstance(other,DataCube):
            ret_array = self.data*other.data
        else:
            ret_array = self.data*other
        return DataCube(ret_array,self.string_lists)
    def __neg__(self):
        return DataCube(-self.data,self.string_lists)
