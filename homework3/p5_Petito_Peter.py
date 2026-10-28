"""Homework 3 - Problem 5.

Author: Peter Petito
Course: COP 4045

a) Recursive leaf drawings with turtle (straight, plus the curved
   extra-credit version).
b) strB(): recursive base conversion.
c) Cnk_m(): recursive, memoized binomial coefficient (n choose k).
d) make_pairs(): recursive pairing of two lists with an accumulator.
"""

import time
import turtle

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# leaf proportions (relative to the current petiole length)
SIDE_RATIO = 0.42    # side leaflets
TOP_RATIO = 0.75     # the rest of the leaf, above the branch point
SIDE_ANGLE = 45      # degrees between the stem and a side leaflet


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


# ---------------------------------------------------------------- a) Leaf
def _leaf_straight(level: int, length: float) -> None:
    """Recursively draw a straight leaf from the turtle's position.

    Level 0 is a plain line. A higher level draws the petiole, a smaller
    leaf on each side, and a smaller leaf continuing straight up.
    Postcondition: the turtle is back at its starting position and heading.
    """
    turtle.forward(length)
    if level > 0:
        turtle.left(SIDE_ANGLE)
        _leaf_straight(level - 1, length * SIDE_RATIO)
        turtle.right(2 * SIDE_ANGLE)
        _leaf_straight(level - 1, length * SIDE_RATIO)
        turtle.left(SIDE_ANGLE)
        _leaf_straight(level - 1, length * TOP_RATIO)
    turtle.backward(length)


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a straight recursive leaf standing vertically.

    param level: the recursion level (>= 0).
    param length: the length of the lower part of the stem (petiole).
    Precondition: the turtle is at the base point of the leaf.
    Postcondition: the turtle is back at the base point, facing North.
    Raises: ValueError if level < 0 or length <= 0.
    """
    if level < 0 or length <= 0:
        raise ValueError("level must be >= 0 and length > 0")
    turtle.setheading(0)     # East, the default orientation
    turtle.left(90)          # turn left 90 degrees to stand vertically
    _leaf_straight(level, length)


def _leaf_curved(level: int, length: float) -> None:
    """Recursively draw a curved leaf from the turtle's position.

    Like _leaf_straight(), but the side leaflets are uneven and the rest
    of the leaf bends a little at every level, so the leaf curves.
    Postcondition: the turtle is back at its starting position and heading.
    """
    turtle.forward(length)
    if level > 0:
        turtle.left(50)
        _leaf_curved(level - 1, length * 0.4)
        turtle.right(110)
        _leaf_curved(level - 1, length * 0.45)
        turtle.left(72)     # net 12 degrees left: the leaf bends
        _leaf_curved(level - 1, length * 0.75)
        turtle.right(12)
    turtle.backward(length)


def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a curved recursive leaf (extra credit).

    param level: the recursion level (>= 0).
    param length: the length of the lower part of the stem (petiole).
    Precondition: the turtle is at the base point of the leaf.
    Postcondition: the turtle is back at the base point, facing North.
    Raises: ValueError if level < 0 or length <= 0.
    """
    if level < 0 or length <= 0:
        raise ValueError("level must be >= 0 and length > 0")
    turtle.setheading(0)
    turtle.left(90)
    _leaf_curved(level, length)


def move_to(x: float, y: float) -> None:
    """Move the turtle to (x, y) without drawing."""
    turtle.up()
    turtle.goto(x, y)
    turtle.down()


