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



from typing import Callable
# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from typing import Iterable as Iter


from typing import Sequence

from typing import Any
from typing import AnyStr
from typing import Dict
from typing import Set
from typing import List
from typing import Tuple
from typing import Sized

from typing import TypeVar
# from typing import Optional

# from typing import TypeAlias  # "from typing_extensions" in Python 3.9 and earlier

Str = str

LocationIndices = Set[int]
LocationGroups = Iter[LocationIndices]

# Iterable_t = Iter_t

Maybe = Tuple[bool, Any]
MaybeInt = Tuple[bool, int]

def make_some(data: Any) -> Maybe:
    return (True, data)
#


def make_nothing() -> Maybe:
    return (False, False) # Second field is unimportant
#


def is_some(arg: Maybe) -> bool:
    return arg[0] == True
#


def is_nothing(arg: Maybe) -> bool:
    return arg[0]  == False
#


def get_data(arg: Maybe) -> Any:
    return arg[1]
#


