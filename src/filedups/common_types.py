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



from typing import Callable
# Callable[[ParamType1, ParamType2, .., ParamTypeN], ReturnType]

from typing import Iterable as Iter
Iter_t = Iter

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

LocationIndices_t = Set[int]
LocationGroups_t = Iter_t[LocationIndices_t]

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