# ------------------------------------------------------- b) Base conversion
def strB(n: int, base: int = 10) -> str:
    """Return the string representation of n in the given base (recursive).

    Digits above 9 are written with the letters 'A'-'Z'.
    Precondition: n is an int >= 0; base is an int with 2 <= base <= 26.
    Raises: ValueError if a precondition is violated.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative int")
    if not isinstance(base, int) or not 2 <= base <= 26:
        raise ValueError("base must be an int between 2 and 26")
    if n < base:                          # base case: a single digit
        return DIGITS[n]
    return strB(n // base, base) + DIGITS[n % base]


def test_strB() -> None:
    """Unit tests for strB()."""
    testif(strB(0) == "0", "strB(0)", "'0'", strB(0))
    testif(strB(100, base=8) == "144", "strB(100, 8)", "'144'",
           strB(100, base=8))
    testif(strB(8191, base=16) == "1FFF", "strB(8191, 16)", "'1FFF'",
           strB(8191, base=16))
    testif(strB(123456789, base=26) == "AA44A1", "strB(123456789, 26)",
           "'AA44A1'", strB(123456789, base=26))


# --------------------------------------------- c) Memoized n choose k
def Cnk_m(n: int, k: int, memo: dict = None) -> int:
    """Return n choose k, recursively, with memoization.

    Uses C(n, k) = C(n-1, k-1) + C(n-1, k), with C(n, 0) = C(n, n) = 1.
    Results already computed are stored in memo, keyed by (n, k), so each
    value is computed only once.
    param memo: the memo dictionary; leave it out (a new one is created).
    Precondition: n and k are ints with 0 <= k <= n.
    Raises: ValueError if a precondition is violated.
    """
    if memo is None:
        if not 0 <= k <= n:
            raise ValueError("need 0 <= k <= n")
        memo = {}
    if k == 0 or k == n:                  # base cases
        return 1
    if (n, k) not in memo:
        memo[(n, k)] = (Cnk_m(n - 1, k - 1, memo)
                        + Cnk_m(n - 1, k, memo))
    return memo[(n, k)]


def test_Cnk_m() -> None:
    """Unit tests for Cnk_m() (values checked with an online calculator)."""
    testif(Cnk_m(5, 0) == 1, "Cnk_m(5, 0)", "1", str(Cnk_m(5, 0)))
    testif(Cnk_m(5, 2) == 10, "Cnk_m(5, 2)", "10", str(Cnk_m(5, 2)))
    testif(Cnk_m(10, 5) == 252, "Cnk_m(10, 5)", "252", str(Cnk_m(10, 5)))
    testif(Cnk_m(40, 20) == 137846528820, "Cnk_m(40, 20)",
           "137846528820", str(Cnk_m(40, 20)))


def run_Cnk() -> None:
    """Print n choose k for some interesting values and the time taken."""
    for n, k in [(10, 3), (20, 10), (52, 5), (100, 50), (300, 150)]:
        start = time.perf_counter()
        result = Cnk_m(n, k)
        elapsed = time.perf_counter() - start
        print(f"C({n}, {k}) = {result}   ({elapsed * 1000:.2f} ms)")


# ------------------------------------------------------- d) Making pairs
def make_pairs(seq1: list, seq2: list, acc: list = None,
               i: int = 0) -> list[tuple]:
    """Return a list of tuples (seq1[i], seq2[i]), recursively.

    Stops at the end of the shorter list. No loops are used; the result is
    built in the accumulator acc.
    param acc: the accumulator; leave it out (a new list is created).
    param i: the current index; leave it out (starts at 0).
    Postcondition: seq1 and seq2 are unchanged.
    """
    if acc is None:
        acc = []
    if i >= len(seq1) or i >= len(seq2):  # base case: a list ran out
        return acc
    acc.append((seq1[i], seq2[i]))
    return make_pairs(seq1, seq2, acc, i + 1)


def test_make_pairs() -> None:
    """Unit tests for make_pairs(), including the boundary cases."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)],
           "make_pairs equal lengths", "ok", "failed")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)],
           "make_pairs seq2 shorter", "ok", "failed")
    testif(make_pairs([1], [4, 5, 6, 7]) == [(1, 4)],
           "make_pairs seq1 shorter", "ok", "failed")
    testif(make_pairs([], [4, 5, 6]) == [], "make_pairs seq1 empty",
           "[]", "failed")
    testif(make_pairs([1, 2, 3], []) == [], "make_pairs seq2 empty",
           "[]", "failed")


def main() -> None:
    """Run the unit tests and examples, then draw both leaves."""
    print("Peter Petito - FAU ID: Z23712200\n")

    print("b) strB unit tests:")
    test_strB()
    print("\nc) Cnk_m unit tests:")
    test_Cnk_m()
    print("\nrun_Cnk():")
    run_Cnk()
    print("\nd) make_pairs unit tests:")
    test_make_pairs()
    print("make_pairs([1, 2, 3], [4, 5, 6, 7, 8, 9]) ->",
          make_pairs([1, 2, 3], [4, 5, 6, 7, 8, 9]))

    print("\na) Drawing the leaves... (click the window to close it)")
    turtle.setup(1000, 750)
    turtle.title("draw_leaf_straight(6, 120)  |  draw_leaf_curved(6, 120)")
    turtle.hideturtle()
    turtle.delay(0)
    turtle.tracer(0)              # draw instantly, show at update()
    move_to(-250, -330)
    draw_leaf_straight(6, 120)
    move_to(170, -330)
    draw_leaf_curved(6, 120)
    turtle.update()
    turtle.exitonclick()


if __name__ == "__main__":
    main()
