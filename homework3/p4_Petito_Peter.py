"""Homework 3 - Problem 4.

Author: Peter Petito
Course: COP 4045

A non-interactive text editor: functions that read, search, replace and
append text in a utf-8 file. Each function reads the whole file into memory
and, if it changes anything, overwrites the file with the new content.
File I/O errors (e.g. FileNotFoundError) are never caught here; they are
passed to the caller.
"""

import os

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


def _read_all(filename: str) -> str:
    """Return the whole content of filename (utf-8)."""
    with open(filename, encoding="utf-8") as f:
        return f.read()


def _write_all(filename: str, text: str) -> None:
    """Overwrite filename with text (utf-8)."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Return the file content in the half-open range [from_, to).

    param from_: start position (named from_ because 'from' is a Python
        keyword).
    param to: end position, excluded; -1 means the end of the file.
    Precondition: 0 <= from_ <= to <= file length, or to == -1.
    Postcondition: the file is unchanged.
    Raises: IndexError if to exceeds the file length,
        ValueError if from_ is negative or greater than to,
        FileNotFoundError / OSError from the file system.
    """
    text = _read_all(filename)
    if to == -1:
        to = len(text)
    if to > len(text):
        raise IndexError(f"to={to} exceeds the file length {len(text)}")
    if from_ < 0 or from_ > to:
        raise ValueError(f"invalid range [{from_}, {to})")
    return text[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Return the positions in the file where search_str is found.

    Occurrences are counted left to right without overlapping, the same way
    ed_replace() counts them. Returns [] if search_str is not found.
    Precondition: search_str is not empty.
    Postcondition: the file is unchanged.
    Raises: ValueError if search_str is empty,
        FileNotFoundError / OSError from the file system.
    """
    if not search_str:
        raise ValueError("search_str must not be empty")
    text = _read_all(filename)
    positions = []
    pos = text.find(search_str)
    while pos != -1:
        positions.append(pos)
        pos = text.find(search_str, pos + len(search_str))
    return positions


def ed_replace(filename: str, search_str: str, replace_with: str,
               occurrence: int = -1) -> int:
    """Replace search_str with replace_with in the file.

    param occurrence: -1 replaces all occurrences; k >= 0 replaces only
        occurrence number k (0 is the first). If there is no occurrence k,
        nothing is replaced.
    Precondition: search_str is not empty; occurrence >= -1.
    Postcondition: the file holds the new text; it is unchanged if nothing
        was replaced or an error occurred.
    Returns: the number of replacements made.
    Raises: ValueError if a precondition is violated,
        FileNotFoundError / OSError from the file system.
    """
    if occurrence < -1:
        raise ValueError("occurrence must be -1 or >= 0")
    positions = ed_find(filename, search_str)   # also validates search_str
    if occurrence == -1:
        targets = positions
    elif occurrence < len(positions):
        targets = [positions[occurrence]]
    else:
        targets = []
    if not targets:
        return 0

    text = _read_all(filename)
    # replace from the end so earlier positions stay valid
    for pos in reversed(targets):
        text = text[:pos] + replace_with + text[pos + len(search_str):]
    _write_all(filename, text)
    return len(targets)


def ed_append(filename: str, string: str) -> int:
    """Append string to the end of the file, creating the file if needed.

    Postcondition: the file ends with string.
    Returns: the number of characters written.
    Raises: FileNotFoundError / OSError from the file system.
    """
    with open(filename, "a", encoding="utf-8") as f:
        return f.write(string)


def test_ed_find() -> None:
    """Unit tests for ed_find()."""
    fn = "test_find.txt"
    _write_all(fn, "01234567890123456789")
    testif(ed_find(fn, "345") == [3, 13], "ed_find two matches",
           "[3, 13]", str(ed_find(fn, "345")))
    testif(ed_find(fn, "356") == [], "ed_find no match", "[]", "not []")
    testif(ed_find(fn, "0") == [0, 10], "ed_find single char",
           "[0, 10]", "wrong positions")
    _write_all(fn, "aaaa")
    testif(ed_find(fn, "aa") == [0, 2], "ed_find no overlap",
           "[0, 2]", str(ed_find(fn, "aa")))
    try:
        ed_find(fn, "")
        testif(False, "ed_find empty string", "", "no ValueError")
    except ValueError:
        testif(True, "ed_find empty string", "ValueError raised")
    os.remove(fn)


def test_ed_replace() -> None:
    """Unit tests for ed_replace()."""
    fn = "test_replace.txt"
    original = "01234567890123456789"

    _write_all(fn, original)
    n = ed_replace(fn, "345", "ABCDE", 1)
    testif(n == 1 and _read_all(fn) == "0123456789012ABCDE6789",
           "ed_replace one occurrence", "second '345' replaced", "failed")

    _write_all(fn, original)
    n = ed_replace(fn, "345", "ABCDE")
    testif(n == 2 and _read_all(fn) == "012ABCDE6789012ABCDE6789",
           "ed_replace all", "both replaced", "failed")

    _write_all(fn, original)
    n = ed_replace(fn, "345", "ABCDE", 5)
    testif(n == 0 and _read_all(fn) == original,
           "ed_replace occurrence too big", "file unchanged", "failed")

    n = ed_replace(fn, "xyz", "ABC")
    testif(n == 0 and _read_all(fn) == original,
           "ed_replace not found", "file unchanged", "failed")

    try:
        ed_replace(fn, "345", "ABC", -2)
        testif(False, "ed_replace bad occurrence", "", "no ValueError")
    except ValueError:
        testif(_read_all(fn) == original, "ed_replace bad occurrence",
               "ValueError raised, file unchanged", "file changed")
    os.remove(fn)


def main() -> None:
    """Show how the ed_ functions are used, then run the unit tests."""
    print("Peter Petito - FAU ID: Z23712200\n")

    fn = "file1.txt"
    if os.path.exists(fn):   # start fresh, as in the handout example
        os.remove(fn)

    print("ed_append:", ed_append(fn, "0123456789"), "characters written")
    print("ed_append:", ed_append(fn, "0123456789"), "characters written")
    print("file content:", ed_read(fn))
    print("ed_read(fn, 3, 9):", ed_read(fn, 3, 9))
    print("ed_read(fn, 3):", ed_read(fn, 3))
    print("ed_find(fn, '345'):", ed_find(fn, "345"))
    print("ed_find(fn, '356'):", ed_find(fn, "356"))

    n = ed_replace(fn, "345", "ABCDE", 1)
    print(f"ed_replace(fn, '345', 'ABCDE', 1): {n} replaced ->", ed_read(fn))
    ed_replace(fn, "ABCDE", "345")   # reset the content
    n = ed_replace(fn, "345", "ABCDE")
    print(f"ed_replace(fn, '345', 'ABCDE'): {n} replaced ->", ed_read(fn))

    # errors are raised to the caller
    try:
        ed_read(fn, 0, 100)
    except IndexError as e:
        print("ed_read(fn, 0, 100) -> IndexError:", e)
    try:
        ed_read("no_such_file.txt")
    except FileNotFoundError as e:
        print("ed_read('no_such_file.txt') -> FileNotFoundError:", e)
    os.remove(fn)

    print("\nUnit tests:")
    test_ed_find()
    test_ed_replace()


if __name__ == "__main__":
    main()
