"""qrem.common.utils module contains all helpful functions used throughout the projcets.

Current contents of this module will relate to:
- dit/bitstring conversions
- python/numpy format conversions
- boolean operators on lists (that treat lists as sets)
- other helpful functions not covered elswhere

May be split into other modules in the future (very likely)

"""
from typing import List

#===================================================
# Constants
#===================================================
#Why 9 is the number as of now? 
SIGNIFICANT_DIGITS = 9




#===================================================
# Boolean operation on lists treated as sets
#===================================================

def lists_intersection(lst1: list,
                       lst2: list):
    """Intersection of 2 lists lst1 and lst2 after conversion of both to sets.
    
    Returns
    -------
    list

    Notes
    -----
    Multiple entries within each of the lists will merge 
    """
    return list(set(lst1) & set(lst2))

def lists_difference(lst1: list,
                     lst2: list):
    """Difference between 2 lists lst1 and lst2 after conversion of both to sets.
    
    Returns
    -------
    list
    
    Notes
    -----
    Multiple entries within each of the lists will merge 
    """
    return list(set(lst1) - set(lst2))

def lists_sum(lst1: list,
              lst2: list):
    """Union between 2 lists lst1 and lst2 after conversion of both to sets. 

    Returns
    -------
    list
    
    Notes
    -----
    Multiple entries within each of the lists will merge 
    """
    return list(set(lst1).union(set(lst2)))

def lists_sum_multiple(lists: List[list]):
    """Union between all lists in the input  list of lists (lists) after conversion to sets. 
    
    Returns
    -------
    list

    Notes
    -----
    Multiple entries within each of the lists will merge 
    """
    return list(set().union(*lists))

def lists_intersection_multiple(lists: List[list]):
    """Intersection of all lists in the input  list of lists (lists) after conversion  to sets. Returns a list.

    Notes
    -----
    Multiple entries within each of the lists will merge 
    """
    l0 = lists[0]
    l1 = lists[1]

    int_list = lists_intersection(l0, l1)
    for l in lists[2:]:
        int_list = lists_intersection(int_list, l)
    return int_list

#TEST_ME test and improve efficiency of the check
def check_for_multiple_occurences(lists: List[list]) -> bool:    
    """Checks for duplicate elements between multiple lists. Multiple occurences within each of lists are not taken into consideration

    Returns
    -------
    bool
    """
    # possible reimplementation, not sure if faster / slower
    # u = reduce(set.union, map(set, ll))
    # sd = reduce(set.symmetric_difference, map(set, lists))
    # len(u - sd) != 0 ->there are repeating elements
    for i in range(len(lists)):
        for j in range(i + 1, len(lists)):
            if len(lists_intersection(lists[i], lists[j])) != 0:
                return True

    return False



# import numpy as np
# import orjson
# from pathlib import Path
# class ExampleDataClass:
#     def __init__(self, name):

#         #[X] default value definitions
#         self.name = name                # name of the Data set
#         dt = np.dtype(np.uint8)         # type definition - helper def for below
#         self.circuits = np.array([],dt) # some data type (for circuits it should be probably list of np.arrays or array of arrays)
#         self.id = -1                    # unique id, set manually during export (field not used currently)
#         self.experiment_type = "DDOT"   # type of experiment - can be coded as string, or as sth else
#         pass

#     def getDictFormat(self):
#         '''returns this class as a json-like dictionary structure'''
#         return self.__dict__

#     def getJSON(self):
#         return  orjson.dumps(self, default=lambda o: o.__dict__,
#         option=orjson.OPT_SERIALIZE_NUMPY, sort_keys=True)
    
#     def exportJSON(self,json_export_path,overwrite = True):
        
#         #[7] Save into json file
#         if(Path(json_export_path).is_file() and not overwrite):
#             print(f"WARNING:: Ommiting export to existing file: <{json_export_path}>")     
#         else:
#             with open(json_export_path, 'w') as outfile:
#                 outfile.write(self.getJSON())

#     def importJSON(self,json_import_path):
#         '''import JSON'''
#         #stub, easy to implement
#         #first orjson.load contents of the file
#         #then assign elements of loaded dict into the class fields
#         pass
