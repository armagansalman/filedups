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
from classes import DuplicateFinder, GroupFunc_t
import argparser_custom as Argp
import util as UT
import grouper_funs as GRPR
import csv_io as cio
#)

def find_duplicates(file_paths: Set[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT):  #(
#(
    fls_unfiltered: Set[str] = set(file_paths)
    
    SMALLEST_SIZE: int = MIN_SIZE_LIMIT
    
    filtered_locations: Set[str] = set(UT.filter_by_size(fls_unfiltered, \
                            MIN_SIZE_LIMIT, MAX_SIZE_LIMIT))
    #
    
    FINDER: DuplicateFinder = DuplicateFinder(filtered_locations)
    all_indices: List[int] = FINDER.get_all_file_indices()
        
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
        , "filtered_locations": filtered_locations \
        , "FINDER": FINDER \
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


def write_typed_group_data(found_groups, FINDER, MIN_SIZE_LIMIT, csv_rows): #(
    idx_grp = 0
    ALL_PATHS = FINDER.get_file_paths()
    
    groups_with_size = []
    
    for group in found_groups:
        group = list(group)
        
        if len(group) < 2:  #(
            continue # Skip unique files.
        #)
        
        loc = ALL_PATHS[group[0]]
        
        try:
            fsize_tpl = UT.get_file_size_in_bytes(loc)
            fsize_byte = fsize_tpl[1]
            
            if fsize_byte < MIN_SIZE_LIMIT:
                continue
            #
            groups_with_size.append((group, fsize_byte))
        #
        except:
            logging.error(f"Couldn't get size of file: {loc}")
        #
    #
    groups_with_size.sort(key = lambda x: x[1], reverse = True)  # Sort groups by size. Descending.
        
    for i, group_and_size in enumerate(groups_with_size):  #(
        
        grp, SIZE = group_and_size
        
        loc = ALL_PATHS[grp[0]] # Take an element for getting size.

        try: #(
            fsize_tpl = UT.get_file_size_in_bytes(loc)
            fsize_byte = fsize_tpl[1]
            fsize_kb = fsize_byte / 1024  # Turns from BYTE -> KB

            # Don't show files smaller than this KB of size.
            if fsize_byte < MIN_SIZE_LIMIT:
                continue
            
            csv_rows.append(['T:0'])
            
            for loc_idx in grp:  #(
                loc = ALL_PATHS[loc_idx]
                
                csv_rows.append( ["T:1", f"{idx_grp}", f"{fsize_kb:1.2f} (KB)", f"{loc}"])
            #)
		#)
        except: #(
            logging.error(f"Couldn't get size of file: {loc}")

        idx_grp += 1
        #)
    #)
#)

#from memory_profiler import profile

#@profile
def find_and_write_duplicates(out_fpath, IN_DIRS: List[str], MIN_SIZE_LIMIT, MAX_SIZE_LIMIT = None):    
    NOW_STR = UT.get_now_str()
    
    TM_beg = time.perf_counter()
    
    results = find_duplicate_from_dirs(IN_DIRS, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
    TM_end_group = time.perf_counter()
    
    locations = results["filtered_locations"]
    locations_len = len(locations)
    hash_sizes = results["hash_sizes"]
    IN_PATHS = results["IN_PATHS"]
    fls_unfiltered = results["fls_unfiltered"]
    
    csv_rows: List[List[Any]] = []
    
    CSV_DELIMITER = ';'
    CSV_QUOTECHAR = '"'
    
    csv_rows.append([f"csv delimiter = {CSV_DELIMITER}"])
    csv_rows.append([f"csv quotechar = {CSV_QUOTECHAR}"])
    
    csv_rows.append( ["T:0", "==", "Empty row"] )
    csv_rows.append( ["T:1", "==", "Group id", "File size", "File Path"] )
    csv_rows.append( ["T:2", "==", "Input directory paths"] )
    csv_rows.append( ["T:3", "==", "Info"] )
    
    
    csv_rows.append( ["T:3", "======= filedups find_and_write_duplicates function begining ======= "] )
    
    csv_rows.append( ["T:3", "Start datetime ISO-8601 = {}".format(NOW_STR)] )

    csv_rows.append(["T:2", IN_PATHS])
    
    csv_rows.append( ["T:3", "Total number of unfiltered files to search=", len(fls_unfiltered)] )
    
    csv_rows.append( ["T:3", "Using size filter. Min Size(bytes)=", MIN_SIZE_LIMIT] )
    
    csv_rows.append( ["T:3", "Using size filter. Max Size(bytes)=", MAX_SIZE_LIMIT] )
    
    csv_rows.append( ["T:3", "Total number of filtered files to search=", locations_len] )
    
    csv_rows.append( ["T:3", "Groupers = size, hashes (bytes)-{}".format(hash_sizes)] )
    
    found_groups = results["groups"]
    FINDER = results["FINDER"]
    
    # Write groups to str buffer. Each line holds at least a group id and a path.
    write_typed_group_data(found_groups, FINDER, MIN_SIZE_LIMIT, csv_rows)
    
    TM_end_str_write = time.perf_counter()

    csv_rows.append( ["T:3", "End datetime ISO-8601 = {}".format(UT.get_now_str())] )
    
    csv_rows.append( ["T:3", "Elapsed Time for Grouping:",TM_end_group - TM_beg, "seconds."] )
    
    csv_rows.append( ["T:3", "Total Elapsed Time:",TM_end_str_write - TM_beg, "seconds."] )
    
    fpaths: List[str] = FINDER.get_file_paths()
    
    csv_rows.append( ["T:3", f"Total file count for grouping was: {len(fpaths)}"] )

    csv_rows.append( ["T:3", "**********************************************************************"] )
    
    fname = f"filedups ({NOW_STR}) at least ({MIN_SIZE_LIMIT} bytes).csv"
    
    cio.csv_write_file(fname, csv_rows, delimiter = CSV_DELIMITER \
						, quotechar = CSV_QUOTECHAR)
    #
    print(f"[ INFO ] Results were written to file: `{fname}`")
#
