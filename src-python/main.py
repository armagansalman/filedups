"""
    <This file is a part of the program armaganymmt-prj-1_name.
    armaganymmt-prj-1_name processes files from different kinds of
    locations to find duplicate files.>
    
    Copyright (C) <2021-2023>  <Armağan Salman> <gmail,protonmail: armagansalman>

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



# WARNING: Don't use print on Windows. Errors like "UnicodeEncodeError: 
# 'charmap' codec can't encode character '\u015f'" can occur

# NOTE(armagan): 512 bytes seem reasonable for the first pass (0th pass is always size pass).
# NOTE(armagan): 8 kilo bytes seem reasonable for the second pass.
# TODO(armagan): For printing paths, split filename, write filename first.
# then write its path.

# TODO(armagan): Create hash,set(paths) groups. Traverse them in DFS and
# repeat the process. Recursively apply the process on every group until
# either 1 file remains or a condition is met.


import time

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
from classes import *
import util as UT
import grouper_funs as GRPR




#from memory_profiler import profile

#@profile
def main_4(out_fpath, IN_PATHS: List[str], SMALLEST_FILE_SIZE):
    string_seq: List = []
    
    string_seq.extend( ["======= filedups-main-4 function begining ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    string_seq.append("Paths: \n")
    string_seq.append( '\n'.join(IN_PATHS) )
    string_seq.append('\n\n')
    
    TM_beg = time.perf_counter()
    
    #print("HASH_BYTES=", HASH_BYTES)

    # string_seq.extend( ["HASH_SIZE(bytes)=", HASH_SIZE] )
    # string_seq.append('\n')
    
    string_seq.extend( ["SMALLEST_FSIZE(bytes)=", SMALLEST_FSIZE] )
    string_seq.append('\n')

    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    SMALLEST_SIZE: int = SMALLEST_FSIZE
    
    def flt_size(path: str):
        #
        try:
            sz: MaybeInt = UT.get_file_size_in_bytes(path)
            if is_nothing(sz):
                return False
            #
            if get_data(sz) >= SMALLEST_SIZE:
                return True
            #
            return False
        #
        except: # TODO(armagan): Report/except when exception occurs.
            return False
    #
    
    string_seq.extend( ["Using size filter. Size(bytes)=", SMALLEST_SIZE] )
    string_seq.append('\n')
    
    locations: Set[str] = set(filter(flt_size, fls_unfiltered))
    
    # fls: Set[str] = UT.get_nonzero_length_files(IN_PATHS)
    
    string_seq.extend( ["Total number of filtered files to search=", len(locations)] )
    string_seq.append('\n')
    

    fsinfo = FilesInfo(locations, UT.local_file_reader, \
                        UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])
    
    # TODO(armagan): Use DuplicateFinder class and group function(s).
    FINDER: DuplicateFinder = DuplicateFinder(FINDX, 0.5)
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    hs1 = 32 * CONST.xBYTE
    hs2 = 1024 * CONST.xBYTE
    #hs2 = 1 * CONST.xKB
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
     , GRPR.sha512_first_X_bytes(X=hs1) \
    , GRPR.sha512_first_X_bytes(X=hs2) \
    ]
    
    string_seq.extend( ["Groupers=size,{}-hash,{}-hash".format(hs1,hs2)] )
    #string_seq.extend( ["Groupers=size,{}-hash".format(hs1)] )
    string_seq.append('\n')
    
    found_groups: LocationGroups_t = FINDER.apply_multiple_groupers(\
                                    all_indices, grouper_funcs)
    
    
    """
    size_group: LocationGroups_t = FINDER.apply_one_grouper(all_indices,\
                                                        GRPR.group_by_size)
    #
    """
    
    #idx_grp = 0
    for idx_grp, grp in enumerate(found_groups):
        
        grp = list(grp)
        if len(grp) < 2:
            continue # Skip unique files.
        
        #string_seq.append("+++++++++++ [Group {}] start +++++++".format(i))
        #string_seq.append('\n')
        
        loc_idx = grp[0]
        loc = FINDER.FIDX.get_location(loc_idx)
        fsize_tpl = FINDER.FIDX.get_size_func(loc_idx)(loc)
        fsize = fsize_tpl[1] / 1024
        
        # TODO(Armagan): Tidy up this mess of a function.
        
        X = 3
        
        if fsize < 1024 * X: # skip if not at least X MB
            continue
        
        string_seq.append('~\n')
        
        for loc_idx in grp:
            # TODO(armagan): This is an ugly way and code. Use PyConst or
            # immutable data structures instead of class/objects.
            # ??https://github.com/tobgu/pyrsistent
            
            loc = FINDER.FIDX.get_location(loc_idx)
            
            string_seq.extend( [f"G: {idx_grp} ; S: {fsize:3.2f} (KB) ; P: {loc}"])
            string_seq.append('\n')
            #string_seq.extend( [">>> File name:", UT.get_path_basename(loc)])
            #string_seq.append('\n')
            #string_seq.append('\n')
        #
        #string_seq.append("----------- [Group {}] END -------".format(idx_grp))
        #string_seq.append('\n')
        #string_seq.append('\n')
        
        #idx_grp += 1
    #
    """"""
    TM_end = time.perf_counter()

    #print("ELAPSED:",TM_end - TM_beg)
    
    string_seq.extend( ["End datetime ISO-8601 = {}".format(UT.get_now_str())] )
    string_seq.append('\n')
    
    string_seq.extend( ["ELAPSED:",TM_end - TM_beg, "seconds."] )
    string_seq.append('\n')
    
    indices: List[int] = FINDX.get_all_indices()
    
    #print(len(indices))
    string_seq.extend( [len(indices)] )
    string_seq.append('\n')
    
    #print(indices[:7])
    #string_seq.extend([indices[:7]])
    
    #print("***************************************")
    string_seq.extend( ["**********************************************************************"] )
    string_seq.append('\n')
    
    
    
    stringified = map(str, string_seq)
    
    UT.append_file_text_utf8(out_fpath, ' '.join(stringified))
#


def trials(trial_count: int, search_paths: List[str], SMALLEST_FILE_SIZE: int):
    NOW = UT.get_now_str()

    for i in range(trial_count):
        
        OUTFILE_PATH = "filedups ({}) (at least ({:2.2f} bytes)).txt".format(NOW, SMALLEST_FILE_SIZE/1024)
        
        # TODO(armagan): Separate apply func. and write to file.
        # TODO(armagan): Create LocalFileFinder
        # TODO(armagan): Combine 1 byte size filter and size grouper for performance.
        
        main_4(OUTFILE_PATH, search_paths, SMALLEST_FILE_SIZE = SMALLEST_FILE_SIZE)
    #

    """
    350871 items, totalling 759,9 GiB (815.983.211.147 bytes) = ext-disk,NOT SAM
    """

    """
    At least 1 byte size filter.
    Groupers=size,512-hash,8192-hash
    ELAPSED: 56.87620095499733 seconds. 
     17354 files.
     ~300 files/second
    """

    """
    At least 1 byte size filter.
    Groupers=size,512-hash,8192-hash 
     ELAPSED: 115.64341640401108 seconds. 
     29288 
     ~250 files/second
    """
#


if __name__ == "__main__":
    # TODO(Armağan): Given args for directories OR do gui as explained below:
    # TODO(Armağan): Use PySimpleGUI to select input text file that holds search directories.
    # 
    _search_paths_MINT = ["/media/genel/Bare-Data/ALL BOOKS-PAPERS/" \
        , "/media/genel/Bare-Data/Documents/" \
        , "/media/genel/Bare-Data/HxD/" \
        , "/media/genel/Bare-Data/Program Files/"]
    #
    
    _search_paths_WIN10 = ["D:\ALL BOOKS-PAPERS" \
        , "D:\Documents" \
        , "D:\HxD" \
        , "D:\Program Files"]
    #
    
    _search_paths = ["/home/genel/"] # or "D:/"
    # trials(3, search_paths) # for performance measurement of cold/hot data.
    
    
    search_paths = [ \
        "/media/genel/SAMSUNG/NOT SAMS/BCK~_2023-01-18T11_/" \
        ,"/media/genel/SAMSUNG/NOT SAMS/BCK~_2023-02-20T13_/" \
        ,"/media/genel/SAMSUNG/NOT SAMS/BCK~HP~_2022-05-06_/" \
        ,"/media/genel/SAMSUNG/NOT SAMS/BCK~Mint~_2022-12-17_/" \
        ,"/media/genel/SAMSUNG/NOT SAMS/BCK~Sandisk-32GB~_2023-02-20_/" \
    ]
    
    SMALLEST_FSIZE = 32 * CONST.xKB
    trials(1, search_paths, SMALLEST_FILE_SIZE = SMALLEST_FSIZE) # 1 == Just to find local duplicates.
#


"""
_search_paths_MINT = ["/media/genel/Bare-Data/ALL BOOKS-PAPERS/" \
, "/media/genel/Bare-Data/Documents/" \
, "/media/genel/Bare-Data/HxD/" \
, "/media/genel/Bare-Data/Program Files/"]
"""

"""
_search_paths = ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
, "/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
, "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
, "/media/genel/SAMSUNG/NOT SAMS/Aile family/"]
# search_paths_MINT = "/media/genel/SAMSUNG/NOT SAMS/Alltxt files/"
"""
