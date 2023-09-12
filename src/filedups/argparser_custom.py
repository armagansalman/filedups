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
