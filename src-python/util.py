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


import os
import hashlib


def get_fpaths_recursively_from_folder(PATH):
    rec_files = set()
    # TODO(armaganslmn): ??? Error handling.
    if os.path.isfile(PATH):
        rec_files.add(PATH)
        return rec_files
    #
    
    for root, dirs, files in os.walk(PATH):
        for name in files:
            p = os.path.join(root, name)
            rec_files.add(os.path.abspath(p))
        #
    #
    return rec_files
#


def get_fpaths_from_path_iter(paths_iter):
    file_paths = []
    # TODO(armaganslmn): Handle if input is file.
    # TODO(armaganslmn): ??? Error handling.
    for path in paths_iter:
        file_paths.extend( get_fpaths_recursively_from_folder(path) )
    #
    return file_paths
#


def get_file_size_in_bytes(path):
    statinfo = os.stat(path)
    return statinfo.st_size
#

def get_local_file_size(PATH: str) -> int:
	return get_file_size_in_bytes(PATH)
#

def local_file_reader(file_path: str, start_offset: int, end_offset: int) -> bytes:
	# Includes bytes at start_offset and end_offset
	data = None
    
    #TODO(armagan): Read by chunks.
	with open(file_path, "rb") as in_fobj:
		in_fobj.seek(start_offset)
		data = in_fobj.read(end_offset - start_offset + 1)
    #
    
	return data
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
