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

Design/Decisions/Definitions:
	+ A 'file' is an ordered sequence of bytes.
		It has a non-negative size. 
		A slice of its bytes can be read given a 'start_idx' and
		'end_idx'.
	
	+ FilesInfo type:
		+ Has 'locations' iterable which holds multiple 'location' 
		values. A 'location' can be any type as long as it can be read 
		from a user given reader function.
		
		+ Has 'reader_func' function that reads and returns bytes from
		a file. If 'end_idx' is bigger than file length, reads all 
		the way to the end (starting at 'start_idx').
		
			Its signature is:
		byte[] reader_func(location: Any, start_idx: int, end_idx: int)

		+ Has 'size_getter' function that returns the number of bytes 
		the file has.
		
			Its signature is:
		non_negative_int size_getter(location: Any)
	
	+ FileIndexer type:
		+ Why: To easily handle different location types and
		reader functions. For example, a FilesInfo object might hold 
		local files and another one holds links to web documents.
		Core part of the program doesn't have to know about such 
		differences.
		
		+ An object of this type (e.g FIDX) assigns every location
		an index (e.g lidx). Using this lidx, its related 'location',
		'reader_func', 'size_getter' can be retrieved in an uniform way
		via FIDX.
"""


class FilesInfo:
	def __init__(self, locations, reader_func, size_getter):
		self.locations = locations
		self.reader_func = reader_func
		self.size_getter = size_getter
	#
#


class FileIndexer:
	def __init__(self, files_info_iter):
		self.data = []
		# self.g_ref holds (x,y) ; x = file_info idx, y = location idx 
		# in that  file_info.locations
		self.g_ref = []
		
		for idx, files_info in enumerate(files_info_iter):
			self.data.append(files_info)
			for jdx, loc in enumerate(files_info.locations):
				self.g_ref.append((idx, jdx))
			#
		#
	#
	
	def get_location(self, idx):
		(data_idx, loc_idx) = self.g_ref[idx]
		locations = self.data[data_idx].locations
		return locations[loc_idx]
	#
	
	def get_reader(self, idx):
		data_pos = self.g_ref[idx]
		return self.data[data_pos[0]].reader_func
	#
	
	def get_size_func(self, idx):
		data_pos = self.g_ref[idx]
		return self.data[data_pos[0]].size_getter
	#
	
	def get_idx_count(self):
		# Total number of locations minus 1.
		return len(self.g_ref)
#


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
finf_2 = FilesInfo(["dabc", "dbac", "dcba"], reader_tmp, size_getter_tmp)
finf_3 = FilesInfo(["qdabc", "qdbac", "qdcba"], full_reader, size_getter_tmp)

finfos = [finf_1, finf_2, finf_3]


FIDX = FileIndexer(finfos)

print(FIDX.get_idx_count())
print(FIDX.get_location(8))
print(FIDX.get_location(5))
print(FIDX.get_location(0))

for i in range(FIDX.get_idx_count()):
	location = FIDX.get_location(i)
	fsize = FIDX.get_size_func(i)(location)
	fbytes = FIDX.get_reader(i)(location, 0, 2)
	
	print((location, fsize, fbytes))
#










"""

def data_indexer(file_info_iter):
	all_data = []
	
	for elm in file_info_iter:
		all_data.append(elm)
	#
	
	g_idx = 0
	g_ref = []
	for idx, files_info in enumerate(all_data):
		for loc in files_info.locations:
			g_ref.append(idx)
	#
	print(g_ref)
	return(g_ref)
#


g_idx = data_indexer(finfos)

print(g_idx[0])


"""
