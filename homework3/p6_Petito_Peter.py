"""Homework 3 - Problem 6.

Author: Peter Petito
Course: COP 4045

Estimate the storage used by a hierarchy of folders and files.

a) Entry base class and File(Entry) with a nonnegative bytes_used.
b) Folder(Entry) with add(), children() and a recursive size().
c) Entry.absolute_path(): recursive path from an entry up to the root.
d) find_large_files(): recursive search for files at or above a size.
e) Unit tests for find_large_files() and absolute_path().
f) main(): one size() call on a nested hierarchy, and find_large_files()
   at two thresholds.
g) main(): absolute_path() for a deeply nested file.
"""

from __future__ import annotations

import unittest


class Entry:
    """Abstract base for a File or Folder; subclasses override size().

    An entry starts with no parent and gets one when added to a Folder.
    """

    def __init__(self, name: str) -> None:
        """Create a parentless entry with the given name."""
        self.name = name
        self._parent: Folder | None = None

    def parent(self) -> Folder | None:
        """Return the containing Folder, or None if this entry is a root."""
        return self._parent

    def size(self) -> int:
        """Return the bytes used by this entry.

        Raises:
            NotImplementedError: Always; subclasses must override this.
        """
        raise NotImplementedError(f"{type(self).__name__} must override size()")

    def absolute_path(self) -> list[Entry]:
        """Return the path from this entry up to the root, recursively.

        Precondition: the hierarchy has no cycles.

        Returns:
            A new list starting with self and ending with the root, where
            each element is the parent of the one before it.
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def __repr__(self) -> str:
        """Return a short description such as File('a.txt')."""
        return f"{type(self).__name__}({self.name!r})"


class File(Entry):
    """A file that uses a fixed, nonnegative number of bytes."""

    def __init__(self, name: str, bytes_used: int) -> None:
        """Create a parentless file.

        Raises:
            TypeError: If bytes_used is not an int.
            ValueError: If bytes_used is negative.
        """
        super().__init__(name)
        if not isinstance(bytes_used, int) or isinstance(bytes_used, bool):
            raise TypeError("bytes_used must be an int")
        if bytes_used < 0:
            raise ValueError(f"bytes_used must be >= 0, got {bytes_used}")
        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return bytes_used."""
        return self.bytes_used


class Folder(Entry):
    """A folder containing files and other folders."""

    def __init__(self, name: str) -> None:
        """Create an empty, parentless folder."""
        super().__init__(name)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add entry as the last child of this folder and set its parent.

        Postcondition: entry.parent() is self.

        Raises:
            TypeError: If entry is not an Entry.
            ValueError: If entry already has a parent or would form a cycle.
        """
        if not isinstance(entry, Entry):
            raise TypeError(f"cannot add a {type(entry).__name__}")
        if entry.parent() is not None:
            raise ValueError(f"{entry!r} already belongs to {entry.parent()!r}")
        if entry in self.absolute_path():
            raise ValueError(f"adding {entry!r} to {self!r} would form a cycle")
        self._children.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return the child entries, in the order they were added."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of all children, including nested folders."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return all files at or below entry with size() >= minimum_size.

    If entry is a File (base case), return [entry] if it is large enough,
    otherwise []. If entry is a Folder, recurse into each child and join
    the results in depth-first order; folders themselves are never
    returned, and an empty folder gives []. The hierarchy is not modified.

    Raises:
        TypeError: If entry is not a File or Folder, or minimum_size is
            not an int.
        ValueError: If minimum_size is negative.
    """
    if not isinstance(minimum_size, int) or isinstance(minimum_size, bool):
        raise TypeError("minimum_size must be an int")
    if minimum_size < 0:
        raise ValueError(f"minimum_size must be >= 0, got {minimum_size}")
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    if isinstance(entry, Folder):
        large_files: list[File] = []
        for child in entry.children():
            large_files += find_large_files(child, minimum_size)
        return large_files
    raise TypeError(f"entry must be a File or Folder, "
                    f"not {type(entry).__name__}")


class _SampleTree(unittest.TestCase):
    """Builds root/{top.txt, empty/, a/{a.txt, b/c/deep.bin}} for each test."""

    def setUp(self) -> None:
        """Create a fresh sample tree."""
        self.root, self.empty = Folder("root"), Folder("empty")
        self.a, self.b, self.c = Folder("a"), Folder("b"), Folder("c")
        self.top = File("top.txt", 500)
        self.a_txt = File("a.txt", 2_000)
        self.deep = File("deep.bin", 50_000)
        for parent, child in [(self.root, self.top), (self.root, self.empty),
                              (self.root, self.a), (self.a, self.a_txt),
                              (self.a, self.b), (self.b, self.c),
                              (self.c, self.deep)]:
            parent.add(child)


