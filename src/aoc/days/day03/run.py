#!/usr/bin/env python
from __future__ import annotations

import re

import aoc.utils.data


def process_mul(mul: str) -> int:
    pattern = re.compile(r'mul\((?P<num1>\d{1,3}),(?P<num2>\d{1,3})\)')
    match = pattern.match(mul)
    if not match:
        raise Exception('No match')

    num1 = int(match.group('num1'))
    num2 = int(match.group('num2'))
    return num1 * num2


def extract_instructions(lines: list[str]) -> list[str]:
    pattern = re.compile(r'(?P<mul>mul\(\d{1,3},\d{1,3}\))|(?P<do>do\(\))|(?P<dont>don\'t\(\))')
    instructions = []
    for line in lines:
        pos = 0
        line_length = len(line)
        while True:
            if pos >= line_length:
                break
            match = pattern.search(line, pos)
            if match:
                instructions.append(match[0])
                pos = match.end()
            else:
                break
    return instructions


def filter_instructions(instructions: list[str]) -> list[str]:
    on = True
    out = []
    for ins in instructions:
        if ins == "don't()":
            on = False
        elif ins == "do()":
            on = True
        elif on:
            out.append(ins)
    return out


def part1() -> int:
    pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    muls = []
    for line in aoc.utils.data.day_input_lines(3):
        pos = 0
        line_length = len(line)
        while True:
            if pos >= line_length:
                break
            match = pattern.search(line, pos)
            if match:
                muls.append(match[0])
                pos = match.end()
            else:
                break
    count = 0
    for m in muls:
        count += process_mul(m)
    return count


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(3)
    instructions = extract_instructions(lines)
    instructions = filter_instructions(instructions)
    count = 0
    for m in instructions:
        count += process_mul(m)
    return count


def main() -> None:
    lines = ['day03:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
