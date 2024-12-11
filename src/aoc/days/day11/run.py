#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


def count_digits(s: int) -> int:
    return len(str(s))


def even_digits(s: int) -> bool:
    return count_digits(s) % 2 == 0


def split_digits(s: int) -> tuple[int, int]:
    ss = str(s)
    length = len(ss)
    half = int(length / 2)
    a = ss[:half]
    b = ss[half:]
    return int(a), int(b)


def step(initial: list[int], num_steps: int) -> list[list[int]]:
    states = [initial]
    for _ in range(num_steps):
        new_state = []
        for s in states[-1]:
            if s == 0:
                new_state.append(1)
            elif even_digits(s):
                a, b = split_digits(s)
                new_state.append(a)
                new_state.append(b)
            else:
                new_state.append(s * 2024)
        states.append(new_state)
    return states


def evolve(s: int) -> list[int]:
    new_state = []
    if s == 0:
        new_state.append(1)
    elif even_digits(s):
        a, b = split_digits(s)
        new_state.append(a)
        new_state.append(b)
    else:
        new_state.append(s * 2024)
    return new_state


def generate(s: int, loops: int, splits: int = 0) -> int:
    evolved = evolve(s)
    if len(evolved) > 1:
        splits += 1
    if loops > 1:
        for e in evolved:
            splits = generate(e, loops - 1, splits=splits)
    return splits


def blink(stones: dict) -> dict:
    out = {}
    for s, count in stones.items():
        if s == 0:
            out[1] = out.get(1, 0) + count
        elif even_digits(s):
            a, b = split_digits(s)
            out[a] = out.get(a, 0) + count
            out[b] = out.get(b, 0) + count
        else:
            val = s * 2024
            out[val] = out.get(val, 0) + count
    return out


def part1_test() -> int:
    splits = 0
    input = [125, 17]
    for s in input:
        splits += generate(s, 25)
    return splits + len(input)


def part1() -> int:
    stones = aoc.utils.data.day_input_ints(11)[0]
    splits = 0
    for s in stones:
        splits += generate(s, 25)
    return splits + len(stones)


def part2_split() -> int:
    stones = aoc.utils.data.day_input_ints(11)[0]
    splits = 0
    for s in stones:
        splits += generate(s, 75)
    return splits + len(stones)


def part2() -> int:
    stone_list = aoc.utils.data.day_input_ints(11)[0]
    stones = {}
    for s in stone_list:
        stones[s] = 1
    print(stones)
    for _ in range(75):
        stones = blink(stones)
    return sum(stones.values())


def main() -> None:
    lines = ['day11:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
