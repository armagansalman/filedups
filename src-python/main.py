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


main-2; 256-B hash_-_ELAPSED: 0.14755042799879448_-_3338 files
[
Double traversal:
main-2; 256-B hash_-_ELAPSED: 0.19136745800278732_-_3338 files
main-2; 1-KB hash_-_ELAPSED: 0.1997125239977322_-_3338 files
main-2; 2-KB hash_-_ELAPSED: 0.21675798000069335_-_3338 files
main-2; 4-KB hash_-_ELAPSED: 0.23161685800005216_-_3338 files
]

Cold-start:
256-B_-_ELAPSED: 156.7744490999903_-_20729 files (home/public)
4-KB_-_ELAPSED: 31.84445598500315_-_3338 files (pics/Aile family)


"""

# NOTE(armagan): 512 bytes seem reasonable for the first pass.
# TODO(armagan): For printing paths, split filename, write filename first.
# then write its path.

# TODO(armagan): Create hash,set(paths) groups. Traverse them in DFS and
# repeat the process. Recursively apple the process on every group until
# either 1 file remais or a condition is met.

import time

# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

import types
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


xB: int = 1
xKB: int = 1024 * xB
xMB: int = 1024 * xKB


tmp_dict: Dict[str, Set] = dict() # Set makes every location unique.


def file_grouper(FXR: FileIndexer, MATCH_PERCENTAGE: float) \
-> Iter_t[Iter_t[int]]:
	# Returns multiple groups of file indices. Files in each group are
	# duplicates to the degree given by MATCH_PERCENTAGE.
	
	
	
	
	z1 = [1,2]
	z2 = {3,4,5}
	return list([z1, z2])
#

"""
res = file_grouper(FIDX, 0.23)

print(res)

data = UT.local_file_reader("./main.py", 0, 15)

print("<",data,">")
"""


"""
GIVEN_PATHS: List[str]= [ \
"/home/public/Pictures/Aile family/" \
, "/home/public/Pictures/Aile family/" ]
"""

GIVEN_PATHS: List[str] = \
[
"/home/public" \
]

HASH_BYTES: int = 512 * xB

def get_nonzero_length_files(paths_arg: Iter_t[str]):
	unq_paths_arg = set(paths_arg)
	paths: Set = set()
	# Set makes every location unique.
	
	for p in UT.get_fpaths_from_path_iter(unq_paths_arg):
		try:
			sz = UT.get_file_size_in_bytes(p)
			if sz > 0:
				paths.add(p)
		except:
			pass
	#
	
	return paths
#


def main_3():
	# For local files.
	# TODO(armagan): Rewrite all.
	TM_beg = time.perf_counter()
	
	print("HASH_BYTES=", HASH_BYTES)

	fls: Set[str] = get_nonzero_length_files(GIVEN_PATHS)

	fsinfo = FilesInfo(fls, UT.local_file_reader, UT.get_local_file_size)

	FINDX = FileIndexer([fsinfo])


	def sha512_all_FIDX_locs(FX: FileIndexer):
		indices: Iterable_t[int] = FX.get_all_indices()
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


def main_2():
	
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
		indices: Iterable_t[int] = FX.get_all_indices()
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



def main_1():

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
			paths = tmp_dict[key]
			if len(paths) < 2:
				continue
			#
			
			print(">>>>>>>", key[:32], "...")
			for val in paths:
				print(val)
			#
			print("################")
		
		
		
		
		end = time.perf_counter()

		print("ELAPSED:", end-beg)
		print(len(szs))
		print(szs[:7])
		print("***************************************")
	#
#

for i in range(3):
	main_2()
#

