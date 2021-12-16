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


"""
no-hash_-_ELAPSED: 0.049525973008712754_-_3338 files
1-B hash_-_ELAPSED: 0.1311204009980429_-_3338 files
128-B hash_-_ELAPSED: 0.13475250000192318_-_3338 files
256-B hash_-_ELAPSED: 0.13714175000495743_-_3338 files
512-B hash_-_ELAPSED: 0.14457203799975105_-_3338 files
1-KB hash_-_ELAPSED: 0.14528957300353795_-_3338 files
2-KB hash_-_ELAPSED: 0.1580927140021231_-_3338 files
4-KB hash_-_ELAPSED: 0.17637374300102238_-_3338 files

Cold-start:
256-B_-_ELAPSED: 156.7744490999903_-_20729 files (home/public)
4-KB_-_ELAPSED: 31.84445598500315_-_3338 files (pics/Aile family)

"""

# NOTE(armagan): 256 bytes seem reasonable for the first pass.
# TODO(armagan): FOr printing paths, split filename, write filename first.
# then write its path.

# TODO(armagan): Create hash,set(paths) groups. Traverse them in DFS and
# repeat the process. Recursively apple the process on every group until
# either 1 file remais or a condition is met.

import time

from typing import Set
from typing import Sequence
from typing import AnyStr
from typing import Dict
from typing import Iterable as Iter

from collections.abc import Iterable

import util as UT
from classes import *


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


xB = 1
xKB = 1024 * xB
xMB = 1024 * xKB

HASH_BYTES = 1 * xKB

tmp_dict: Dict[str, Set] = dict()

for i in range(3):
	# "/media/public/SAMSUNG/NOT SAMSUNG/Any backup before 2020-02-16/" # 224365 files ; 618.96 secs
	
	# "/media/public/SAMSUNG/NOT SAMSUNG/Aile family/",
	#GIVEN_PATHS = ["/home/public/"]
	GIVEN_PATHS = ["/home/public/Pictures/Aile family/"]
	#paths = ["/home/public/Desktop/find-file-duplicates-main/"]
	#paths = ["/home/public/Pictures/Wallpapers/"]
	
	szs = []
	print(GIVEN_PATHS)
	print("HASH_BYTES:", HASH_BYTES)
	
	beg = time.perf_counter()

	paths = []
	
	
	
	for p in UT.get_fpaths_from_path_iter(GIVEN_PATHS):
		try:
			sz = UT.get_file_size_in_bytes(p)
			if sz > 0:
				paths.append(p)
				szs.append(sz)
		except:
			pass
	#
	
	print(len(paths) , "files")
	
	for p in paths:
		# TODO(armagan): Rewrite. Not clean/correct.
		try:
			hs = UT.file_sha512(p, HASH_BYTES)
		except:
			print("Can't get hash of:", p)
		#
		st = tmp_dict.get(hs, set())
		st.add(p)
		tmp_dict[hs] = st
	#

	for key in tmp_dict.keys():
		st = tmp_dict[key]
		if len(paths) < 2:
			continue
		#
		
		print(">>>>>>>", key[:32], "...")
		for val in st:
			print(val)
		#
		print("################")
	
	
	
	
	end = time.perf_counter()

	print("ELAPSED:", end-beg)
	print(len(szs))
	print(szs[:7])
	print("***************************************")
#

