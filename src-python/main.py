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



# WARNING: Don't use print on Windows. Errors like "UnicodeEncodeError: 
# 'charmap' codec can't encode character '\u015f'" can occur

# NOTE(armagan): 512 bytes seem reasonable for the first pass (0th pass is always by size).
# NOTE(armagan): 8 kilo bytes seem reasonable for the second pass.
# TODO(armagan): For printing paths, split filename, write filename first.
# then write its path.

# TODO(armagan): Create hash,set(paths) groups. Traverse them in DFS and
# repeat the process. Recursively apple the process on every group until
# either 1 file remais or a condition is met.

import time

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
from classes import *
import util as UT
import grouper_funs as GRPR



#pic_path = "/home/public"

def full_reader(file_loc, start_idx, end_idx):
    return file_loc[:]

def reader_tmp(file_loc, start_idx, end_idx):
    # TODO(armagan): Use fopen or similar file reading functions.
    # Read bytes from file starting at idx 'start_idx'
    # including 'end_idx'.
    return file_loc[start_idx:end_idx]
#

def size_getter_tmp(file_loc):
    # File size in bytes.
    return len(file_loc)
#

finf_1 = FilesInfo(["abc", "bac", "cba"], reader_tmp, size_getter_tmp)
finf_2 = FilesInfo(["dabc"], reader_tmp, size_getter_tmp)
finf_3 = FilesInfo(["qdabc", "qdbac"], full_reader, size_getter_tmp)

finfos = [finf_1, finf_2, finf_3]


FIDX = FileIndexer(finfos)

"""
for i in range(FIDX.get_idx_count()):
    location = FIDX.get_location(i)
    fsize = FIDX.get_size_func(i)(location)
    fbytes = FIDX.get_reader(i)(location, 0, 2)
    
    print((location, fsize, fbytes))
#
"""


tmp_dict: Dict[str, Set] = dict() # Set makes every location unique.
#######

get_nonzero_length_files = UT.get_nonzero_length_files
#######



def main_1():
    # "/media/public/SAMSUNG/NOT SAMSUNG/Any backup before 2020-02-16/" # 224365 files ; 618.96 secs
    
    # "/media/public/SAMSUNG/NOT SAMSUNG/Aile family/",
    #GIVEN_PATHS = ["/home/public/"]
    #GIVEN_PATHS_1 = ["/home/public/Pictures/Aile family/"]
    #paths = ["/home/public/Desktop/find-file-duplicates-main/"]
    #paths = ["/home/public/Pictures/Wallpapers/"]
    
    GIVEN_PATHS_1 = ["H:/NOT SAMSUNG/Aile family"]
    
    szs = []
    string_seq = []
    #print(GIVEN_PATHS_1)
    string_seq.extend( [GIVEN_PATHS_1] )
    string_seq.append('\n')
    
    #print("HASH_BYTES:", HASH_BYTES)
    string_seq.extend( ["HASH_BYTES=", HASH_BYTES] )
    string_seq.append('\n')
    
    beg = time.perf_counter()

    paths: Set = set()
    
    
    
    for p in UT.get_fpaths_from_path_iter(GIVEN_PATHS_1):
        try:
            sz = UT.get_file_size_in_bytes(p)
            if sz > 0:
                paths.add(p)
                szs.append(sz)
        except:
            pass
    #
    
    #print(len(paths) , "files")
    string_seq.extend( [len(paths) , "files"] )
    string_seq.append('\n')
    
    
    for p in paths:
        # TODO(armagan): Rewrite. Not clean/correct.
        try:
            hs = UT.file_sha512(p, HASH_BYTES)
            sz = UT.get_file_size_in_bytes(p)
            #sz = 999
            group = tmp_dict.get(hs, set())
            
            size_location = (sz, p)
            group.add(size_location)
            
            tmp_dict[hs] = group
        except:
            #print("Can't get hash of:", p)
            string_seq.extend( ["Can't get hash of:", p] )
            string_seq.append('\n')
            
        #
        
    #

    for key in tmp_dict.keys():
        group = tmp_dict[key]
        if len(group) < 2:
            continue
        #
        
        #print(">>>>>>>", key[:32], "...")
        string_seq.extend( [">>>>>>>", key[:32], "..."] )
        string_seq.append('\n')
        
        for val in group:
            #print(val)
            string_seq.extend( [val] )
            string_seq.append('\n')
        #
        #print("################")
        string_seq.extend( ["################"] )
        string_seq.append('\n')
    
    
    
    
    end = time.perf_counter()

    #print("ELAPSED:", end-beg)
    string_seq.extend( ["ELAPSED:",end-beg, "seconds."] )
    string_seq.append('\n')
    
    #print(len(szs))
    string_seq.extend( ["Processed file count:", len(szs)] )
    string_seq.append('\n')
    
    #print("*****************************************************************")
    string_seq.extend( ["*****************************************************************"] )
    string_seq.append('\n')
    
    
    fpath = "2021-12-09_filedups-main-1_2.txt"
    
    stringified = map(str, string_seq)
    
    UT.append_file_text_utf8(fpath, ' '.join(stringified))
        
    #
