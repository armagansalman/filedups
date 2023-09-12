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


import util as UT
from common_types import *
from classes import *


def group_by_size(FIDX: FileIndexer, LOCS: LocationIndices_t) -> LocationGroups_t:
    
    size_groups: Dict[int, Set[int]] = dict()
    for IDX in LOCS:
        LOC = FIDX.get_location(IDX)
        SFUN = FIDX.get_size_func(IDX)
        SIZE: Maybe = SFUN(LOC)
        
        # TODO(armagan): Report/except when SIZE == None.
        if is_nothing(SIZE):
            continue
        #
        sz: int = get_data(SIZE)
        
        # Group location indices which have the same size:
        group: Set[int] = size_groups.get(sz, set())
        group.add(IDX)
        size_groups[sz] = group
    #
    
    res: List[Set[int]] = list()
    for key, val in size_groups.items():
        res.append(val)
    #
    
    return res
#


def sha512_first_X_bytes(X: int) -> GroupFunc_t:
    #
    def grouper(FIDX: FileIndexer, LOCS: LocationIndices_t) -> LocationGroups_t:
        #
        hash_groups: Dict[int, Set[int]] = dict()
        
        for IDX in LOCS:
            LOC = FIDX.get_location(IDX)
            read_func = FIDX.get_reader(IDX)
            FIRST_X_BYTES = read_func(LOC, X) # end byte idx = X-1
            
            # TODO(armagan): Report/except when FIRST_X_BYTES == None.
            if is_nothing(FIRST_X_BYTES):
                continue
            #
            data: bytes = get_data(FIRST_X_BYTES)
            
            hex_hash = UT.sha512_bytes(data)
            
            group: Set[int] = hash_groups.get(hex_hash, set())
            group.add(IDX)
            hash_groups[hex_hash] = group
        #
        
        res: List[Set[int]] = list()
        for key, val in hash_groups.items():
            res.append(val)
        #
        
        return res
    #
    
    return grouper
#