class TestFindLargeFiles(_SampleTree):
    """Tests for find_large_files()."""

    def test_single_file_above_threshold(self) -> None:
        """A file at or above the threshold is returned alone."""
        f = File("f", 1_000)
        self.assertEqual(find_large_files(f, 999), [f])
        self.assertEqual(find_large_files(f, 1_000), [f])

    def test_single_file_below_threshold(self) -> None:
        """A file below the threshold gives []."""
        self.assertEqual(find_large_files(File("f", 1_000), 1_001), [])

    def test_nested_folders(self) -> None:
        """Files deep inside nested folders are found."""
        self.assertEqual(find_large_files(self.root, 1_000),
                         [self.a_txt, self.deep])
        self.assertEqual(find_large_files(self.root, 10_000), [self.deep])

    def test_empty_folder(self) -> None:
        """An empty folder gives []."""
        self.assertEqual(find_large_files(self.empty, 0), [])

    def test_threshold_zero_returns_all_files(self) -> None:
        """A threshold of 0 returns every file, in depth-first order."""
        self.assertEqual(find_large_files(self.root, 0),
                         [self.top, self.a_txt, self.deep])

    def test_invalid_arguments(self) -> None:
        """Bad arguments raise the documented errors."""
        with self.assertRaises(ValueError):
            find_large_files(self.root, -1)
        with self.assertRaises(TypeError):
            find_large_files(self.root, 1.5)
        with self.assertRaises(TypeError):
            find_large_files("root", 0)


class TestAbsolutePath(_SampleTree):
    """Tests for Entry.absolute_path()."""

    def test_root_path(self) -> None:
        """A root's path contains only the root."""
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_deeply_nested_file_path(self) -> None:
        """A deep file's path runs from the file up to the root."""
        path = self.deep.absolute_path()
        expected = [self.deep, self.c, self.b, self.a, self.root]
        self.assertEqual(len(path), len(expected))
        for actual, entry in zip(path, expected):
            self.assertIs(actual, entry)

    def test_folder_path(self) -> None:
        """A folder's path works the same way as a file's."""
        self.assertEqual(self.b.absolute_path(), [self.b, self.a, self.root])

    def test_path_updates_after_add(self) -> None:
        """A parentless file is its own root until it is added to a folder."""
        f = File("new.txt", 1)
        self.assertEqual(f.absolute_path(), [f])
        self.empty.add(f)
        self.assertEqual(f.absolute_path(), [f, self.empty, self.root])


def main() -> None:
    """Demonstrate size(), find_large_files() and absolute_path(), then
    run the unit tests without exiting."""
    print("Peter Petito - FAU ID: Z23712200")

    # university/cs/cop4045/hw3: four levels, with files at every level.
    university, cs = Folder("university"), Folder("cs")
    cop4045, hw3 = Folder("cop4045"), Folder("hw3")
    data = File("data.csv", 150_000)
    for parent, child in [
            (university, File("syllabus.pdf", 1_200)), (university, cs),
            (cs, File("intro.py", 4_000)), (cs, File("lecture.mp4", 2_500_000)),
            (cs, cop4045), (cop4045, File("notes.txt", 3_000)),
            (cop4045, hw3), (hw3, File("p6.py", 9_000)), (hw3, data)]:
        parent.add(child)

    print(f"\nf) university.size() = {university.size():,} bytes")
    print("   The same size() call on each child (File or Folder):")
    for child in university.children():
        print(f"     {child!r:<22} size() = {child.size():>10,}")
    for threshold in (10_000, 1_000_000):
        names = [f.name for f in find_large_files(university, threshold)]
        print(f"   find_large_files(university, {threshold:,}) -> {names}")

    path = data.absolute_path()
    print("\ng) data.absolute_path() ->", [e.name for e in path])
    print("   As a path:", "/".join(e.name for e in reversed(path)))

    print("\ne) Unit tests:", flush=True)  # flush: unittest writes to stderr
    unittest.main(argv=[""], exit=False, verbosity=2)


if __name__ == "__main__":
    main()