#


def main_2(HASH_BYTES):
    
    TM_beg = time.perf_counter()
    print("HASH_BYTES=", HASH_BYTES)

    fls: Set[str] = get_nonzero_length_files(GIVEN_PATHS)

    def print_iterable(itr):
        for elm in itr:
            print(elm)
        #
    #

    #print_iterable(fls)


    fsinfo = FilesInfo(fls, UT.local_file_reader, UT.get_local_file_size)


    FINDX = FileIndexer([fsinfo])

    print(FINDX.get_all_indices())


    def sha512_all_FIDX_locs(FX: FileIndexer):
        indices: Iter_t[int] = FX.get_all_indices()
        groups: Dict[str, Set[str]] = dict()
        
        for ix in indices:
            loc = FX.get_location(ix)
            reader = FX.get_reader(ix)
            sizer = FX.get_size_func(ix)
            
            # 0.09671903399976145 sec = get all 3 data for all 3338 files.
            try:
                fdata: bytes = reader(loc, 0, HASH_BYTES-1)
                # 0.1660889649992896
                
                
                digest = UT.sha512_bytes(fdata)
                # ELAPSED: 0.18541843900129606
                # 0.18996872500065365
                # 0.2524847469994711
            except:
                # TODO(armagan): ???Report/abort/handle.
                print("Can't get hash of:", loc)
                continue # Skip this file. Can't access.
            
            # TODO(armagan): Rewrite. Not clean/correct.
            
            st = groups.get(digest, set())
            st.add(loc)
            groups[digest] = st
        #

        for key in groups.keys():
            paths = groups[key]
            if len(paths) < 2:
                continue
            #
            
            print(">>>>>>>", key[:32], "...")
            for val in paths:
                print(val)
            #
            print("################")
        
            
        #
    #


    print(sha512_all_FIDX_locs(FINDX))



    TM_end = time.perf_counter()

    print("ELAPSED:",TM_end - TM_beg)
    
    indices: Iter_t[int] = FINDX.get_all_indices()
    
    print(len(indices))
    print(indices[:7])
    print("***************************************")
    #
#


