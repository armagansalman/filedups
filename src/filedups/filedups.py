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

#( System modules
import time
import logging
#)

#(
from common_types import *
import constants as CONST
from classes import FilesInfo, FileIndexer, DuplicateFinder
import argparser_custom as Argp
import util as UT
import grouper_funs as GRPR
#)

def find_duplicates(file_paths: Set[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
#(
    fls_unfiltered: Set[str] = file_paths
    
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
        , "fls_unfiltered": fls_unfiltered \
    }
    
    return result_data
#)


def find_duplicate_from_dirs(IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
    IN_PATHS = UT.ignore_redundant_subdirs(IN_DIRS)
    
    fls_unfiltered: Set[str] = UT.get_fpaths_from_path_iter(IN_PATHS)
    
    result_data = find_duplicates(fls_unfiltered, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
    result_data["IN_PATHS"] = IN_PATHS
    
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
        
        try:
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
        except:
            logging.error(f"Couldn't get size of file: {loc}")

        
        idx_grp += 1
    #)
#)

#from memory_profiler import profile

#@profile
def find_and_write_duplicates(out_fpath, IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT = None):    
    TM_beg = time.perf_counter()
    
    results = find_duplicate_from_dirs(IN_DIRS, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
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
    
    UT.append_file_text_utf8(out_fpath, ''.join(stringified))
#
