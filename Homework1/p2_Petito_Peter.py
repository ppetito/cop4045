"""Peter Petito
Problem 2: Pythagorean Numbers
Reads a positive integer n from the terminal and finds all Pythagorean triples
(a, b, c) with 0 < a, b, c <= n such that a^2 + b^2 = c^2.
Uses a simple brute force algorithm that tries all possible combinations of
a, b, c in the range 1...n.
"""

def find_pythagorean(n):
    """Finds all pythagorean triples with 0 < a, b, c <= n
    tries every combination of a, b, c from 1 to n and keeps the ones that
    satisfy a^ 2 + b^2 = c^2. This is a brute-force approach.
 
    Args:
        n: A positive integer upper bound for a, b, and c.
 
    Returns:
        A list of tuples (a, b, c) representing Pythagorean triples.
    """

    triples = []

    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a ** 2 + b ** 2 == c ** 2:
                    triples.append((a,b,c))
    return triples

def main():
    """reads n from the terminal and displays all pythagorean triples."""
    n = int(input("Enter a positive integer n: "))

    triples = find_pythagorean(n)

    if triples: 
        print("Pythagorean triples (a, b, c) with a, b, c <=", n, ":")
        for triple in triples:
            print(triple)
    else:
        print("No pythagorean triples found for n=",n)

if __name__ == "__main__":
    main()