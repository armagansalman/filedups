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
import argparser_custom as Argp
import util as UT
import filedups


def check_existence_paths(paths: list[str]):  #(
    import os
    
    for idx, pt in enumerate(paths):  #(
        if not os.path.exists(pt):
            raise Exception(f"Path doesn't exist.\nPath index (starts from 0): {idx}\nPaths:{paths}\n")
    #)
#)


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
    
    return filedups.find_and_write_duplicates(OUTFILE_PATH, search_paths, MIN_FSIZE, MAX_FSIZE)
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

