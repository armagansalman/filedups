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


"""

Design/Decisions/Definitions:
    + A 'file' is an ordered sequence of bytes.
        It has a non-negative size. 
        A slice of its bytes can be read given a 'start_idx' and
        'end_idx'.
    
    + FilesInfo type:
        + Has 'locations' iterable which holds multiple 'location' 
        values. A 'location' can be any type as long as it can be read 
        from a user given reader function.
        
        + Has 'reader_func' function that reads and returns bytes from
        a file. If 'end_idx' is bigger than file length, reads all 
        the way to the end (starting at 'start_idx').
        
            Its signature is:
        byte[] reader_func(location: Any, start_idx: int, end_idx: int)

        + Has 'size_getter' function that returns the number of bytes 
        the file has.
        
            Its signature is:
        non_negative_int size_getter(location: Any)
    
    + FileIndexer type:
        + Why: To easily handle different location types and
        reader functions. For example, a FilesInfo object might hold 
        local files and another one holds links to web documents.
        Core part of the program doesn't have to know about such 
        differences.
        
        + An object of this type (e.g FIDX) assigns every location
        an index (e.g lidx). Using this lidx, its related 'location',
        'reader_func', 'size_getter' can be retrieved in an uniform way
        via FIDX.
        
    + DuplicateFinder type:
        + Accepts a 'FileIndexer' object and a float value that denotes
        how similar can two files be if they are to be grouped as 
        duplicate. For example, 25% means that at least 25% of the files' 
        content starting from index 0 to 25% of the file must be the same.
        
        Concrete example: For 25% similarity constraint,
        file-1 = [0,1,0,0,1,0,1,1]
        file-2 = [1,1,0,0,1,0,1,1]
        these two files would NOT be grouped as duplicates. Because 
        their first element is different.
        
        + Has 'get_file_indexer' function. Returns the member.
        
        + Has 'group_files' function. Takes similarity percentage as float.
        A FileGroup is an iterable of file indices (from FileIndexer).
        'group_files' function returns an iterable of FileGroup elements. 
        
        + TODO(armagan): ???optional byte count constraint.
        + TODO(armagan): ???Make 'DuplicateFinder' just a function interface.
"""


# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from common_types import *


#T_FXR = FileIndexer
#T_CALL = Callable
#T_iter = Iter_t

#T_DupLocs = Set[int] # A group of duplicate files is a set of thier indices.
#T_DupGroups = T_iter[T_DupLocs]

#T_grouper = Callable[[T_FXR, Iter_t[int], float], Iter_t[int]]

StartIdx = int
EndIdx = int

class FilesInfo:
    def __init__(self, locations: Iter_t[Any] \
    , reader_func: Callable[[Any, StartIdx, EndIdx], bytes] \
    , size_getter: Callable[[Any], int]):
    #   
        self.locations: List[Any]  = list(set(locations))
        # set to remove duplicate locations.
        # Ensure it's subscriptable.
        
        self.reader_func = reader_func
        self.size_getter = size_getter
    #
#


class FileIndexer:
    def __init__(self, files_info_iter: Iter_t[FilesInfo]):
        self.data: Sequence[FilesInfo] = []
        # self.g_ref holds (x,y) ; x = file_info idx, y = location idx 
        # in that  file_info.locations
        self.g_ref: Sequence[Tuple[int,int]] = []
        
        for idx, files_info in enumerate(files_info_iter):
            self.data.append(files_info)
            for jdx, loc in enumerate(files_info.locations):
                self.g_ref.append((idx, jdx))
            #
        #
    #
    
    def get_location(self, idx: int) -> Any:
        (data_idx, loc_idx) = self.g_ref[idx]
        locations: Sequence[Any] = self.data[data_idx].locations
        return locations[loc_idx]
    #
    
    def get_reader(self, idx: int) -> Callable[[Any, int, int], bytes]:
        data_pos = self.g_ref[idx]
        return self.data[data_pos[0]].reader_func
    #
    
    def get_size_func(self, idx: int) -> Callable[[Any], int]:
        data_pos = self.g_ref[idx]
        return self.data[data_pos[0]].size_getter
    #
    
    def get_max_idx(self) -> int:
        # Total number of locations minus 1.
        return len(self.g_ref)
    #
    
    def get_all_indices(self) -> List[int]:
        return [x for x in range(self.get_max_idx())]
    #
#






MatchPercentage_t = float

GroupFunc_t = Callable[[FileIndexer, LocationIndices_t, \
                        MatchPercentage_t], LocationGroups_t]


class DuplicateFinder:
    #def __init__(self \
    #X = TypeVar(Callable[[FileIndexer, Iter_t[int], float], Tuple(FileIndexer,Iter_t[int])])
    #, groupers: Sequence[Tuple[FileIndexer, float]]):
    #   self.GRP = groupers
    #
    
    def __init__(self, FILE_INDEXER: FileIndexer, \
                SIMILARITY_PERCENTAGE: float):
        self.FIDX = FILE_INDEXER
        self.SIMILARITY = SIMILARITY_PERCENTAGE
    #
    
    
    def get_file_indexer(self):
        return self.FIDX
    #
    
    
    def apply_one_grouper(self, LOCS: LocationIndices_t, \
                        FUNC: GroupFunc_t) -> LocationGroups_t:
        #
        locs: LocationGroups_t = FUNC(self.FIDX, LOCS, \
                                            self.SIMILARITY)
        return locs
    #
    
    
    def rec_apply(self, LOCS: LocationIndices_t, FUNC_IDX, \
                    GROUPERS: List[GroupFunc_t]) -> LocationGroups_t:
        #
        locs: Set[int] = set(LOCS)
        if len(locs) < 2: # Fewer than 2 files can't be duplicates.
            return [locs]
        #
        
        if FUNC_IDX >= len(GROUPERS): # No grouper func. left to apply.
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
        # TODO(armagan): ???User MUST ??? match percentage.
        GROUPER_FUNC_IDX = 0
        result_groups: LocationGroups_t = self.rec_apply(LOCS, \
                                            GROUPER_FUNC_IDX, GROUPERS)
        #
        return result_groups
    #
    
    """
    def group_files(self, similarity_percentage):
        for lref in self.FIDX.get_idx_count():
            loc = self.FIDX.get_location(lref)
            reader = self.FIDX.get_reader(lref)
            size_func = self.FIDX.get_size_func(lref)
            #
    """
#

