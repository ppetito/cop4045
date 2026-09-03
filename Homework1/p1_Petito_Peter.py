"""Peter Petito
Problem 1: Quadratic equations

Reads coefficients a, b, c from the terminal in an infinite loop, solves the quadratic
equation a*x^2 + b*x + c = 0, print the real solutions to the terminal, and visualizes 
the corresponding quadratic function y = a*x^2 + b*x + c using matplotlib.
The loop ends when the user presses enter instead of typing a value for 'a'. 
"""
import matplotlib.pyplot as plt
import numpy as np

NUM_POINTS = 150
MARGIN = 2.0
NO_ROOT_HALF_WIDTH = 5.0

def solve_quadratic(a, b, c):
    """Solves a quadratic equation
    args: a, coefficient of x^2
          b, coefficient of x
          c, constant
    
    returns: a tuple where roots is an empty tuple if there are
    no real solutions, a 1-tuple if there is exactly one real solution,
    or a 2-tuple if there are two.
    """
    discriminant = b ** 2-4 * a * c
    if discriminant < 0:
        return discriminant, ()
    elif discriminant == 0:
        x1 = -b / (2 * a)
        return discriminant, (x1,)
    else:
        sqrt_disc = discriminant ** .5
        x1 = (-b + sqrt_disc) / (2 * a)
        x2 = (-b - sqrt_disc) / (2 * a)
        return discriminant, (x1, x2)

def get_plot_domain(a, b, roots):
    """Chooses an x axis domain for plotting the function.
    If there are real roots, the domain is centered around them with a margin on each
    side so the roots are clearly visible on the chart. If there are no real roots, the
    domain is centered on the functions vertex x_opt = -b / (2*a).

    args: a, coefficient of x^2
          b, coefficient of x
          roots, tuple of real roots. 0, 1 or 2 elements.

    returns: a tuple (x_min, x_max).
    """
    if roots:
        x_min = min(roots) - MARGIN
        x_max = max(roots) + MARGIN
    else: 
        x_opt = -b / (2 *a)
        x_min = x_opt - NO_ROOT_HALF_WIDTH
        x_max = x_opt + NO_ROOT_HALF_WIDTH

    return x_min, x_max

def plot_quadratic(a, b, c, roots):
    """Plots y = a*x^2 + b*x + c using matplotlib
    
    args:
    a, coefficient of x^2
    b, coefficient of x
    c, constant 
    roots, tuple of real roots, used to pick a domain the keeps the roots 
    visible on the chart.
    """
    x_min, x_max = get_plot_domain(a, b, roots)
    x_values = np.linspace(x_min, x_max, NUM_POINTS)
    y_values = a * x_values ** 2 + b * x_values + c

    plt.figure()
    plt.plot(x_values, y_values, "b.")
    plt.axhline(0, color="black", linewidth=.5)
    plt.title("y = {}x^2 + {}x + {}".format(a,b,c))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid = True
    plt.show()

def main():
    """Runs the main input/solve/plot loop until user presses enter. """
    while True:
        a_input = input("Enter a: ")
        if a_input == "":
            break
        b_input = input("Enter b: ")
        c_input = input("Enter c: ")

        a = float(a_input)
        b = float(b_input)
        c = float(c_input)

        discriminant, roots = solve_quadratic(a, b, c)

        if discriminant < 0:
            print("No real solutions")
        elif discriminant == 0:
            print("One solution: {:.5f}".format(roots[0]))
        else:
            print("Two solutions: x1={:.5f} x2={:.5f}".format(roots[0], roots[1]))

        plot_quadratic(a, b, c, roots)

        print()


if __name__ == "__main__":
    main()