#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


class Base:
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.heights = self.make_heights()
        self.max_height = self.height - 2

    def make_heights(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        return ','.join([str(h) for h in self.heights])


class Lock(Base):
    def make_heights(self):
        heights = []
        for _ in range(self.width):
            heights.append(0)
        for row_index in range(1, self.height):
            for column_index, c in enumerate(self.grid[row_index]):
                if c == '#':
                    heights[column_index] += 1
        return heights


class Key(Base):
    def make_heights(self):
        heights = []
        for _ in range(self.width):
            heights.append(0)
        for row_index in range(0, self.height - 1):
            for column_index, c in enumerate(self.grid[row_index]):
                if c == '#':
                    heights[column_index] += 1
        return heights

    def fits(self, lock: Lock) -> bool:
        return all(column + lock.heights[column_index] <= self.max_height for column_index, column in enumerate(self.heights))


def lines_to_locks_and_keys(lines: list[str]) -> tuple[list[Lock], list[Key]]:
    locks = []
    keys = []
    group = []
    for line in lines:
        if not line:
            if group[0][0] == '#':
                locks.append(Lock(group))
            else:
                keys.append(Key(group))
            group = []
        else:
            group.append(line)
    if group[0][0] == '#':
        locks.append(Lock(group))
    else:
        keys.append(Key(group))
    return locks, keys


def part1() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(25, which=0)
    lines = aoc.utils.data.day_input_lines(25)
    locks, keys = lines_to_locks_and_keys(lines)
    matches = 0
    for lo in locks:
        # print(f'lock: {lo}')
        for k in keys:
            # print(f'key: {k}')
            if k.fits(lo):
                matches += 1
    return matches


def part2() -> int:
    return 0


def main() -> None:
    lines = ['25:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
