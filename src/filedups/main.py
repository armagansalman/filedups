"""
    <This file is a part of the program armaganymmt-prj-1_name.
    armaganymmt-prj-1_name processes files from different kinds of
    locations to find duplicate files.>
    
    Copyright (C) <2021-2023>  <Armağan Salman> <gmail: armagansalman>

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
import logging

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
from classes import *
import argparser_custom as Argp
import util as UT
import grouper_funs as GRPR






#from memory_profiler import profile

#@profile
def main_4(out_fpath, IN_DIRS: List[str], SMALLEST_FILE_SIZE_BYTE, MAX_SIZE_LIMIT = None):
    IN_PATHS = UT.ignore_redundant_subdirs(IN_DIRS)
    
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
    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    string_seq.extend( ["Total number of unfiltered files to search=", len(fls_unfiltered)] )
    string_seq.append('\n')
    
    
    SMALLEST_SIZE: int = SMALLEST_FILE_SIZE_BYTE
        
    string_seq.extend( ["SMALLEST_FILE_SIZE_BYTE(bytes)=", SMALLEST_FILE_SIZE_BYTE] )
    string_seq.append('\n')
    
    string_seq.extend( ["Using size filter. Size(bytes)=", SMALLEST_SIZE] )
    string_seq.append('\n')
    
    locations: Set[str] = set(UT.filter_by_size(fls_unfiltered, \
                            SMALLEST_FILE_SIZE_BYTE, MAX_SIZE_LIMIT))
    
    # fls: Set[str] = UT.get_nonzero_length_files(IN_PATHS)
    
    string_seq.extend( ["Total number of filtered files to search=", len(locations)] )
    string_seq.append('\n')
    

    fsinfo = FilesInfo(locations, UT.local_file_reader_first_bytes, \
                        UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])
    
    FINDER: DuplicateFinder = DuplicateFinder(FINDX)
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    hs1 = 64 * CONST.xBYTE
    hs2 = 1024 * CONST.xBYTE
    #hs2 = 1 * CONST.xKB
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
     , GRPR.sha512_first_X_bytes(X=hs1) \
    , GRPR.sha512_first_X_bytes(X=hs2) \
    ]
    
    string_seq.extend( ["Groupers=size,{}-hash,{}-hash".format(hs1,hs2)] )
    #string_seq.extend( ["Groupers=size,{}-hash".format(hs1)] )
    string_seq.append('\n')
    
    string_seq.extend( ["T.1 ; == ; Group id ; File size ; File Path"] )
    #string_seq.extend( ["Groupers=size,{}-hash".format(hs1)] )
    string_seq.append('\n')
    
    found_groups: LocationGroups_t = FINDER.apply_multiple_groupers(\
                                    all_indices, grouper_funcs)
    
    
    """
    size_group: LocationGroups_t = FINDER.apply_one_grouper(all_indices,\
                                                        GRPR.group_by_size)
    #
    """
    
    idx_grp = 0
    for i, grp in enumerate(found_groups):  #(
        
        grp = list(grp)
        if len(grp) < 2:
            continue # Skip unique files.
        
        #string_seq.append("+++++++++++ [Group {}] start +++++++".format(i))
        #string_seq.append('\n')
        
        loc_idx = grp[0]
        loc = FINDER.FIDX.get_location(loc_idx)
        fsize_tpl = FINDER.FIDX.get_size_func(loc_idx)(loc)
        fsize_byte = fsize_tpl[1]
        fsize_kb = fsize_byte / 1024  # Turns from BYTE -> KB
        
        # TODO(Armagan): Tidy up this mess of a function.
        
        SKIP_SIZE_BYTE = SMALLEST_FILE_SIZE_BYTE  # Don't show files smaller than this KB of size.
        
        if fsize_byte < SKIP_SIZE_BYTE: # skip if not at least SKIP_SIZE KB
            continue
        
        string_seq.append('~\n')
        
        for loc_idx in grp:  #(
            # TODO(armagan): This is an ugly way and code. Use PyConst or
            # immutable data structures instead of class/objects.
            # ??https://github.com/tobgu/pyrsistent
            
            loc = FINDER.FIDX.get_location(loc_idx)
            
            string_seq.extend( [f"T.1 ; G: {idx_grp} ; S: {fsize_kb:1.2f} (KB) ; P: {loc}"])
            string_seq.append('\n')
        #)
        
        idx_grp += 1
    #)
    
    TM_end = time.perf_counter()

    #print("ELAPSED:",TM_end - TM_beg)
    
    string_seq.extend( ["End datetime ISO-8601 = {}".format(UT.get_now_str())] )
    string_seq.append('\n')
    
    string_seq.extend( ["ELAPSED:",TM_end - TM_beg, "seconds."] )
    string_seq.append('\n')
    
    indices: List[int] = FINDX.get_all_indices()
    
    #print(len(indices))
    string_seq.extend( [f"Total file count for grouping was: {len(indices)}"] )
    string_seq.append('\n')
    
    #print(indices[:7])
    #string_seq.extend([indices[:7]])
    
    #print("***************************************")
    string_seq.extend( ["**********************************************************************"] )
    string_seq.append('\n')
    
    
    
    stringified = map(str, string_seq)
    
    UT.append_file_text_utf8(out_fpath, ' '.join(stringified))
#


def trials(trial_count: int, search_paths: List[str], SMALLEST_FILE_SIZE_BYTE: int):
    NOW = UT.get_now_str()

    for i in range(trial_count):
        
        OUTFILE_PATH = "filedups ({}) (at least ({:2.2f} bytes)).txt".format(NOW, SMALLEST_FILE_SIZE_BYTE/1024)
        
        # TODO(armagan): Separate apply func. and write to file.
        # TODO(armagan): Create LocalFileFinder
        # TODO(armagan): Combine 1 byte size filter and size grouper for performance.
        
        main_4(OUTFILE_PATH, search_paths, SMALLEST_FILE_SIZE_BYTE = SMALLEST_FILE_SIZE_BYTE)
    #
#

def check_existence_paths(paths: list):  #(
    import os
    
    for idx, pt in enumerate(paths):  #(
        if not os.path.exists(pt):
            raise Exception(f"Path doesn't exist.\nPath index (starts from 0): {idx}\nPaths:{paths}\n")
    #)
#)


def main(args):  #(
    logging.basicConfig(filename=f"filedups {UT.get_now_str()}.log", encoding='utf-8', level=logging.DEBUG)
    
    DEFAULT_MIN_FSIZE = 100 * CONST.xKB
    
    SMALLEST_FSIZE = DEFAULT_MIN_FSIZE
    
    msize = args["min_file_size"]
    if msize != None:
        SMALLEST_FSIZE = int(msize)
    #
    
    MAX_FSIZE = args["max_file_size"]
    if MAX_FSIZE != None:
        MAX_FSIZE = int(MAX_FSIZE)
    #    

    in_fname = args["in-txt-filepath"]
    
    in_txt_file_lines = UT.read_file_text(in_fname)
    
    search_paths_iter = map(lambda p: p.strip() , in_txt_file_lines)  # Remove prefix and suffix blank characters.
    search_paths = list(search_paths_iter)
    
    check_existence_paths(search_paths)
    
    print("<[ INFO ]> Finding duplicates...")
    
    NOW = UT.get_now_str()
    OUTFILE_PATH = "filedups ({}) (at least ({} KB)).txt".format(NOW, int(SMALLEST_FSIZE/1024))
    
    return main_4(OUTFILE_PATH, search_paths, SMALLEST_FSIZE, MAX_FSIZE)
#)


if __name__ == "__main__":
    # TODO(Armağan): Restructure and clean the code.
    # TODO(Armağan): Given args for directories OR do gui as explained below:
    # TODO(Armağan): Use PySimpleGUI to select input text file that holds search directories.
    # 
    import sys
    
    if len(sys.argv) < 2:  #(
        raise Exception("No input file given as argument. Aborted.")
    #)
    
    parser_version = 0
    parsed_args = Argp.create_parser(sys.argv, parser_version)
    
    args = dict()
    args["in-txt-filepath"] = parsed_args.filename
    args["min_file_size"] = parsed_args.min_file_size
    args["max_file_size"] = parsed_args.max_file_size
    
    main(args)
#

