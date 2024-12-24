#!/usr/bin/env python
from __future__ import annotations

import operator

import aoc.utils.data


def nop(a, b) -> None:
    pass


op_to_op = {
    'NOP': nop,
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor,
}

wires = {}
wire_values = {}
zwires = set()


def get_wire_value(w: str) -> int | None:
    return wire_values.get(w)


def set_wire_value(w: str, value: int) -> int:
    wire_values[w] = value
    return value


class Wire:
    def __init__(self, name: str, a: str, b: str, op: str, state: int | None = None) -> None:
        self.name = name
        self.a = a
        self.b = b
        self.op_name = op
        self.op = op_to_op[op]
        self.state = state

    def run(self) -> int | None:
        a = get_wire_value(self.a)
        b = get_wire_value(self.b)
        if a is None or b is None:
            return None

        self.state = self.op(a, b)
        set_wire_value(self.name, self.state)
        return self.state


def lines_to_wires(lines: list[str]):
    ops = 0
    for index, line in enumerate(lines):
        if not line:
            ops = index + 1
            break
        name, value = line.split(':')
        value = int(value)
        wire_values[name] = value
        wires[name] = Wire(name, '', '', 'NOP', value)
        if name.startswith('z'):
            zwires.add(name)

    for i in range(ops, len(lines)):
        line = lines[i]
        parts = lines[i].split()
        name = parts[4]
        wires[name] = Wire(name, parts[0], parts[2], parts[1])
        if name.startswith('z'):
            zwires.add(name)


def step() -> None:
    for w in wires.values():
        if w.state is None:
            w.run()


def zcomplete() -> bool:
    return all(wires[w].state is not None for w in zwires)


def get_zvalues() -> list[int]:
    values = []
    for w in sorted(list(zwires), reverse=True):
        values.append(wires[w].state)
    return values


def binary_to_decimal(binary_str):
    decimal = 0
    for digit in binary_str:
        # Multiply the current decimal by 2 (shift left) and add the new bit
        decimal = decimal * 2 + int(digit)
    return decimal


def find_wire(a: str, b: str, op: str) -> Wire | None:
    for w in wires.values():
        if w.op_name == op and ((w.a == a and w.b == b) or (w.a == b and w.b == a)):
            return w
    raise Exception(f'not found {a} {op} {b}')
    return None


def wrong_wires_orig() -> set:
    wrong = set()
    op_to_wire = {}
    op_to_wire['z00_carry'] = find_wire('x00', 'y00', 'AND')
    swap = {}

    for i in range(1, 45):
        print(i)
        xname = f'x{i:02}'
        yname = f'y{i:02}'
        zname = f'z{i:02}'
        z_out = wires[zname]

        xy_xor_key = f'xy{i:02}_xor'
        xy_xor_wire = find_wire(xname, yname, 'XOR')
        op_to_wire[xy_xor_key] = xy_xor_wire

        # xor for this bit's output
        xy_xor_name = xy_xor_wire.name

        previous_carry = f'z{i-1:02}_carry'
        previous_carry_name = op_to_wire[previous_carry].name

        z_out_set = set([z_out.a, z_out.b])
        proper_z_out_set = set([xy_xor_name, previous_carry_name])
        common = z_out_set & proper_z_out_set
        swapped = set()
        if len(common) != 2:
            missing = z_out_set - common
            swapped |= missing
            missing = proper_z_out_set - common
            swapped |= missing
            print(swapped)
            swl = list(swapped)
            swap[swl[0]] = swl[1]
            swap[swl[1]] = swl[0]
            wrong |= swapped

        if xy_xor_name in swap:
            xy_xor_name = swap[xy_xor_name]
        if previous_carry_name in swap:
            previous_carry_name = swap[previous_carry_name]

        xy_xor_and_prev_carry_wire = find_wire(xy_xor_name, previous_carry_name, 'AND')
        xy_and_wire = find_wire(xname, yname, 'AND')
        or_to_carry = find_wire(xy_xor_and_prev_carry_wire.name, xy_and_wire.name, 'OR')
        op_to_wire[f'z{i:02}_carry'] = or_to_carry

        if len(wrong) == 8:
            return wrong
    return wrong


def parse_ops(lines: list[str]) -> list[tuple]:
    operations = []
    ops = 0
    for index, line in enumerate(lines):
        if not line:
            ops = index + 1
    for i in range(ops, len(lines)):
        line = lines[i]
        parts = line.split()
        operations.append((parts[0], parts[1], parts[2], parts[4]))
    return operations


def wrong_wires(lines: list[str]) -> set:
    # see adder circuit
    # https://www.caretxdigital.com/
    wrong = set()
    operations = parse_ops(lines)
    for op1, op, op2, res in operations:
        # z output must be xor apart from the top bit
        if res[0] == 'z' and op != 'XOR' and res != 'z45':
            wrong.add(res)

        # xor gates which don't have x,y inputs and not a z output
        if op == 'XOR' and res[0] not in ['z'] and op1[0] not in ['x', 'y'] and op2[0] not in ['x', 'y']:
            wrong.add(res)

        # and gates always go to or gates, apart from the first bit
        if op == 'AND' and 'x00' not in (op1, op2):
            for subop1, subop, subop2, _ in operations:
                if (res in (subop1, subop2)) and subop != 'OR':
                    wrong.add(res)

        # xor gates never go to or gates
        if op == 'XOR' and 'x00' not in (op1, op2):
            for subop1, subop, subop2, _ in operations:
                if (res in (subop1, subop2)) and subop == 'OR':
                    wrong.add(res)

    return wrong


def part1() -> int:
    return 0
    # lines = aoc.utils.data.day_test_lines(24, which=2)
    lines = aoc.utils.data.day_input_lines(24)
    lines_to_wires(lines)
    while not zcomplete():
        step()
    zvalues = get_zvalues()
    binary_str = ''.join([str(b) for b in zvalues])
    return binary_to_decimal(binary_str)


def part2() -> str:
    lines = aoc.utils.data.day_input_lines(24)
    wrong = wrong_wires(lines)
    return ','.join(sorted(list(wrong)))


def main() -> None:
    lines = ['24:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
