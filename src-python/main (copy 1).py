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


import time

import util as UT
from classes import *


pic_path = "/home/public"

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

for i in range(3):
	# "/media/public/SAMSUNG/NOT SAMSUNG/Any backup before 2020-02-16/" # 224365 files ; 618.96 secs
	
	# "/media/public/SAMSUNG/NOT SAMSUNG/Aile family/",
	paths = ["/home/public/Pictures/Aile family/"]
	paths = ["/media/public/SAMSUNG/NOT SAMSUNG/+18 porn/"]
	paths = ["/media/public/SAMSUNG/NOT SAMSUNG/Aile fotolar, videolar/"]
	szs = []
	print(paths)
	
	beg = time.perf_counter()

	paths = UT.get_fpaths_from_path_iter(paths)
	print(len(paths) , "files")
	
	
	for p in paths:
		try:
			sz = UT.get_file_size_in_bytes(p)
			szs.append(sz)
		except:
			pass
	#
	
	

	end = time.perf_counter()

	print("ELAPSED:", end-beg)
	print(len(szs))
	print(szs[:7])
	print("###########")

