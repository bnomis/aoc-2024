import collections
from typing import Self

Point = collections.namedtuple('Point', ['x', 'y'])


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'{self.x},{self.y}'

    def __lt__(self, other: Self) -> bool:
        return self.x < other.x and self.y < other.y

    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y

    def __neq__(self, value: Self) -> bool:
        return self.x != value.x or self.y != value.y

    def __add__(self, value: Self) -> Self:
        return Position(self.x + value.x, self.y + value.y)

    def __sub__(self, value: Self) -> Self:
        return Position(self.x - value.x, self.y - value.y)

    def __mul__(self, value: int) -> Self:
        return Position(self.x * value, self.y * value)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def update(self, value: Self) -> Self:
        self.x += value.x
        self.y += value.y
        return self

    def pos(self) -> tuple:
        return (self.x, self.y)

    def distance(self, value: Self) -> int:
        return abs(self.x - value.x) + abs(self.y - value.y)
