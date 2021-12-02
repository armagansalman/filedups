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


class FilesInfo:
	def __init__(self, locations, reader_func, size_getter):
		self.locations = locations
		self.reader_func = reader_func
		self.size_getter = size_getter
	#
#

class FileIndexer:
	def __init__(self, file_info_iter):
		self.data = []
		self.g_ref = []
		
		for idx, files_info in enumerate(file_info_iter):
			self.data.append(files_info)
			for loc in files_info.locations:
				self.g_ref.append(idx)
			#
		#
	#
	
	def get_location(self, idx):
		data_pos = self.g_ref[idx]
		return self.data[data_pos].reader_func
	#
	
	def get_reader(self, idx):
		data_pos = self.g_ref[idx]
		return self.data[data_pos].reader_func
	#
	
	def get_size_func(self, idx):
		data_pos = self.g_ref[idx]
		return self.data[data_pos].size_getter
	#
	
	def get_max_idx(self):
		# Total number of locations minus 1.
		return len(self.g_ref) - 1
#







def reader_tmp():
	pass
#

def size_getter_tmp(inp):
	return size(inp)
#

finf_1 = FilesInfo(["abc", "bac", "cba"], reader_tmp, size_getter_tmp)
finf_2 = FilesInfo(["dabc", "dbac", "dcba"], reader_tmp, size_getter_tmp)
finf_3 = FilesInfo(["qdabc", "qdbac", "qdcba"], reader_tmp, size_getter_tmp)

finfos = [finf_1, finf_2, finf_3]


FIDX = FileIndexer(finfos)

print(FIDX.get_max_idx())












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
