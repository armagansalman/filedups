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


from common_types import *


# Some type definitions:
StartIdx = int
EndIdx = int
Locations = List[int]


class DuplicateFinder:
    
    FILE_PATHS = None  # File Indexer
	
    def __init__(self, file_paths):
        if type(file_paths) != list:
            file_paths = list(file_paths)
        #
        self.FILE_PATHS = file_paths
    #
    
    
    def get_file_paths(self):
        return self.FILE_PATHS
    #
    
    def get_all_file_indices(self):
        return [i for i in range(len(self.FILE_PATHS))]
    #
    
    def apply_one_grouper(self, file_indices, \
                        FUNC) \
                        -> LocationGroups_t:
        #
        locs: LocationGroups_t = FUNC(self, file_indices)
        return locs
    #
    
    
    def rec_apply(self, file_indices, FUNC_IDX: int, \
                    GROUPERS: List[Callable]) \
                    -> LocationGroups_t:
        #
        locs: Set[int] = file_indices
        
        if len(locs) < 2 or FUNC_IDX >= len(GROUPERS):
            # Fewer than 2 files can't be duplicates. 
            # OR No grouper func. left to apply.
            return [locs]
        #
        
        loc_groups: LocationGroups_t = self.apply_one_grouper(locs,\
                                                    GROUPERS[FUNC_IDX])
        #
        
        NEXT_FUNC_IDX = FUNC_IDX + 1
        combined_groups = []
        
        for grp in loc_groups:
            sub_grp_result: LocationGroups_t = self.rec_apply(grp, \
                                                NEXT_FUNC_IDX, GROUPERS)
            #
            for sub_grp in sub_grp_result:
                combined_groups.append(sub_grp)
            #
        #
        
        return combined_groups
    #
    
    
    def apply_multiple_groupers(self, file_paths, \
                    GROUPERS: List[Callable]) -> LocationGroups_t:
        GROUPER_FUNC_IDX = 0
        
        result_groups: LocationGroups_t = self.rec_apply(file_paths, \
                                            GROUPER_FUNC_IDX, GROUPERS)
        #
        return result_groups
    #
    
#

GroupFunc_t = Callable[[DuplicateFinder, Locations], LocationGroups_t]
