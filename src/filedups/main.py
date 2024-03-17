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



# WARNING: Errors like "UnicodeEncodeError: 
# 'charmap' codec can't encode character '\u015f'" can occur on Windows terminal.


import time
import logging

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]
from common_types import *
import constants as CONST
import argparser_custom as Argp
import util as UT
import filedups_api as FDAPI
import csv_io as cio



def check_existence_paths(paths: list[str]):  #(
    import os
    
    for idx, pt in enumerate(paths):  #(
        if not os.path.exists(pt):
            raise Exception(f"Path doesn't exist.\nPath index (starts from 0): {idx}\nPaths:{paths}\n")
    #)
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
    
    results = FDAPI.find_duplicates_from_dirs(IN_DIRS, MIN_SIZE_LIMIT, MAX_SIZE_LIMIT)
    
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
    
    return out_fpath
#

def main(args: dict):  #(
    NOW = UT.get_now_str()
    
    logging.basicConfig(filename=f"filedups ({NOW}).log", encoding='utf-8', level=logging.DEBUG)
    
    DEFAULT_MIN_FSIZE = 1000 * CONST.xKB
    
    MIN_FSIZE = DEFAULT_MIN_FSIZE
    
    msize = args["min_file_size"]
    if msize != None:
        MIN_FSIZE = int(msize)
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
    print(f"<[ INFO ]> Search started at: {UT.get_now_str()}")
    print("<[ INFO ]> It can take minutes to hours depending on the number of files.")
    print("<[ INFO ]> It takes at least 3 minutes to filter 284000 files to 40300 files and then find duplicates.")
    print("<[ INFO ]> It takes at least 19 minutes to filter 286000 files to 140000 files and then find duplicates.")
    
    OUTFILE_PATH = "filedups ({}) (at least ({} KB)).txt".format(NOW, int(MIN_FSIZE/1024))
    
    return find_and_write_duplicates(OUTFILE_PATH, search_paths, MIN_FSIZE, MAX_FSIZE)
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

