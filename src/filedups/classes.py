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


# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from common_types import *


StartIdx = int
EndIdx = int

Location = Any
ReaderFunc = Callable[[Any, StartIdx, EndIdx], Tuple[bool, bytes]]
SizeFunc = Callable[[Any], Tuple[bool, int]]

class FilesInfo:
    def __init__(self, locations: Iter_t[Any] \
    , reader_func: ReaderFunc \
    , size_getter: SizeFunc):
    #   
        self.locations: List[Location]  = list(set(locations))
        # set data type to remove duplicate locations.
        # Ensure it's subscriptable.
        
        self.reader_func = reader_func
        self.size_getter = size_getter
    #
#


# Type Definition:
# FileTriple = Tuple[Location, ReaderFunc, SizeFunc]
IndexedFile = Tuple[Any, int]

class FileIndexer:
    data: Any = None
    fns_file_reader: List[Callable] = None
    fns_file_size: List[Callable] = None
    
    def __init__(self, files_info_iter: Iter_t[FilesInfo]):
        self.data: List[str] = list()
        self.fns_file_reader = list()
        self.fns_file_size = list()
        
        finfo_idx = 0

        for files_info in files_info_iter:
            self.fns_file_reader.append(files_info.reader_func)
            self.fns_file_size.append(files_info.size_getter)
            
            for loc in files_info.locations:
                info: IndexedFile = (loc, finfo_idx)
                    
                self.data.append(info)
            #
            finfo_idx += 1
        #
    #
    
    
    def get_file_info(self, idx: int) -> IndexedFile:
        info: IndexedFile = self.data[idx]
        return info
    #
    
    
    def get_location(self, idx: int) -> Location:
        info: IndexedFile = self.get_file_info(idx)
        return info[0]
    #
    
    
    def get_reader(self, idx: int) -> ReaderFunc:
        info: IndexedFile = self.get_file_info(idx)
        return self.fns_file_reader[info[1]]
    #
    
    
    def get_size_func(self, idx: int) -> SizeFunc:
        info: IndexedFile = self.get_file_info(idx)
        return self.fns_file_size[info[1]]
    #
    
    
    def get_data_len(self) -> int:
        return len(self.data)
    #
    
    
    def get_all_indices(self) -> List[int]:
        return [x for x in range(self.get_data_len())]
    #
    
#


# Some type definitions:
GroupFunc_t = Callable[[FileIndexer, LocationIndices_t], LocationGroups_t]


class DuplicateFinder:
    FIDX = None  # File Indexer
	
    def __init__(self, FILE_INDEXER: FileIndexer):
        self.FIDX = FILE_INDEXER
    #
    
    
    def get_file_indexer(self):
        return self.FIDX
    #
    
    
    def apply_one_grouper(self, LOCS: LocationIndices_t, \
                        FUNC: GroupFunc_t) -> LocationGroups_t:
        #
        locs: LocationGroups_t = FUNC(self.FIDX, LOCS)
        return locs
    #
    
    
    def rec_apply(self, LOCS: LocationIndices_t, FUNC_IDX: int, \
                    GROUPERS: List[GroupFunc_t]) -> LocationGroups_t:
        #
        locs: Set[int] = set(LOCS)
        if len(locs) < 2 or FUNC_IDX >= len(GROUPERS):
            # Fewer than 2 files can't be duplicates. 
            # OR No grouper func. left to apply.
            return [locs]
        #
        
        loc_groups: LocationGroups_t = self.apply_one_grouper(locs,\
                                                    GROUPERS[FUNC_IDX])
        #
        
        NEXT_FUNC_IDX = FUNC_IDX + 1
        combined_groups: List[LocationIndices_t] = []
        
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
    
    
    def apply_multiple_groupers(self, LOCS: LocationIndices_t, \
                    GROUPERS: List[GroupFunc_t]) -> LocationGroups_t:
        GROUPER_FUNC_IDX = 0
        result_groups: LocationGroups_t = self.rec_apply(LOCS, \
                                            GROUPER_FUNC_IDX, GROUPERS)
        #
        return result_groups
    #
    
#

