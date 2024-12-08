#!/usr/bin/env python
from __future__ import annotations

import functools
import itertools
import operator

import aoc.utils.data


def concat(a: int, b: int) -> int:
    c = f'{a}{b}'
    return int(c)


operator_map = {
    '*': operator.mul,
    '+': operator.add,
    '|': concat
}

perm_cache = {}


class Equation:
    def __init__(self, target: int, numbers: list[int], operators: str = '*+') -> None:
        self.target = target
        self.numbers = numbers
        self.operators = operators

    def __str__(self) -> str:
        return f'{self.target}: {self.numbers}'

    def makes(self, ops: list[str]) -> tuple[bool, list[str]]:
        total = self.numbers[0]
        op_cache = []
        for i, o in enumerate(ops):
            op = operator_map[o]
            total = op(total, self.numbers[i + 1])
            op_cache.append(o)
            if total > self.target:
                return False, op_cache
        return total == self.target, op_cache

    def all_add(self) -> int:
        return functools.reduce(operator.add, self.numbers, 0)

    def all_mul(self) -> int:
        return functools.reduce(operator.mul, self.numbers, 1)

    def truthy(self) -> bool:
        num_nums = len(self.numbers)
        num_combs = num_nums - 1

        combs = []
        # build caches
        for c in itertools.combinations_with_replacement(self.operators, num_combs):
            combs.append(c)
            if c in perm_cache:
                continue
            perm_cache[c] = list()
            for p in itertools.permutations(c, num_combs):
                p = list(p)
                if p not in perm_cache[c]:
                    perm_cache[c].append(p)

        tried = []
        attempt = 0
        bad_ops = []
        for c in combs:
            for p in perm_cache[c]:
                if p in tried:
                    continue

                # starting bad ops
                bad_op = False
                for bo in bad_ops:
                    bol = len(bo)
                    if p[:bol] == bo:
                        print('bad ops')
                        bad_op = True
                        break
                if bad_op:
                    continue

                good, ops = self.makes(p)
                if good:
                    return True
                tried.append(p)
                if len(ops) > 0:
                    bad_ops.append(ops)
                attempt += 1
        return False


def parse_lines(lines: list[str], operators: str = '*+') -> list[Equation]:
    eqs = []
    for line in lines:
        target, number_str = line.split(':')
        target = int(target)
        numbers = []
        for n in number_str.split():
            numbers.append(int(n))
        eqs.append(Equation(target, numbers, operators=operators))
    return eqs


def part1() -> int:
    return 0
    lines = aoc.utils.data.day_input_lines(7)
    total = 0
    for e in parse_lines(lines):
        print(e)
        if e.truthy():
            total += e.target
    return total


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(7)
    total = 0
    for e in parse_lines(lines, operators='*+|'):
        print(e)
        if e.truthy():
            total += e.target
    return total

def main() -> None:
    lines = ['day07:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
