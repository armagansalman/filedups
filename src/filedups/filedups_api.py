"""
    MIT License

Copyright (c) 2023 Armağan Salman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

#( System modules
#)

#( Project modules
from common_types import *
import constants as CONST
from classes import DuplicateFinder, GroupFunc
import util as UT
import grouper_funs as GRPR
#)

def find_duplicates(file_paths: Set[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
#(
    """ Given file paths, returns duplicate scan result as a dict.
        
        Groups by size first. Then groups by sha512 hash of first 2KB 
        of every file.
    """
    
    fls_unfiltered: Set[str] = set(file_paths)
    
    SMALLEST_SIZE: int = MIN_SIZE_LIMIT
    
    filtered_locations: Set[str] = set(UT.filter_by_size(fls_unfiltered, \
                            MIN_SIZE_LIMIT, MAX_SIZE_LIMIT))
    #
    
    FINDER: DuplicateFinder = DuplicateFinder(filtered_locations)
    all_indices: List[int] = FINDER.get_all_file_indices()
        
    #hash_sizes = [64 * CONST.xBYTE, 1 * CONST.xKB]
    hash_sizes = [2048 * CONST.xBYTE]
    
    grouper_funcs: List[GroupFunc] = [ 
        GRPR.group_by_size \
        , GRPR.sha512_first_X_bytes(X = hash_sizes[0]) \
        #, GRPR.sha512_first_X_bytes(X = hash_sizes[1]) \
    ]
    
    found_groups: LocationGroups = FINDER.apply_multiple_groupers(\
                                    all_indices, grouper_funcs)
    #
    
    result_data = {
        "groups": found_groups \
        , "filtered_locations": filtered_locations \
        , "FINDER": FINDER \
        , "hash_sizes": hash_sizes \
        , "fls_unfiltered": fls_unfiltered \
    }
    
    return result_data
#)


def find_duplicates_from_dirs(IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
    """ Given folder paths, returns duplicate scan result as a dict. """
    
    IN_PATHS = UT.ignore_redundant_subdirs(IN_DIRS)
    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    result_data = find_duplicates(fls_unfiltered, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
    result_data["IN_PATHS"] = IN_PATHS
    
    return result_data
#)


