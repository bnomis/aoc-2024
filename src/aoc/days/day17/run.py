#!/usr/bin/env python
from __future__ import annotations

import operator

import aoc.utils.data


class HaltException(Exception):
    pass


class ImpossibleException(Exception):
    pass


class Computer:
    opcode_to_instruction = {
        0: 'adv',
        1: 'bxl',
        2: 'bst',
        3: 'jnz',
        4: 'bxc',
        5: 'out',
        6: 'bdv',
        7: 'cdv',
    }

    def __init__(self, state: dict) -> None:
        self.a = state['registers']['A']
        self.b = state['registers']['B']
        self.c = state['registers']['C']
        self.program = state['program']
        self.instruction_pointer = 0
        self.output = []

    def __str__(self) -> str:
        lines = []
        lines.append(f'A: {self.a} B: {self.b} C: {self.c}')
        lines.append(str(self.program))
        lines.append(str(self.instruction_pointer))
        lines.append(str(self.output))
        return '\n'.join(lines)

    def get_output(self) -> str:
        return ','.join([str(o) for o in self.output])

    def run(self) -> None:
        program_length = len(self.program)
        while self.instruction_pointer < program_length - 1:
            self.execute(self.instruction_pointer)

    def execute(self, ip: int) -> None:
        opcode = self.program[ip]
        func_name = self.opcode_to_instruction[opcode]
        func = getattr(self, func_name)
        func(ip)

    def target(self, program: list[int]) -> bool:
        program_length = len(self.program)
        while self.instruction_pointer < program_length - 1:
            self.execute(self.instruction_pointer)
            if self.impossible_target(program):
                return False
        return self.output_matches_target(program)

    def impossible_target(self, target: list[int]) -> bool:
        if not self.output:
            return False
        return any(target[i] != self.output[i] for i in range(len(self.output)))

    def output_matches_target(self, target: list[int]) -> bool:
        target_length = len(target)
        output_length = len(self.output)
        if target_length != output_length:
            return False
        return all(target[i] == self.output[i] for i in range(target_length))

    def combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise Exception('Unknown operand')

    def adv(self, ip: int) -> None:
        numerator = self.a
        power = self.combo_operand(self.program[ip + 1])
        denominator = 2**power
        value = int(numerator / denominator)
        self.a = value
        self.instruction_pointer += 2

    def bxl(self, ip: int) -> None:
        value = operator.xor(self.b, self.program[ip + 1])
        self.b = value
        self.instruction_pointer += 2

    def bst(self, ip: int) -> None:
        value = operator.and_(self.combo_operand(self.program[ip + 1]), 7)
        self.b = value
        self.instruction_pointer += 2

    def jnz(self, ip: int) -> None:
        if self.a == 0:
            self.instruction_pointer += 1
            return
        self.instruction_pointer = self.program[ip + 1]

    def bxc(self, ip: int) -> None:
        value = operator.xor(self.b, self.c)
        self.b = value
        self.instruction_pointer += 2

    def out(self, ip: int) -> None:
        value = operator.and_(self.combo_operand(self.program[ip + 1]), 7)
        self.output.append(value)
        self.instruction_pointer += 2

    def bdv(self, ip: int) -> None:
        numerator = self.a
        power = self.combo_operand(self.program[ip + 1])
        denominator = 2**power
        value = int(numerator / denominator)
        self.b = value
        self.instruction_pointer += 2

    def cdv(self, ip: int) -> None:
        numerator = self.a
        power = self.combo_operand(self.program[ip + 1])
        denominator = 2**power
        value = int(numerator / denominator)
        self.c = value
        self.instruction_pointer += 2


def parse_input(lines: list[str]) -> dict:
    out = {'registers': {}, 'program': []}
    for line in lines:
        if not line:
            continue
        parts = line.split(':')
        if parts[0] == 'Program':
            ops = []
            for o in parts[1].split(','):
                o = o.strip()
                if not o:
                    continue
                ops.append(int(o))
            out['program'] = ops
        else:
            rid = parts[0].split()
            out['registers'][rid[1]] = int(parts[1])
    return out


# work from right to left finding the 3 bits in A which match the target
def find_digits(input: dict, astart: int, index: int, possible: set | None = None) -> int:
    if possible is None:
        possible = set()
    target = input['program']
    for n in range(8):
        # try the values 0 - 7 in the low three bits
        a = (astart << 3) | n
        input['registers']['A'] = a
        computer = Computer(input)
        computer.run()
        # have we matched the last digits of the target
        if computer.output == target[-index:]:
            if computer.output == target:
                possible.add(a)
            else:
                find_digits(input, a, index + 1, possible=possible)
    if len(possible) > 0:
        return min(possible)
    return 0


def part1() -> str:
    # return '?'
    # lines = aoc.utils.data.day_test_lines(17, which=0)
    lines = aoc.utils.data.day_input_lines(17)
    parsed_input = parse_input(lines)
    computer = Computer(parsed_input)
    computer.run()
    return computer.get_output()


def part2_slow() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(17, which=2)
    lines = aoc.utils.data.day_input_lines(17)
    parsed_input = parse_input(lines)
    target = parsed_input['program']
    found = False
    a = 0
    while not found:
        parsed_input['registers']['A'] = a
        computer = Computer(parsed_input)
        if computer.target(target):
            found = True
            break
        a += 1
    return a


def part2() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(17, which=2)
    lines = aoc.utils.data.day_input_lines(17)
    parsed_input = parse_input(lines)
    return find_digits(parsed_input, 0, 1)


def main() -> None:
    lines = ['day17:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
