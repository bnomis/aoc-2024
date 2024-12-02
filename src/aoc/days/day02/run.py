#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


def increasing(data: list[int]) -> bool:
    return sorted(data) == data


def decreasing(data: list[int]) -> bool:
    return sorted(data, reverse=True) == data


def good_diffs(data: list[int]) -> bool:
    for i in range(len(data) - 1):
        diff = abs(data[i] - data[i + 1])
        if diff < 1 or diff > 3:
            return False
    return True


def good_line(line: list[int]) -> bool:
    return (increasing(line) or decreasing(line)) and good_diffs(line)


def damp_good_line(line: list[int]) -> bool:
    for i in range(len(line)):
        dampened = line[:]
        dampened.pop(i)
        if good_line(dampened):
            return True
    return False


def part1() -> int:
    count = 0
    for line in aoc.utils.data.day_input_ints(2):
        if good_line(line):
            count += 1
    return count


def part2() -> int:
    count = 0
    for line in aoc.utils.data.day_input_ints(2):
        if good_line(line) or damp_good_line(line):
            count += 1
    return count


def main() -> None:
    lines = ['day02:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
