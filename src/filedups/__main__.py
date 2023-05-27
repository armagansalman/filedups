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



import main as M
import constants as CONST
import util as UT


if __name__ == "__main__":
    # TODO(Armağan): Restructure and clean the code.
    # TODO(Armağan): Given args for directories OR do gui as explained below:
    # TODO(Armağan): Use PySimpleGUI to select input text file that holds search directories.
    # 
    import sys
    
    if len(sys.argv) < 2:  #(
        raise Exception("No input file given as argument. Aborted.")
    #)
    
    arg_list = sys.argv[1:]
    
    first_arg: str = arg_list[0]  # .txt file which holds a dir path on each line.
    
    assert(first_arg.endswith(".txt"))
    
    args = dict()
    args["in-txt-filepath"] = first_arg
    
    M.main(args)
#
