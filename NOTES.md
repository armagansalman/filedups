+ Bugs in Python:
    + When sending paths to search in the beginning, if the data type is
    str, the code (2021-12-16) makes every char of the PATH an element
    of a set. Expected behv. = Add that path to the set, not its chars.
