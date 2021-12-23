"""
    <This file is a part of the program armaganymmt-prj-1_name.
    armaganymmt-prj-1_name processes files from different kinds of
    locations to find duplicate files.>
    
    Copyright (C) <2021>  <Armağan Salman> <gmail,protonmail: armagansalman>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import util as UT
from common_types import *
from classes import *


def grouper_example(file_indexer, location_indices, match_percentage):
    return
#


def group_by_size(FIDX: FileIndexer, LOCS: LocationIndices_t, \
                    PERC: MatchPercentage_t) -> LocationGroups_t:
    
    size_groups: Dict[int, Set[int]] = dict()
    for IDX in LOCS:
        LOC = FIDX.get_location(IDX)
        SFUN = FIDX.get_size_func(IDX)
        SIZE = SFUN(LOC)
        
        # Group location indices which have the same size:
        group: Set[int] = size_groups.get(SIZE, set())
        group.add(IDX)
        size_groups[SIZE] = group
    #
    res: List[Set[int]] = list()
    for key, val in size_groups.items():
        res.append(val)
    #
    return res
#


def sha512_first_X_bytes(X: int) -> GroupFunc_t:
    #
    def grouper(FIDX: FileIndexer, LOCS: LocationIndices_t, \
                    PERC: MatchPercentage_t) -> LocationGroups_t:
        #
        hash_groups: Dict[int, Set[int]] = dict()
        
        for IDX in LOCS:
            LOC = FIDX.get_location(IDX)
            read_func = FIDX.get_reader(IDX)
            FIRST_X_BYTES = read_func(LOC, 0, X-1) # end byte idx = X-1
            
            hex_hash = UT.sha512_bytes(FIRST_X_BYTES)
            
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
                        
