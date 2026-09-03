"""Peter Petito
Problem 3: Duplicated substrings

part a) find_dup_str(s, n) determines whether string s contains a duplicated substring of length
n and returns the first such substring found, or the empty string if none are found. Uses
string slicing only, no str.find/ str.index or any built in search functions.

part b) find_max_dup(s) finds the longest duplicated substring in s by calling
find_dup_str(s, n) with decreasing values of n.
"""

def find_dup_str(s, n):
    """Finds the first substring of length n that is duplicated in s.
    Scans s from left to right. for each starting position i, takes the substring s and checks,
    using string slicing, whether that same substring occurs again later in s without overlapping
    the first occurence. Returns the first such duplicated substring found.
    
    args:
    s: the string to search
    n: the length of the substring to look for
    
    returns:
    the first occuring substring of length n that is duplicated in s or the empty string if none exists"""

    if n<= 0 or n>len(s) // 2:
        return ""

    for i in range(len(s) - n + 1):
        candidate = s[i:i + n]
        for j in range( i + n, len(s) - n + 1):
            if s[j:j + n] == candidate:
                return candidate
    return ""

def find_max_dup(s):
    """Finds the longest substring that is duplicated in s.
    calls find_dup_str(s,n) starting from the largest possible length down to 1, and 
    returns the first duplicated substring found.
    
    args:
    s: the string to search
    
    returns:
    the longest duplicated substring in s, or the empty string if s has no duplicated substrings.
    """
    for n in range(len(s) // 2, 0, -1):
        result = find_dup_str(s,n)
        if result != "":
            return result

    return ""

def main():
    "Reads test input from the terminal and prints results"
    s = input("Enter a string: ")
    n = int(input("Enter a substring length n: "))
    print("find_dup_str result:", repr(find_dup_str(s,n)))

    s2 = input("Enter a string: ")
    print("find_max_dup result:", repr(find_max_dup(s2)))

if __name__ == "__main__":
    main()