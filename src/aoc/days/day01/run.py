#!/usr/bin/env python
from __future__ import annotations

import functools
import operator

import aoc.utils.data


def sorted_columns(lines: list[list[int]]) -> tuple[list[int], list[int]]:
    left = []
    right = []
    for line in lines:
        left.append(line[0])
        right.append(line[-1])
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    return left_sorted, right_sorted


def part1() -> int:
    left_sorted, right_sorted = sorted_columns(aoc.utils.data.day_input_ints(1))
    diffs = []
    for i in range(len(left_sorted)):
        diffs.append(abs(left_sorted[i] - right_sorted[i]))
    return functools.reduce(operator.add, diffs)


def part2() -> int:
    left_sorted, right_sorted = sorted_columns(aoc.utils.data.day_input_ints(1))
    count_cache = {}
    max_index = len(left_sorted)
    left_index = 0
    right_index = 0
    num_times = []
    while left_index < max_index:
        left_num = left_sorted[left_index]
        if left_num not in count_cache:
            left_num_times = 0
            while right_index < max_index:
                right_num = right_sorted[right_index]
                if right_num < left_num:
                    right_index += 1
                elif right_num == left_num:
                    left_num_times += 1
                    right_index += 1
                else:
                    break
            count_cache[left_num] = left_num_times
        num_times.append([left_num, count_cache[left_num]])
        left_index += 1

    total = 0
    for num, count in num_times:
        total += (num * count)
    return total


def main() -> None:
    lines = ['day01:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
