# FIND FILE DUPLICATES
**WARNING: THIS PROJECT IS IN PROGRESS. DO NOT DEPEND ON ANY FUNCTION/CLASS/MODULE**
Given a sequence of paths (directory or file), finds and groups duplicate files recursively.
Doesn't provide 100% accuracy. Reported files in a group might be different.
Processing speed = near 300 files/second for a cold search on hard disk.

## HOW TO USE
Current (2021-12-26) use is not as pleasant as it can be. It will be improved.  
Put paths in a list and assign it to **search_paths** variable in **main.py** under if __name__ == "__main__":  
Then, from the console,  
**python3 main.py**