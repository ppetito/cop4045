# Copyright 2017, 2013, 2011 Pearson Education, Inc., W.F. Punch & R.J.Enbody
# Modified by Peter Petito for COP 4045 Homework 3, Problem 3: added humans.
"""Homework 3 - Problem 3: Predator-Prey simulation with humans.

Author: Peter Petito
Course: COP 4045

Five classes are defined: Animal, Prey, Predator, Human and Island.
The Island is an n x n grid where the animals live. Prey breed; Predators
eat Prey, breed and starve; Humans eat Predators (not Prey), breed and
starve. The simulation runs until all three populations stay constant or
for at most MAX_TICKS clock ticks, then plots the populations over time.
"""

from __future__ import annotations

import random
from typing import Union

import matplotlib.pyplot as plt

MAX_TICKS = 1000    # maximum length of the simulation
STABLE_TICKS = 20   # populations unchanged this long are considered converged

Location = Union[tuple[int, int], int]   # (x, y) or 0 when nothing found


class Island:
    """An n x n grid where a 0 value means the cell is not occupied."""

    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0,
                 human_count: int = 0) -> None:
        """Create an empty n x n grid, then fill it with animals.

        Precondition: prey_count + predator_count + human_count <= n * n.
        """
        self.grid_size = n
        self.grid: list[list] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, human_count)

    def init_animals(self, prey_count: int, predator_count: int,
                     human_count: int) -> None:
        """Put the initial animals at random unoccupied positions.

        Raises: ValueError if there are more animals than grid cells.
        """
        if prey_count + predator_count + human_count > self.grid_size ** 2:
            raise ValueError("too many animals for the island")
        self._place_animals(Prey, prey_count)
        self._place_animals(Predator, predator_count)
        self._place_animals(Human, human_count)

    def _place_animals(self, animal_class: type, count: int) -> None:
        """Create count animals of animal_class at random free positions."""
        placed = 0
        while placed < count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.animal(x, y):
                self.register(animal_class(island=self, x=x, y=y))
                placed += 1

    def clear_all_moved_flags(self) -> None:
        """Clear every animal's moved flag so the next turn can start."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return the size of the island (one dimension)."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Put animal on the grid at its own coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove animal from the grid."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Union[Animal, int]:
        """Return the animal at (x, y), 0 if empty, -1 if off the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Return the grid as text, with (0, 0) in the lower left corner."""
        s = ""
        for j in range(self.grid_size - 1, -1, -1):   # top row first
            for i in range(self.grid_size):
                cell = self.grid[i][j]
                s += "{:<3s}".format(str(cell) if cell else ".")
            s += "\n"
        return s

    def _count(self, animal_class: type) -> int:
        """Return the number of animals of animal_class on the grid."""
        return sum(isinstance(cell, animal_class)
                   for row in self.grid for cell in row)

    def count_prey(self) -> int:
        """Return the number of Prey on the island."""
        return self._count(Prey)

    def count_predators(self) -> int:
        """Return the number of Predators on the island."""
        return self._count(Predator)

    def count_humans(self) -> int:
        """Return the number of Humans on the island."""
        return self._count(Human)


class Animal:
    """An animal that lives on an Island, moves and breeds.

    Subclasses must define the class attribute breed_time.
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """Create an animal at (x, y) on island, printed as s."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple[int, int]:
        """Return the coordinates of the current position."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the one-letter name used on the grid."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> Location:
        """Return the first of the 8 neighboring locations holding an object
        of exactly type_looking_for (int means empty), or 0 if none does.
        """
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0),
                  (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offset:
            x = self.x + dx
            y = self.y + dy
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                return (x, y)
        return 0

    def move_to(self, location: tuple[int, int]) -> None:
        """Move to location and mark this animal as moved.

        Precondition: location is on the island and empty (or its occupant
            has just been removed).
        """
        self.island.remove(self)
        self.x, self.y = location
        self.island.register(self)
        self.moved = True

    def move(self) -> None:
        """Move to an open neighboring position, if not moved this turn."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.move_to(location)

    def eat(self) -> None:
        """Do nothing by default; animals that hunt override this."""

    def hunt(self, target_class: type) -> bool:
        """Eat a neighboring animal of type target_class, if there is one.

        Postcondition: if a target was found, it is removed from the island
            and this animal has moved into its cell.
        Returns: True if a target was eaten, False otherwise.
        """
        if self.moved:
            return False
        location = self.check_grid(target_class)
        if not location:
            return False
        self.island.remove(self.island.animal(*location))
        self.move_to(location)
        return True

    def breed(self) -> None:
        """Breed a new animal of the same class in an open neighboring
        position, if the breed clock has run out. Otherwise wait.
        """
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0],
                                            y=location[1])
                self.island.register(new_animal)

    def clock_tick(self) -> None:
        """Advance the breed clock by one tick."""
        self.breed_clock -= 1

    def clear_moved_flag(self) -> None:
        """Reset the moved flag for a new turn."""
        self.moved = False


class Prey(Animal):
    """Prey only move and breed. Printed as 'O'."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """Create a Prey at (x, y) with a full breed clock."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time


class Predator(Animal):
    """Predators eat Prey, breed, and starve if they don't eat in time.

    Printed as 'X'. Class attributes breed_time and starve_time are set
    in main().
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """Create a Predator at (x, y) with full breed and starve clocks."""
        super().__init__(island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Advance the breed and starve clocks; remove if starved."""
        super().clock_tick()
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat a neighboring Prey, if there is one, and reset starving."""
        if self.hunt(Prey):
            self.starve_clock = self.starve_time


class Human(Animal):
    """Humans eat Predators (never Prey), breed, and starve.

    Printed as 'H'. Class attributes breed_time, starve_time and hunt_time
    are set in main(). A Human only tries to hunt once every hunt_time
    ticks, counted from its creation.
    """

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """Create a Human at (x, y) with full breed, starve and hunt clocks."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        """Advance the breed, starve and hunt clocks; remove if starved."""
        super().clock_tick()
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Every hunt_time ticks, eat a neighboring Predator if there is one.

        Postcondition: when it is time to hunt, the hunt clock restarts;
            if a Predator was eaten, the starve clock restarts too.
        """
        if self.hunt_clock <= 0 and not self.moved:
            self.hunt_clock = self.hunt_time
            if self.hunt(Predator):
                self.starve_clock = self.starve_time


###########################################
def main(predator_breed_time: int = 8, predator_starve_time: int = 4,
         initial_predators: int = 40, prey_breed_time: int = 3,
         initial_prey: int = 200, human_breed_time: int = 20,
         human_starve_time: int = 15, human_hunt_time: int = 4,
         initial_humans: int = 5, size: int = 20,
         ticks: int = MAX_TICKS) -> None:
    """Run the simulation, print the island and statistics, then plot.

    The simulation stops when the Prey, Predator and Human populations have
    all stayed the same for STABLE_TICKS ticks, or after ticks ticks.
    """
    print("Peter Petito - FAU ID: Z23712200\n")

    # class attributes shared by all animals of each type
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    # population history, for graphing
    prey_list: list[int] = []
    predator_list: list[int] = []
    human_list: list[int] = []

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print("Island at the start:")
    print(isle)
    print("tick  prey  predators  humans")

    stable = 0   # number of ticks in a row with no population change
    tick = 0
    for tick in range(min(ticks, MAX_TICKS)):
        isle.clear_all_moved_flags()
        # every animal tries to eat, move, breed, then its clocks advance
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        counts = (isle.count_prey(), isle.count_predators(),
                  isle.count_humans())
        if prey_list and counts == (prey_list[-1], predator_list[-1],
                                    human_list[-1]):
            stable += 1
        else:
            stable = 0
        prey_list.append(counts[0])
        predator_list.append(counts[1])
        human_list.append(counts[2])

        if tick % 10 == 0:
            print("{:>4d}  {:>4d}  {:>9d}  {:>6d}".format(tick, *counts))
        if stable >= STABLE_TICKS:
            print(f"\nPopulations converged after {tick + 1} ticks.")
            break
    else:
        print(f"\nStopped after the maximum of {tick + 1} ticks.")

    print("Island at the end:")
    print(isle)
    print(f"Final populations - prey: {prey_list[-1]}, "
          f"predators: {predator_list[-1]}, humans: {human_list[-1]}")
    print(f"Peak populations  - prey: {max(prey_list)}, "
          f"predators: {max(predator_list)}, humans: {max(human_list)}")

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.title("Island populations over time")
    plt.xlabel("Time (clock ticks)")
    plt.ylabel("Population")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
