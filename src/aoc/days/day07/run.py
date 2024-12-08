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
        self.ops = []
        for c in operators:
            self.ops.append(operator_map[c])

    def __str__(self) -> str:
        return f'{self.target}: {self.numbers}'

    def makes_comb(self, ops: list[str]) -> tuple[bool, list[str]]:
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

    def truthy_comb(self) -> bool:
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

                good, ops = self.makes_comb(p)
                if good:
                    return True
                tried.append(p)
                if len(ops) > 0:
                    bad_ops.append(ops)
                attempt += 1
        return False

    def truthy(self) -> bool:
        # https://topaz.github.io/paste/#XQAAAQBgBQAAAAAAAAAzHIoib6qOhkKVB6+O3fm4OMHyeMAxpj3pnh6q9HZdml22zq92lTaCI7ki/Xux2v2vlBQsI5F0KacFpkIDsL+QmszzQV7aqkWXbZFOVE+EJ2DhIed7ZPO1Z5USfqlVt0eIwCm42m+1d21cAzMyh0q0Zk+lQT3aC2m9fRbR3QNERoDKWYHw6tIIawpcYQkatJYof9VuFBzAC8fQYiu5enK2oM3FqUCsX7rmG7MDuydOgf8Va4Umox+a0tyUEGu5l4OW4ucyEs343E4eZ0NMQ+CaQahhgMQlOk6l183CfDYbnBv0tbMdkY2PiwzBoAXXw9hGpGMImgn+Ma/NeM3xds8vN+c41JrwmKOyZ4wq2LROeu3nisZrW9KlBMy3RVtP5wtkUNL2KAHAoytBZOWw93/W8eucTOUcW28qF+/MSAHrb0M10Gw2cY5syUdMywQ564820PcZQUip+BGCj+Gp0PoQxw0UtYxmfaHmCnhHScDfk6ukcinV+f84PWBq0peFTbc5UKpBzDhQJxUK+hrSwGBcMpkLVxaC9oc5j+SAfsWnkqR3QU7KuTF9dDTOCfvf1rByJ+84zHOF4wWyfM7dyGzgK7T+OhqpW+QlfOWO5G+EucMP7qWv0hUKVn9HPjwGRELjxCjexL+j+mvgwdjIDjm10u0XwP3+J+gM4kHuMRugDapog5HBLXTUICOas15nOvucImdrXuYmoNBA2H5UNF3CQfNkz98E0XCCIkmGSNC+K7uhWc5hbVjVOKywGFP/5zLASA==
        accumulator = [self.numbers[0]]
        # print(accumulator)

        # this runs along the numbers
        # accumulating the results
        for num in self.numbers[1:-1]:
            accumulator = [
                result
                for partial in accumulator
                for op in self.ops
                if (result := op(partial, num)) <= self.target
            ]
            # print(accumulator)

        # last number
        num = self.numbers[-1]
        for partial in accumulator:
            for op in self.ops:
                if op(partial, num) == self.target:
                    return True
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
    lines = aoc.utils.data.day_input_lines(7)
    total = 0
    for e in parse_lines(lines):
        # print(e)
        if e.truthy():
            total += e.target
    return total


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(7)
    total = 0
    for e in parse_lines(lines, operators='*+|'):
        # print(e)
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
