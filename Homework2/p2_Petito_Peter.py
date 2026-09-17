# Peter Petito - Homework 2
# Problem 2: Comprehensions
def main():
    # a) a,b,c,d distinct in [1,10], a^2+b^2 = c^2+d^2
    result_a = [(a, b, c, d)
                for a in range(1, 11) for b in range(1, 11)
                for c in range(1, 11) for d in range(1, 11)
                if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2]
    print("a)", result_a)

    # b) (lowercase, length) for strings shorter than 5 chars
    words_b = ['One', 'SEVEN', 'three', 'two', 'Ten']
    result_b = [(w.lower(), len(w)) for w in words_b if len(w) < 5]
    print("b)", result_b)

    # c) "Firstname Middlename Lastname" -> "Firstname M. Lastname"
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    result_c = [f"{n.split()[0]} {n.split()[1][0]}. {n.split()[2]}" for n in names]
    print("c)", result_c)

    # d) anagram pairs (case insensitive) between lst1 and lst2
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    result_d = [(w1, w2) for w1 in lst1 for w2 in lst2 if sorted(w1.lower()) == sorted(w2.lower())]
    print("d)", result_d)

    # e) string -> length
    s = ['one', 'two', 'three']
    result_e = {word: len(word) for word in s}
    print("e)", result_e)

    # f) index -> vowel character (case insensitive)
    text = "Hello world"
    result_f = {i: c for i, c in enumerate(text) if c.lower() in 'aeiou'}
    print("f)", result_f)


if __name__ == "__main__":
    main()