def main_3(out_fpath, IN_PATHS, HASH_SIZE, SMALLEST_FSIZE):
    # For local files.
    # TODO(armagan): Rewrite all.
    string_seq: List = []
    #, "D:\\"
    #GIVEN_PATHS_3 = ["D:\Documents\Aile", "D:\Documents", "D:\Documents\Game Related", "D:\\"]
    #GIVEN_PATHS_3 = ["H:/NOT SAMSUNG/Aile family"]
    GIVEN_PATHS_3 = IN_PATHS
    
    string_seq.extend( ["======= filedups-main-3 function begining ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    string_seq.extend( GIVEN_PATHS_3 )
    string_seq.append('\n')
    
    #print("TODO: Don't use print. Use a string list and write to file as utf-8 encoded.")
    #exit(0)
    
    TM_beg = time.perf_counter()
    
    #print("HASH_BYTES=", HASH_BYTES)

    string_seq.extend( ["HASH_SIZE(bytes)=", HASH_SIZE] )
    string_seq.append('\n')
    
    string_seq.extend( ["SMALLEST_FSIZE(bytes)=", SMALLEST_FSIZE] )
    string_seq.append('\n')

    fls: Set[str] = get_nonzero_length_files(GIVEN_PATHS_3)
    
    
    string_seq.extend( ["Total number of files to search=", len(fls)] )
    string_seq.append('\n')
    

    fsinfo = FilesInfo(fls, UT.local_file_reader, UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])

    

    def sha512_all_FIDX_locs(FX: FileIndexer):
        Group_Val_t = Set[Tuple[int, Any]] # int = len in bytes ; Any = location
        
        indices: List[int] = FX.get_all_indices()
        groups: Dict[str, Group_Val_t] = dict()
        
        file_report_counter = 0
        
        for ix in indices:
            loc = FX.get_location(ix)
            reader = FX.get_reader(ix)
            sizer = FX.get_size_func(ix)
            
            # 0.09671903399976145 sec = get all 3 data for all 3338 files.
            try:
                fsize: int = sizer(loc)
                
                if fsize < SMALLEST_FSIZE:
                    continue
                #
                
                fdata: bytes = reader(loc, 0, HASH_SIZE-1)
                # 0.1660889649992896
                
                
                digest = UT.sha512_bytes(fdata)
                # ELAPSED: 0.18541843900129606
                # 0.18996872500065365
                # 0.2524847469994711
                
                
                
                size_loc = (fsize, loc)
                
                st = groups.get(digest, set())
                st.add(size_loc)
                groups[digest] = st
            except:
                # TODO(armagan): ???Report/abort/handle.
                #print("Can't get hash of:", loc)
                
                string_seq.extend( ["Can't get hash of:", loc] )
                string_seq.append('\n')
                
                continue # Skip this file. Can't access.
            
            # TODO(armagan): Rewrite. Not clean/correct.
            
            
        #

        for key in groups.keys():
            paths = groups[key]
            if len(paths) < 2:
                # Skip unique file group.
                continue
            #
            
            #print(">>>>>>>", key[:32], "...")
            
            string_seq.extend( [">>>>>>>", key[:32], "..."] )
            string_seq.append('\n')
            
            
            
            for val in paths:
                #print(val)
                sz, loc = val
                if sz >= SMALLEST_FSIZE:                
                    string_seq.extend( [val] )
                    string_seq.append('\n')
                    
                    file_report_counter += 1
                #
            #
            #print("################")
            
            string_seq.extend( ["################"] )
            string_seq.append('\n')
            
        #
        
        string_seq.extend( ["Reported file count=", file_report_counter] )
        string_seq.append('\n')
        
        return len(indices)
    #


    #print("Processed file count:", sha512_all_FIDX_locs(FINDX))

    #string_seq.extend( ["Processed file count:", sha512_all_FIDX_locs(FINDX)] )
    #string_seq.append('\n')

    sha512_all_FIDX_locs(FINDX)

    TM_end = time.perf_counter()

    #print("ELAPSED:",TM_end - TM_beg)
    
    string_seq.extend( ["ELAPSED:",TM_end - TM_beg, "seconds."] )
    string_seq.append('\n')
    
    indices: Iter_t[int] = FINDX.get_all_indices()
    
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
#


#from memory_profiler import profile

#@profile
def main_4(out_fpath, IN_PATHS: List[str], SMALLEST_FSIZE):
    string_seq: List = []
    
    string_seq.extend( ["======= filedups-main-4 function begining ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    string_seq.append("Paths: ")
    string_seq.extend( IN_PATHS )
    string_seq.append('\n')
    
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
            sz = UT.get_file_size_in_bytes(path)
            if sz >= SMALLEST_SIZE:
                return True
            #
            return False
        #
        except:
            return False
    #
    
    string_seq.extend( ["Using size filter. Size(bytes)=", SMALLEST_SIZE] )
    string_seq.append('\n')
    
    locations: Set[str] = set(filter(flt_size, fls_unfiltered))
    
    # fls: Set[str] = UT.get_nonzero_length_files(IN_PATHS)
    
    string_seq.extend( ["Total number of files to search=", len(locations)] )
    string_seq.append('\n')
    

    fsinfo = FilesInfo(locations, UT.local_file_reader, \
                        UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])
    
    # TODO(armagan): Use DuplicateFinder class and group function(s).
    FINDER: DuplicateFinder = DuplicateFinder(FINDX, 0.5)
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    hs1 = 512
    hs2 = 8 * CONST.xKB
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
     , GRPR.sha512_first_X_bytes(X=hs1) \
     , GRPR.sha512_first_X_bytes(X=hs2) ]
    
    string_seq.extend( ["Groupers=size,{}-hash,{}-hash".format(hs1,hs2)] )
    string_seq.append('\n')
    
    found_groups: LocationGroups_t = FINDER.apply_multiple_groupers(\
                                    all_indices, grouper_funcs)
    
    
    """
    size_group: LocationGroups_t = FINDER.apply_one_grouper(all_indices,\
                                                        GRPR.group_by_size)
    #
    """
    
    i = 0
    for seq in found_groups:
        if len(list(seq)) < 2:
            continue # Skip unique files.
        
        string_seq.append("----------- [Group {}] start------".format(i))
        string_seq.append('\n')
        
        for loc_idx in seq:
            # TODO(armagan): This is an ugly way and code. Use PyConst or
            # immutable data structures instead of class/objects.
            # ??https://github.com/tobgu/pyrsistent
            
            loc = FINDER.get_file_indexer().get_location(loc_idx)
            string_seq.extend( ["File path:", loc])
            string_seq.append('\n')
            string_seq.extend( [">>> File name:", UT.get_path_basename(loc)])
            string_seq.append('\n')
        #
        string_seq.append("*********** [Group {}] END *******".format(i))
        string_seq.append('\n')
        string_seq.append('\n')
        
        i += 1
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


NOW = UT.get_now_str()

for i in range(3):
    """
    seq = ["abc", "def", "gh", "\n"]
    
    fpath = "tmp_2021-12-09.txt"
    
    UT.append_file_list_utf8(fpath, data = seq)
    UT.write_file_text_utf8(fpath, ''.join(seq), FORCE_OVERWRITE = False)
    
    print("TODO: Don't use print. Use a string list and write to file as utf-8 encoded.")
    exit(0)
    """
    
    #main_1()
    smallest_file_size: int = 1 * CONST.xBYTE
    
    OUTFILE_PATH = "{}_bigger than ({} bytes).txt".format(NOW, smallest_file_size)
    
    

    
    
    #search_paths_WINDOWS = ["D:\ALL BOOKS-PAPERS", "D:\Documents", "D:\HxD", "D:\Program Files"]
    
    #main_3(OUTFILE_PATH, search_paths_WINDOWS, HASH_BYTES, smallest_file_size)
    
    
    _search_paths_MINT = ["/media/genel/Bare-Data/ALL BOOKS-PAPERS/" \
    , "/media/genel/Bare-Data/Documents/" \
    , "/media/genel/Bare-Data/HxD/" \
    , "/media/genel/Bare-Data/Program Files/"]
    
    
    _search_paths = ["/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
    , "/media/genel/SAMSUNG/NOT SAMS/Anime-Cartoon-Manga/" \
    , "/media/genel/SAMSUNG/NOT SAMS/Aile fotolar, videolar/" \
    , "/media/genel/SAMSUNG/NOT SAMS/Aile family/"]
    # search_paths_MINT = "/media/genel/SAMSUNG/NOT SAMS/Alltxt files/"
    
    _search_paths_MINT = ["/media/genel/Bare-Data/"]
    
    _search_paths_MINT = ["/home/genel/"]
    
    search_paths = ["/home/genel/"]
    
    _search_paths = ["/media/genel/Bare-Data/"]
    
    # TODO(armagan): Separate apply func. and write to file.
    # TODO(armagan): Create LocalFileFinder
    # TODO(armagan): Combine 1 byte size filter and size grouper for performance.
    
    main_4(OUTFILE_PATH, search_paths, smallest_file_size)
#

"""
350871 items, totalling 759,9 GiB (815.983.211.147 bytes) = ext-disk,NOT SAM
"""

"""
ELAPSED: 56.87620095499733 seconds. 
 17354 files.
 ~300 files/second
"""
