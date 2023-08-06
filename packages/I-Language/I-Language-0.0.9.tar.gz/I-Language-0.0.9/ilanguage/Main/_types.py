"""
I Language types.
Version: 0.1.2

Copyright (c) 2023-present I Language Development.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the 'Software'),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

##########
# LINTER #
##########

# pylint: disable=R0903


###########
# IMPORTS #
###########

import ast
import builtins
from typing import (
    List as _List,
    Optional,
)

from typing_extensions import (
    Any as _Any,
    Self,
    Type,
)


#############
# BASE TYPE #
#############


class BaseType:
    """
    Represents a base type object.
    """

    types: _List[Self] = []

    def __init__(self, value: str, python_type: Optional[Type]) -> None:
        """Initializes a new type.

        Args:
            value (str): Value of the type.
            python_type (Optional[Type]): Python base type representing this type.
        """

        self.value = value
        self.python_type = python_type

        self.validate()

    def validate(self) -> None:
        """
        Validates the value with the type.
        """

        if self.python_type is not None:
            self.python_type(ast.literal_eval(self.value))


#########
# TYPES #
#########


class Any(BaseType):
    """
    Dynamic type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a dynamic type.

        :param value: Value of the object to check for dynamic value.
        """

        super().__init__(value, _Any)


class Bool(BaseType):
    """
    Bool type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a bool type.

        :param value: Value of the object to check for boolean value.
        """

        super().__init__(value, builtins.bool)


class Complex(BaseType):
    """
    Complex integer type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a complex type.

        :param value: Value of the object to check for complex value.
        """

        super().__init__(value, builtins.complex)


class Dict(BaseType):
    """
    Dictionary type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a dictionary type.

        :param value: Value of the object to check for dictionary value.
        """

        super().__init__(value, builtins.dict)


class Dictionary(Dict):
    """
    Dictionary type.
    """


class Dynamic(Any):
    """
    Dynamic type.
    """


class Float(BaseType):
    """
    Float type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a float type.

        :param value: Value of the object to check for float value.
        """

        super().__init__(value, builtins.float)


class Int(BaseType):
    """
    Integer type.
    """

    def __init__(self, value: str) -> None:
        """Initializes an integer type.

        :param value: Value of the object to check for integer value.
        """

        super().__init__(value, builtins.int)


class Integer(Int):
    """
    Integer type.
    """


class List(BaseType):
    """
    List type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a list type.

        :param value: Value of the object to check for list value.
        """

        super().__init__(value, builtins.list)


class Null(BaseType):
    """
    None type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a none type.

        :param value: Value of the object to check for none value.
        """

        super().__init__(value, None)


class Str(BaseType):
    """
    String type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a string type.

        :param value: Value of the object to check for string value.
        """

        super().__init__(value, builtins.str)


class String(Str):
    """
    String type.
    """


class mdarray(BaseType):
    """
    Multi-dimensional array type.
    """

    def __init__(self, value: str) -> None:
        """Initializes a multidimensional array type.

        Args:
            value (mdarray): Value of the object to check for multidimensional array value.
        """

        super().__init__(value, _Any)  # TODO (ElBe): Add python type
