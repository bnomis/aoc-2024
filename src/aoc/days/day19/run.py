#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data
import aoc.utils.types


def parse_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    patterns = []
    designs = []
    for p in lines[0].split(','):
        p = p.strip()
        patterns.append(p)
    patterns = sorted(patterns, key=lambda x: len(x), reverse=True)

    lines_length = len(lines)
    for i in range(2, lines_length):
        designs.append(lines[i])

    return patterns, designs


def design_is_possible(
    patterns: list[str],
    design: str,
) -> bool:
    exhausted = False
    possibles = set()
    filtered_patterns = []
    for p in patterns:
        pos = design.find(p)
        if pos == -1:
            continue

        filtered_patterns.append(p)
        if design.startswith(p):
            possibles.add(p)

    # print(f'filtered: {filtered_patterns}')
    # print(f'find: {design}')
    while not exhausted:
        new_possibles = set()
        for po in possibles:
            # print(f'try: {po} {design}')
            for p in filtered_patterns:
                np = po + p
                if np == design:
                    # print(f'found: {design}')
                    return True

                if design.startswith(np):
                    new_possibles.add(np)

        if not new_possibles:
            # print(f'impossible: {design}')
            return False

        # print(new_possibles)
        # print('--round')
        possibles = new_possibles

    return False


def possible_designs(patterns: list[str], designs: list[str]) -> list[str]:
    possible = []
    for d in designs:
        if design_is_possible(patterns, d):
            possible.append(d)
    return possible


def print_possibles_seq(possibles: dict):
    for k in sorted(possibles.keys()):
        print(k)
        lines = []
        for c in sorted(possibles[k]):
            lines.append(str(c))
        line = '\n  '.join(lines)
        print(f'  {line}')


# this works but is too slow
# we're only interested in the count
# see below version
def all_combos_seq(
    patterns: list[str],
    design: str,
) -> set:
    found = set()
    exhausted = False
    possibles = {}
    filtered_patterns = []
    for p in patterns:
        pos = design.find(p)
        if pos == -1:
            continue

        filtered_patterns.append(p)
        if design.startswith(p):
            if p not in possibles:
                possibles[p] = set()
            possibles[p].add((p,))

    while not exhausted:
        new_possibles = {}
        # dict of possible set of combs
        print_possibles_seq(possibles)
        for pos, posp in possibles.items():
            # loop through combs
            for po in posp:
                for p in filtered_patterns:
                    np = pos + p
                    if np == design:
                        print(f'found {po} {p}')
                        found.add(po + (p,))
                        continue

                    if design.startswith(np):
                        if np not in new_possibles:
                            new_possibles[np] = set()
                        new_possibles[np].add(po + (p,))

        if not new_possibles:
            break
        possibles = new_possibles

    return found


def all_combos(
    patterns: list[str],
    design: str,
) -> int:
    found = 0
    exhausted = False
    # possible is count of possible combinations for this string
    possibles = {}
    filtered_patterns = []
    for p in patterns:
        pos = design.find(p)
        if pos == -1:
            continue

        filtered_patterns.append(p)
        if design.startswith(p):
            possibles[p] = 1

    while not exhausted:
        new_possibles = {}
        for pos, count in possibles.items():
            for p in filtered_patterns:
                np = pos + p
                if np == design:
                    found += count
                    continue

                if design.startswith(np):
                    if np not in new_possibles:
                        new_possibles[np] = 0
                    new_possibles[np] += count

        if not new_possibles:
            break
        possibles = new_possibles

    return found


def all_possible(patterns: list[str], designs: list[str]) -> list[int]:
    possible = []
    for d in designs:
        combs = all_combos(patterns, d)
        possible.append(combs)
    return possible


def part1() -> int:
    # lines = aoc.utils.data.day_test_lines(19, which=0)
    lines = aoc.utils.data.day_input_lines(19)
    patterns, designs = parse_lines(lines)
    possible = possible_designs(patterns, designs)
    return len(possible)


def part2() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(19, which=0)
    lines = aoc.utils.data.day_input_lines(19)
    patterns, designs = parse_lines(lines)
    lengths = all_possible(patterns, designs)
    return sum(lengths)


def main() -> None:
    lines = ['day19:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
