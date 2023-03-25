# FIND FILE DUPLICATES
<br>Given a sequence of paths (full directory paths), finds and groups duplicate files recursively.
<br>Doesn't provide 100% accuracy. Reported files in a group might not be exactly the same.

## HOW TO USE
Put full paths of directories you want to search in in-dirs.txt file on separate lines.
<br>Then run main.py as:
<br>For Linux:
<br>**python3 main.py in-dirs.txt**

<br>For Windows:
<br>**py main.py in-dirs.txt**
<br>or
<br>**python3 main.py in-dirs.txt**

<br>Results will be in a text file, which starts with filedups and contains timestamp of scan.

### Notes
36652 beginning files, 11002 files after filter, size,64-hash,1024-hash TOOK 164 seconds (on USB 2.0, external 5400 rpm hard disk).
