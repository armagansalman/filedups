"""
    Copyright (C) 2021-2023  Armağan Salman

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
FileTriple = Tuple[Location, ReaderFunc, SizeFunc]

class FileIndexer:
    data = None
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
                info: FileTriple = (loc, finfo_idx)
                    
                self.data.append(info)
            #
            finfo_idx += 1
        #
    #
    
    
    def get_file_info(self, idx: int) -> FileTriple:
        info: FileTriple = self.data[idx]
        return info
    #
    
    
    def get_location(self, idx: int) -> Location:
        info: FileTriple = self.get_file_info(idx)
        return info[0]
    #
    
    
    def get_reader(self, idx: int) -> ReaderFunc:
        info: FileTriple = self.get_file_info(idx)
        return self.fns_file_reader[info[1]]
    #
    
    
    def get_size_func(self, idx: int) -> SizeFunc:
        info: FileTriple = self.get_file_info(idx)
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

