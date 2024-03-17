"""
MIT License

Copyright (c) 2024 Armağan Salman

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

# https://pythonassets.com/posts/browse-file-or-folder-in-tk-tkinter/

import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import main as M


# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('400x200')


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        initialdir=os.getcwd(),
        title='Open a file (directories)',
        filetypes=filetypes)

    MIN_FILE_SIZE = 1024 * 1024 # 1Mb

    args = dict()
    args["in-txt-filepath"] = filename
    args["min_file_size"] = MIN_FILE_SIZE
    args["max_file_size"] = None
    
    out_fpath = M.main(args)
    current_dir = os.getcwd()
    
    info = showinfo(
        title='Result File',
        message=os.path.join(current_dir, out_fpath)
    )
    print(info)


# open button
open_button = ttk.Button(
    root,
    text='Open a file that contains directories',
    command=select_file
)

open_button.pack(expand=True)


# run the application
root.mainloop()
