"""Peter Petito
Problem 4: Function visualization

Defines plot_function(fun_str, domain, ns) which evaluates a user supplied
function expression over an evenly sampled domain, prints a table of x, y values,
and plots the function using matplotlib
"""

import math
import matplotlib.pyplot as plt

def plot_function(fun_str, domain, ns):
    """Computes, tabulates and plots a function given as a string.
    args:
    fun_str: a string with a mathematical expression in variable x,
    for example "2 * x + 3"
    domain: a tuple defining the functions domain
    ns: the number of sample points to use across the domain.
    """

    xmin, xmax = domain
    step = (xmax - xmin) / (ns - 1) if ns>1 else 0

    xs = [xmin + i * step for i in range(ns)]

    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("{:>10s} {:>10s}".format("x", "y"))
    print("-"*21)
    for x, y in zip(xs, ys):
        print("{:>10.4f} {:>+10.4f}".format(x,y))

    plt.figure()
    plt.plot(xs, ys, "bo-")
    plt.title(fun_str)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

def main():
    """Reads function, domain, and sample count from the terminal."""
    fun_str = input("Enter function with variable x: ")
    ns = int(input("Enter number of samples: "))
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))

    plot_function(fun_str, (xmin,xmax), ns)

if __name__ == "__main__":
    main()