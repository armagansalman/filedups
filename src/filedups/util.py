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



import os
import hashlib
import io
import datetime

import common_types as CT
from common_types import *


def get_utc_datetime_now():
    return datetime.datetime.now()
#


def get_now_str():
    now = get_utc_datetime_now()
    now_str = "{}-{}-{}T{}-{}-{}".format(now.year, now.month, now.day, now.hour \
    , now.minute, now.second)
    return now_str
#


def get_path_basename(PATH: str):
    return os.path.basename(PATH)
#


def get_fpaths_recursively_from_folder(PATH: str):
    rec_files: Set = set()
    # TODO(armaganslmn): ??? Error handling.
    
    if os.path.isfile(PATH):
        rec_files.add(PATH)
        return rec_files
    #
    
    elif os.path.isdir(PATH):
        for root, dirs, files in os.walk(PATH):
            for name in files:
                p = os.path.join(root, name)
                rec_files.add(os.path.abspath(p))
            #
        #
    
    else: # Link or something else. Ignore them.
        pass
    #
    return rec_files
#


def get_absolute_path(path: CT.Str): #(
    return os.path.abspath(path)
#)

def ignore_redundant_subdirs(dirs: CT.Iter[CT.Str]):
    """ If a dir D_1 is a descendant of a dir D_2, don't include D_1 as
        it will be included with recursive search of D_2. 
        WARNING: If a given path is a file, it will also be ignored.
    """
# (
    dirs_tpl = tuple(dirs)

    abs_paths = list(map(get_absolute_path, filter(os.path.isdir, dirs_tpl)))

    if len(abs_paths) < 1:
        # (
        raise Exception(
            f"Can't get directory paths from given dirs (are they valid directories?): {str(dirs_tpl)}")
    # )

    abs_paths.sort()

    prev = abs_paths[0]

    essential_dirs = []

    for ix in range(1, len(abs_paths)):
        # (
        current = abs_paths[ix]

        if current.startswith(prev):  # Current is a descendant, ignore.
            # (
            continue
        # )
        else:
            # (
            essential_dirs.append(prev)
            prev = current
        # )
    # )
    essential_dirs.append(prev)

    return essential_dirs
# )

def get_fpaths_from_path_iter(paths_iter: List[str]):
    if type(paths_iter) != list:
        raise Exception("A list of str paths must be given.")
    
    file_paths: Set = set()
    unq_paths = set(paths_iter)
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    for path in unq_paths:
        file_paths = file_paths.union( get_fpaths_recursively_from_folder(path) )
    #
    return file_paths
#


def get_file_size_in_bytes(path) -> MaybeInt:
    try:
        statinfo = os.stat(path)
        return make_some(statinfo.st_size)
    #
    except: # TODO(armagan): Report/except when exception occurs.
        # Don't fail silently.
        return make_nothing()
    #    
#

def get_local_file_size(PATH: str) -> MaybeInt:
	return get_file_size_in_bytes(PATH)
#

def get_nonzero_length_files(paths_arg: List[str]):
    paths: Set = set()
    # Set makes every location unique.
    
    for p in get_fpaths_from_path_iter(paths_arg):
        try:
            sz: MaybeInt = get_file_size_in_bytes(p)
            if is_nothing(sz):
                continue
            #
            if get_data(sz) >= 1:
                paths.add(p)
        except: # TODO(armagan): Report/except when exception occurs.
            pass
    #
    
    return paths
#


def local_file_reader_first_bytes(file_path: str, first_bytes_count: int) \
        -> Tuple[bool, bytes]:
    # Includes bytes at start_offset and end_offset
    try:
        data: bytes = b'0'
        
        #TODO(armagan): Read by chunks.
        with open(file_path, "rb") as in_fobj:
            data = in_fobj.read(first_bytes_count)
        #
        
        return make_some(data)
    except: # TODO(armagan): Report/except when None.
        return make_nothing()
#


def local_file_reader_range(file_path: str, start_offset: int, \
        end_offset: int) -> Tuple[bool, bytes]:
    # Includes bytes at start_offset and end_offset
    try:
        data: bytes = b'0'
        
        #TODO(armagan): Read by chunks.
        with open(file_path, "rb") as in_fobj:
            in_fobj.seek(start_offset)
            data = in_fobj.read(end_offset - start_offset + 1)
        #
        
        return make_some(data)
    except: # TODO(armagan): Report/except when None.
        return make_nothing()
#


def filter_by_size(paths: CT.Iter[str], min_limit = None, max_limit = None):
#
    included_paths = []
    for pt in paths:  #(
        try:  # TODO(Armağan): Don't hide errors.
            msz: MaybeInt = get_file_size_in_bytes(pt)
            
            sz = get_data(msz)
            
            min_cond = (min_limit != None and sz >= min_limit) or min_limit == None
            max_cond = (max_limit != None and sz <= max_limit) or max_limit == None
            
            if min_cond and max_cond:
                included_paths.append(pt)
            #
        except: # TODO(armagan): Report/except when exception occurs.
            continue
    #)
    return included_paths
#

def sha512_bytes(data: bytes):
	hs = hashlib.sha512()
	hs.update(data)
	return hs.hexdigest()
#


def file_sha512(file_path, size_to_read):
    hs = hashlib.sha512()
    data = None
    
    with open(file_path, "rb") as in_fobj:
        data = in_fobj.read(size_to_read)
    #
    
    hs.update(data)
    return hs.hexdigest()
#

def write_file_utf8(fpath: str, text: str, OPEN_MODE: str):

    with io.open(fpath, OPEN_MODE, encoding='utf8') as F:
        F.write(text)
    #
#


def append_file_list_utf8(fpath: str, data: List):
    write_file_utf8(fpath, ''.join(data), 'a')
    print("[ INFO ] Appended to file:", fpath)
#


def append_file_text_utf8(fpath: str, text: str):
    write_file_utf8(fpath, text, 'a')
    print("[ INFO ] Appended to file:", fpath)
#


def write_file_text_utf8(fpath: str, text: str, FORCE_OVERWRITE = False):  #(
    # Write text(utf8) to file.
    if os.path.exists(fpath) and FORCE_OVERWRITE == True:
        write_file_utf8(fpath, text, 'w')
        print("[ INFO ] Written (mode = w) to file:", fpath)
        return True
    #
    else:
        print("[ WARNING ] NO text was written to file: '", fpath, "' FORCE_OVERWRITE = ", FORCE_OVERWRITE)
        return False
    #
#)


def read_file_text(fpath: str, encoding: str = 'utf8'):  #(
    if not os.path.exists(fpath):
        raise Exception(f"File not found. Path: {fpath}")
    
    with open(fpath, 'r', encoding = encoding) as fr:  #(
        return fr.readlines()
    #)
#




"""
def getSHA256(currentFile, full=False):
	#Read the 64k at a time, hash the buffer & repeat till finished. 
	#By default only checksum the first block
	hasher = hashlib.sha256()
	with open(currentFile, 'rb') as file:
		buf = file.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			if not full:
				break
			buf = file.read(BLOCKSIZE)
	return hasher.hexdigest()
"""



"""
with io.open(filename,'r',encoding='utf8') as f:
    text = f.read()
# process Unicode text
with io.open(filename,'w',encoding='utf8') as f:
    f.write(text)
"""
