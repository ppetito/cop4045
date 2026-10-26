"""Homework 3 - Problem 1.

Author: Peter Petito
Course: COP 4045

NVector: an N-dimensional vector of real numbers stored in a list.
"""

from __future__ import annotations

from typing import Any, Union

Number = Union[int, float]


# testif() from the Homework appendix (provided by the instructor).
def testif(b, testname, msgOK="", msgFailed=""):
    """Function used for testing.
    param b: boolean, normally a tested condition: true if test passed, false otherwise
    param testname: the test name
    param msgOK: string to be printed if param b==True  ( test condition true)
    param msgFailed: string to be printed if param b==False
    returns b
    """
    if b:
        print("Success: "+ testname + "; " + msgOK)
    else:
        print("Failed: "+ testname + "; " + msgFailed)
    return b


def _is_number(x: Any) -> bool:
    """Return True if x is an int or float (not a bool)."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


class NVector:
    """An N-dimensional vector of real numbers, stored in its own list."""

    def __init__(self, *args: Any) -> None:
        """Create a vector from one sequence of numbers or from 2+ numbers.

        Precondition: one argument must be a sequence of numbers; two or
            more arguments must each be a number.
        Postcondition: self holds a new list (never shared with the caller).
        Raises: TypeError if a single argument is not a sequence or any
            element is not a number.
        """
        elems = list(args[0]) if len(args) == 1 else list(args)
        for x in elems:
            if not _is_number(x):
                raise TypeError("elements must be numbers, got " + repr(x))
        self._elems = elems

    @classmethod
    def zeros(cls, n: int) -> NVector:
        """Return a new vector of dimension n with all elements 0.

        Precondition: n is an int >= 0.
        Raises: TypeError if n is not an int, ValueError if n < 0.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("dimension must be an int")
        if n < 0:
            raise ValueError("dimension must be non-negative")
        return cls([0] * n)

    def __len__(self) -> int:
        """Return the dimension of the vector."""
        return len(self._elems)

    def __getitem__(self, index: int) -> Number:
        """Return the element at index (negative indexes work like lists).

        Raises: TypeError if index is not an int, IndexError if out of range.
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")
        return self._elems[index]

    def __setitem__(self, index: int, value: Number) -> None:
        """Set the element at index to value (negative indexes allowed).

        Postcondition: self[index] == value.
        Raises: TypeError if index is not an int or value is not a number,
            IndexError if index is out of range.
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")
        if not _is_number(value):
            raise TypeError("elements must be numbers")
        self._elems[index] = value

    def __str__(self) -> str:
        """Return the vector as a string, e.g. '[3, 0, 1, -1]'."""
        return "[" + ", ".join(str(x) for x in self._elems) + "]"

    def __eq__(self, other: object) -> bool:
        """Return True if other is an NVector with the same elements."""
        if not isinstance(other, NVector):
            return False
        return self._elems == other._elems

    def __ne__(self, other: object) -> bool:
        """Return True if self is not equal to other."""
        return not self == other

    def __add__(self, other: Union[NVector, Number]) -> NVector:
        """Return a new vector: self + other.

        param other: an NVector of the same length (added element-wise)
            or a number (added to every element).
        Postcondition: self and other are unchanged.
        Raises: ValueError if the lengths differ, TypeError for other types.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same length")
            return NVector([a + b for a, b in zip(self._elems, other._elems)])
        if _is_number(other):
            return NVector([a + other for a in self._elems])
        return NotImplemented

    def __radd__(self, other: Number) -> NVector:
        """Return other + self for a number other (e.g. 10 + v)."""
        return self.__add__(other)

    def __mul__(self, other: Union[NVector, Number]) -> Number:
        """Return the scalar product of self and other.

        param other: an NVector B (result is sum of A[i] * B[i]) or a
            number b (result is sum of A[i] * b).
        Postcondition: self and other are unchanged.
        Raises: ValueError if the lengths differ, TypeError for other types.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same length")
            return sum(a * b for a, b in zip(self._elems, other._elems))
        if _is_number(other):
            return sum(a * other for a in self._elems)
        return NotImplemented

    def __rmul__(self, other: Number) -> Number:
        """Return other * self for a number other (e.g. 2 * v)."""
        return self.__mul__(other)


def main() -> None:
    """Test the NVector class."""
    print("Peter Petito - FAU ID: Z23712200")
    # a) constructor with one sequence (copies it, rejects scalars)
    lst = [3, 0, 1, -1]
    v = NVector(lst)
    lst[0] = 100
    testif(v[0] == 3 and len(v) == 4, "constructor(list)",
           "list copied", "list shared or wrong")
    testif(NVector((3, 0, 1, -1)) == v, "constructor(tuple)", "ok", "failed")
    try:
        NVector(5)
        testif(False, "constructor(scalar)", "", "no TypeError")
    except TypeError:
        testif(True, "constructor(scalar)", "TypeError raised")

    # b) constructor with 2+ arguments
    testif(NVector(3, 0, 1, -1) == v, "constructor(*args)", "ok", "failed")

    # c) __len__
    testif(len(NVector(1, 2, 3)) == 3, "__len__", "ok", "failed")

    # d) __getitem__
    testif(v[1] == 0, "__getitem__", "v[1] == 0", "failed")
    testif(v[-2] == 1, "__getitem__ negative", "v[-2] == 1", "failed")
    try:
        v[4]
        testif(False, "__getitem__ out of range", "", "no IndexError")
    except IndexError:
        testif(True, "__getitem__ out of range", "IndexError raised")

    # e) __setitem__
    v = NVector(1, 2, 3, 4)
    v[3] = 10
    testif(v[3] == 10, "__setitem__", "setitem works", "setitem failed")
    v[-4] = 7
    testif(v == NVector(7, 2, 3, 10), "__setitem__ negative", "ok", "failed")

    # f) __str__
    testif(str(NVector(3, 0, 1, -1)) == "[3, 0, 1, -1]", "__str__",
           str(NVector(3, 0, 1, -1)), "wrong string")

    # g) __eq__ and __ne__
    a = NVector(1, 2, 3)
    testif(a == NVector([1, 2, 3]), "__eq__", "equal", "failed")
    testif(not a == [1, 2, 3], "__eq__ non-NVector", "not equal", "failed")
    testif(a != NVector(1, 2, 4), "__ne__", "not equal", "failed")

    # h) __add__ and __radd__
    v = NVector([3, 0, 1, -1])
    testif(v + NVector([1, 2, 3, 4]) == NVector([4, 2, 4, 3]),
           "__add__ NVector", "ok", "failed")
    testif(v + 10 == NVector([13, 10, 11, 9]), "__add__ number", "ok",
           "failed")
    testif(10 + v == NVector([13, 10, 11, 9]), "__radd__", "ok", "failed")
    try:
        v + NVector(1, 2)
        testif(False, "__add__ length mismatch", "", "no ValueError")
    except ValueError:
        testif(True, "__add__ length mismatch", "ValueError raised")

    # i) __mul__ and __rmul__
    testif(v * NVector([1, 2, 3, 4]) == 2, "__mul__ NVector", "ok", "failed")
    testif(v * 2 == 6, "__mul__ number", "ok", "failed")
    testif(2 * v == 6, "__rmul__", "ok", "failed")

    # j) zeros
    testif(NVector.zeros(3) == NVector(0, 0, 0), "zeros", "ok", "failed")


if __name__ == "__main__":
    main()
