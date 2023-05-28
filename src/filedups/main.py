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



# WARNING: Errors like "UnicodeEncodeError: 
# 'charmap' codec can't encode character '\u015f'" can occur on Windows terminal.


import time
import logging

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
from classes import FilesInfo, FileIndexer, DuplicateFinder
import argparser_custom as Argp
import util as UT
import grouper_funs as GRPR




def find_duplicate_groups(IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
    IN_PATHS = UT.ignore_redundant_subdirs(IN_DIRS)
    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    SMALLEST_SIZE: int = MIN_SIZE_LIMIT
    
    locations: Set[str] = set(UT.filter_by_size(fls_unfiltered, \
                            MIN_SIZE_LIMIT, MAX_SIZE_LIMIT))
    #
    
    fsinfo = FilesInfo(locations, UT.local_file_reader_first_bytes, \
                        UT.get_local_file_size)

    FINDX = FileIndexer([fsinfo])
    
    FINDER: DuplicateFinder = DuplicateFinder(FINDX)
    all_indices: Set[int] = FINDER.get_file_indexer().get_all_indices()
    
    #hash_sizes = [64 * CONST.xBYTE, 1 * CONST.xKB]
    hash_sizes = [2048 * CONST.xBYTE]
    
    grouper_funcs: List[GroupFunc_t] = [ GRPR.group_by_size \
        , GRPR.sha512_first_X_bytes(X = hash_sizes[0]) \
        #, GRPR.sha512_first_X_bytes(X = hash_sizes[1]) \
    ]
    
    
    found_groups: LocationGroups_t = FINDER.apply_multiple_groupers(\
                                    all_indices, grouper_funcs)
    #
    
    result_data = {"groups": found_groups \
        , "finder": FINDER \
        , "findx": FINDX \
        , "locations": locations \
        , "hash_sizes": hash_sizes \
        , "IN_PATHS": IN_PATHS \
        , "fls_unfiltered": fls_unfiltered \
    }
    
    return result_data
#)


def write_typed_group_data(found_groups, FINDER, FINDX, MIN_SIZE_LIMIT, string_seq): #(
    idx_grp = 0
    for i, grp in enumerate(found_groups):  #(
        
        grp = list(grp)
        if len(grp) < 2:  #(
            continue # Skip unique files.
        #)
                
        loc_idx = grp[0]
        loc = FINDER.FIDX.get_location(loc_idx)
        fsize_tpl = FINDER.FIDX.get_size_func(loc_idx)(loc)
        fsize_byte = fsize_tpl[1]
        fsize_kb = fsize_byte / 1024  # Turns from BYTE -> KB
        
        # TODO(Armagan): Tidy up this mess of a function.
        
        SKIP_SIZE_BYTE = MIN_SIZE_LIMIT  # Don't show files smaller than this KB of size.
        
        if fsize_byte < SKIP_SIZE_BYTE:
            continue
        
        string_seq.append('~\n')
        
        for loc_idx in grp:  #(
            loc = FINDER.FIDX.get_location(loc_idx)
            
            string_seq.extend( [f"T:1 ; G: {idx_grp} ; S: {fsize_kb:1.2f} (KB) ; P: {loc}"])
            string_seq.append('\n')
        #)
        
        idx_grp += 1
    #)
#)


#from memory_profiler import profile

#@profile
def find_and_write_duplicates(out_fpath, IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT = None):    
    TM_beg = time.perf_counter()
    
    results = find_duplicate_groups(IN_DIRS, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
    TM_end_group = time.perf_counter()
    
    locations = results["locations"]
    locations_len = len(locations)
    hash_sizes = results["hash_sizes"]
    IN_PATHS = results["IN_PATHS"]
    fls_unfiltered = results["fls_unfiltered"]
    
    string_seq: List = []
    
    string_seq.extend( ["======= filedups find_and_write_duplicates function begining ======= "] )
    string_seq.append('\n')
    
    now_str = UT.get_now_str()
    
    string_seq.extend( ["Start datetime ISO-8601 = {}".format(now_str)] )
    string_seq.append('\n')
    
    
    
    string_seq.append("Paths: \n")
    string_seq.append( '\n'.join(IN_PATHS) )
    string_seq.append('\n\n')
    
    
    string_seq.extend( ["Total number of unfiltered files to search=", len(fls_unfiltered)] )
    string_seq.append('\n')
    
    string_seq.extend( ["Using size filter. Min Size(bytes)=", MIN_SIZE_LIMIT] )
    string_seq.append('\n')
    string_seq.extend( ["Using size filter. Max Size(bytes)=", MAX_SIZE_LIMIT] )
    string_seq.append('\n')
    
    
    string_seq.extend( ["Total number of filtered files to search=", locations_len] )
    string_seq.append('\n')
    
    string_seq.extend( ["Groupers = size, hashes (bytes)-{}".format(hash_sizes)] )
    string_seq.append('\n')
    
    
    string_seq.extend( ["T:1 ; == ; Group id ; File size ; File Path"] )
    string_seq.append('\n')
    
    found_groups = results["groups"]
    FINDER = results["finder"]
    FINDX = results["findx"]
    
    # Write groups to str buffer. Each line holds at least a group id and a path.
    write_typed_group_data(found_groups, FINDER, FINDX, MIN_SIZE_LIMIT, string_seq)
    
    TM_end_str_write = time.perf_counter()

    string_seq.append('~\n')

    string_seq.extend( ["End datetime ISO-8601 = {}".format(UT.get_now_str())] )
    string_seq.append('\n')
    
    string_seq.extend( ["Elapsed Time for Grouping:",TM_end_group - TM_beg, "seconds."] )
    string_seq.append('\n')
    string_seq.extend( ["Total Elapsed Time:",TM_end_str_write - TM_beg, "seconds."] )
    string_seq.append('\n')
    
    indices: List[int] = FINDX.get_all_indices()
    
    string_seq.extend( [f"Total file count for grouping was: {len(indices)}"] )
    string_seq.append('\n')

    string_seq.extend( ["**********************************************************************"] )
    string_seq.append('\n')
    
    
    
    stringified = map(str, string_seq)
    
    UT.append_file_text_utf8(out_fpath, ' '.join(stringified))
#

def check_existence_paths(paths: list):  #(
    import os
    
    for idx, pt in enumerate(paths):  #(
        if not os.path.exists(pt):
            raise Exception(f"Path doesn't exist.\nPath index (starts from 0): {idx}\nPaths:{paths}\n")
    #)
#)


def main(args):  #(
    NOW = UT.get_now_str()
    
    logging.basicConfig(filename=f"filedups ({NOW}).log", encoding='utf-8', level=logging.DEBUG)
    
    DEFAULT_MIN_FSIZE = 1000 * CONST.xKB
    
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
    print("<[ INFO ]> It can take minutes to hours depending on the number of files.")
    
    OUTFILE_PATH = "filedups ({}) (at least ({} KB)).txt".format(NOW, int(SMALLEST_FSIZE/1024))
    
    return find_and_write_duplicates(OUTFILE_PATH, search_paths, SMALLEST_FSIZE, MAX_FSIZE)
#)


if __name__ == "__main__":
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

