"""Reproduce the fictional case study's arithmetic; no external dependencies."""
from fractions import Fraction


def compare(before_count, before_minutes, after_count, after_minutes):
    if before_count <= 0 or after_count <= 0 or before_minutes <= 0 or after_minutes < 0:
        raise ValueError("Counts and baseline minutes must be positive; pilot minutes nonnegative")
    before = Fraction(before_minutes, before_count)
    after = Fraction(after_minutes, after_count)
    reduction = (before - after) / before
    return before, after, reduction


if __name__ == "__main__":
    before, after, reduction = compare(120, 5400, 120, 2160)
    assert (before, after, reduction) == (45, 18, Fraction(3, 5))
    assert Fraction(5400 - 2160, 60) == 54
    assert compare(120, 5400, 60, 1080) == (before, after, reduction)
    print("PASS: 45 -> 18 min/quote; 60% lower average; 54-hour equal-volume batch difference.")
    print("PASS: unequal batch volumes preserve the per-quote comparison.")
