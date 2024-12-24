#!/usr/bin/env python
from __future__ import annotations

import operator

import aoc.utils.data


class Buyer:
    def __init__(self, start: int, steps: int) -> None:
        self.start = start
        self.steps = steps
        self.numbers = []
        self.deltas = []
        self.ones = []
        self.seqs = {}
        self.process(start, steps)

    def process(self, start: int, steps: int) -> None:
        self.numbers.append(start)
        self.ones.append(start % 10)
        current = start
        for i in range(1, steps + 1):
            output = current * 64
            output = operator.xor(current, output)
            output1 = output % 16777216

            output = int(output1 / 32)
            output = operator.xor(output1, output)
            output2 = output % 16777216

            output = output2 * 2048
            output = operator.xor(output2, output)
            output3 = output % 16777216
            current = output3
            self.numbers.append(current)
            self.ones.append(current % 10)
            self.deltas.append(self.ones[i] - self.ones[i - 1])
            if i > 3:
                s = (self.deltas[-4], self.deltas[-3], self.deltas[-2], self.deltas[-1])
                if s not in self.seqs:
                    self.seqs[s] = self.ones[-1]


def process(start: int, steps: int) -> int:
    current = start
    for _ in range(steps):
        output = current * 64
        output = operator.xor(current, output)
        output1 = output % 16777216

        output = int(output1 / 32)
        output = operator.xor(output1, output)
        output2 = output % 16777216

        output = output2 * 2048
        output = operator.xor(output2, output)
        output3 = output % 16777216
        current = output3
    return current


def part1() -> int:
    # return 0
    total = 0
    # lines = aoc.utils.data.day_test_lines(22)
    lines = aoc.utils.data.day_input_lines(22)
    for line in lines:
        num = int(line)
        total += process(num, 2000)
    return total


def part2() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(22, which=2)
    lines = aoc.utils.data.day_input_lines(22)
    buyers = []
    seqs = set()
    for line in lines:
        num = int(line)
        b = Buyer(num, 2000)
        buyers.append(b)
        bs = set(b.seqs.keys())
        seqs |= bs

    totals = []
    for s in seqs:
        t = 0
        for b in buyers:
            t += b.seqs.get(s, 0)
        totals.append(t)
    return max(totals)


def main() -> None:
    lines = ['22:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
