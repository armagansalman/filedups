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



import argparse



def argparser_ver_0():  #(
    parser = argparse.ArgumentParser(
                prog='filedups',
                description='Finds local duplicate files. Found files may not be duplicates! Check before doing an action on them.',
            )
    #
    parser.add_argument('filename', help = ".txt file containing full directory paths on each line.") # positional argument
    parser.add_argument('--min-file-size', help = "Minimum file size in bytes.")      # option that takes a value
    parser.add_argument('--max-file-size', help = "Maximum file size in bytes.")      # option that takes a value
    
    return parser
#)


def create_parser(args, version_id):  #)
    script_name_removed_args = args[1:]
    
    parser = argparser_ver_0()
    
    return parser.parse_args(script_name_removed_args)
#)
