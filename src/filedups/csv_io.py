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


import csv
from typing import Iterable, Any


def csv_read_file(
				file_path: str \
				, delimiter: str = ',' \
				, quotechar: str = '"' \
				, encoding='utf-8'):
	#
	with open(file_path, newline='', encoding=encoding) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
		
		for row in csv_reader:
			yield row
		#
	#
#

Iter = Iterable
def csv_write_file(
				file_path: str \
				, rows: Iter[Iter[Any]] \
				, file_mode: str = 'w' \
				, delimiter:str = ",", quotechar:str = '"' \
				, quoting = csv.QUOTE_MINIMAL \
				, encoding='utf-8'):
	#
	with open(file_path, file_mode, newline='', encoding=encoding) as csvfile:
		csv_writer = csv.writer(csvfile, delimiter=delimiter,
								quotechar=quotechar, quoting=quoting)
		#
		for row in rows:
			csv_writer.writerow(row)
		#
	#
#

def main(*args, **kwargs):	
	rows = [
			['Spam'] * 5 + ['Baked Beans'] \
			, ['Spam', 'Lovely Spam', 'Wonderful Spam']
	]
	
	fpath = 'eggs.csv'
	
	csv_write(fpath, rows)
	
	csv_rows = list(csv_read(fpath))
	
	for row, c_row in zip(rows, csv_rows):
		assert(row == c_row)
	#
	print("All assertions passed.")
#


if __name__ == "__main__":
	main()
#



