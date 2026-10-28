"""Homework 3 - Problem 2.

Author: Peter Petito
Course: COP 4045

University parking permits: a ParkingPermit base class with StudentPermit
and FacultyPermit subclasses. All costs come from a fee schedule dictionary.
"""

from __future__ import annotations


class ParkingPermit:
    """A parking permit with an owner, a number of months and a fee schedule.

    The fee schedule maps fee names to dollar amounts. Every schedule must
    have a "monthly" key; subclasses may require more keys.
    """

    def __init__(self, owner: str, months: int,
                 fee_schedule: dict[str, float]) -> None:
        """Create a permit.

        Precondition: months >= 1; fee_schedule has a "monthly" key.
        Postcondition: the permit stores its own copy of fee_schedule.
        Raises: ValueError if months < 1, KeyError if "monthly" is missing.
        """
        if months < 1:
            raise ValueError("months must be at least 1")
        if "monthly" not in fee_schedule:
            raise KeyError("fee schedule needs a 'monthly' fee")
        self.owner = owner
        self.months = months
        self.fee_schedule = dict(fee_schedule)

    def cost(self) -> float:
        """Return the base cost: months times the monthly fee."""
        return self.months * self.fee_schedule["monthly"]

    def __str__(self) -> str:
        """Return a readable description, e.g. 'Ann: 3 months, $75.00'."""
        return f"{self.owner}: {self.months} months, ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Return a string that recreates the permit."""
        return (f"{type(self).__name__}({self.owner!r}, {self.months!r}, "
                f"{self.fee_schedule!r})")


class StudentPermit(ParkingPermit):
    """A student permit that also stores the number of vehicles registered.

    Fee schedule keys: "monthly" and "extra_vehicle" (one-time fee for each
    vehicle after the first).
    """

    def __init__(self, owner: str, months: int,
                 fee_schedule: dict[str, float], vehicles: int) -> None:
        """Create a student permit.

        Precondition: vehicles >= 1; fee_schedule also has "extra_vehicle".
        Raises: ValueError if vehicles < 1, KeyError if a fee is missing.
        """
        super().__init__(owner, months, fee_schedule)
        if vehicles < 1:
            raise ValueError("vehicles must be at least 1")
        if "extra_vehicle" not in fee_schedule:
            raise KeyError("fee schedule needs an 'extra_vehicle' fee")
        self.vehicles = vehicles

    def cost(self) -> float:
        """Return the monthly cost plus the fee for each extra vehicle."""
        extra = (self.vehicles - 1) * self.fee_schedule["extra_vehicle"]
        return super().cost() + extra

    def __str__(self) -> str:
        """Return a readable description of the student permit."""
        return (f"Student permit - {self.owner}: {self.months} months, "
                f"{self.vehicles} vehicle(s), ${self.cost():.2f}")

    def __repr__(self) -> str:
        """Return a string that recreates the student permit."""
        return (f"StudentPermit({self.owner!r}, {self.months!r}, "
                f"{self.fee_schedule!r}, {self.vehicles!r})")


class FacultyPermit(ParkingPermit):
    """A faculty permit that also stores whether garage access is included.

    Fee schedule keys: "monthly" and "garage_monthly" (extra per month with
    garage access).
    """

    def __init__(self, owner: str, months: int,
                 fee_schedule: dict[str, float], garage: bool) -> None:
        """Create a faculty permit.

        Precondition: fee_schedule also has "garage_monthly".
        Raises: KeyError if a fee is missing.
        """
        super().__init__(owner, months, fee_schedule)
        if "garage_monthly" not in fee_schedule:
            raise KeyError("fee schedule needs a 'garage_monthly' fee")
        self.garage = garage

    def cost(self) -> float:
        """Return the monthly cost plus the garage fee, if included."""
        garage_fee = self.fee_schedule["garage_monthly"] if self.garage else 0
        return super().cost() + self.months * garage_fee

    def __str__(self) -> str:
        """Return a readable description of the faculty permit."""
        access = "with" if self.garage else "no"
        return (f"Faculty permit - {self.owner}: {self.months} months, "
                f"{access} garage, ${self.cost():.2f}")

    def __repr__(self) -> str:
        """Return a string that recreates the faculty permit."""
        return (f"FacultyPermit({self.owner!r}, {self.months!r}, "
                f"{self.fee_schedule!r}, {self.garage!r})")


def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each permit's owner and cost, then return the total revenue.

    param permits: a list of permits of any type (mixed is fine).
    Postcondition: the permits are unchanged.
    """
    total = 0.0
    for permit in permits:
        print(permit)
        total += permit.cost()
    return total


def main() -> None:
    """Show how the permit classes and summarize_list() are used."""
    print("Peter Petito - FAU ID: Z23712200")

    student_fees = {"monthly": 25, "extra_vehicle": 10}
    faculty_fees = {"monthly": 40, "garage_monthly": 15}

    permits = [
        StudentPermit("Alice", 4, student_fees, 1),
        StudentPermit("Ben", 6, student_fees, 3),
        FacultyPermit("Dr. Cruz", 12, faculty_fees, True),
        FacultyPermit("Dr. Diaz", 3, faculty_fees, False),
    ]

    print("\nPermit objects (repr):")
    for permit in permits:
        print(repr(permit))

    print("\nSummary:")
    total = summarize_list(permits)
    print(f"\nTotal revenue: ${total:.2f}")


if __name__ == "__main__":
    main()
