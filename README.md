# filedups
<br>Given a sequence of paths (full directory paths), finds and groups duplicate files recursively.
<br>Doesn't provide 100% accuracy. Reported files in a group might not be exactly the same.

## HOW TO USE
Go to src/filedups in terminal.
<br>Put full paths of directories you want to search in in-dirs.txt file on separate lines.
<br>Options (M, X are the number of bytes) (default value is 1024000 (1000 KB)): 
<br>--min-file-size M
<br>--max-file-size X

<br>Then run main.py:
<br>For Linux:
<br>**python3 main.py in-dirs.txt**

<br><br>1000 KB minimum file size:
<br>**python3 main.py in-dirs.txt --min-file-size 1024000**

<br><br>200 KB minimum, 2000 KB maximum file size:
<br>**python3 main.py in-dirs.txt --min-file-size 204800 --max-file-size 2048000**

<br>For Windows:
<br>**py main.py in-dirs.txt**
<br>or
<br>**python3 main.py in-dirs.txt**

<br>Results will be in a text file of current working directory of command line
<br>, which starts with filedups and contains timestamp of the scan.
