#!/usr/bin/env python
from __future__ import annotations

import random

import aoc.utils.data
import aoc.utils.grid
import aoc.utils.types

"""
px = A.x * a + B.x * b
py = A.y * a + B.y * b

a = px - Bx * b
    ------------
         Ax

b = py - Ay * a
    ------------
         By

a = px - Bx * (py - Ay * a) / By
    -------------------------------
                 Ax

a = px - (Bx * py) / By + (Bx * Ay * a) / By
    ---------------------------------------------
                 Ax

Ax * a = px - (Bx * py) / By + (Bx * Ay * a) / By
Ax * By * a = px * By - (Bx * py) + (Bx * Ay * a)
Ax * By * a - (Bx * Ay * a) = px * B.y - (Bx * py)
a (AxBy - BxAy) = pxBy - Bxpy

a = pxBy - Bxpy
    -----------
    AxBy - BxAy
"""

button_costs = {
    'A': 3,
    'B': 1,
}

max_button_presses = 100


class Button:
    def __init__(self, id: str, x: int, y: int) -> None:
        self.id = id
        self.delta = aoc.utils.types.Point(x, y)

    def add_to_point(self, point: aoc.utils.types.Point) -> aoc.utils.types.Point:
        return aoc.utils.types.Point(point.x + self.delta.x, point.y + self.delta.y)


def path_to_counts(path: list[str]) -> dict:
    counts = {}
    for p in path:
        if p not in counts:
            counts[p] = 0
        counts[p] += 1
    return counts


def path_to_costs(path: list[str]) -> int:
    costs = 0
    counts = path_to_counts(path)
    for k, v in counts.items():
        costs += button_costs[k] * v
    return costs


def path_has_max_presses(path: list[str]) -> bool:
    counts = path_to_counts(path)
    for v in counts.values():  # noqa: SIM110
        if v >= max_button_presses:
            return True
    return False


def prize_paths(
    prize: aoc.utils.types.Point,
    buttons: list[Button],
    position: aoc.utils.types.Point,
    path: list[str],
    found: list[list[str]],
) -> list[list[str]]:
    # print(f'{prize} {buttons} {position} {path} {found}')
    # overshoot
    if position.x > prize.x:
        return found
    if position.y > prize.y:
        return found
    # found
    if position == prize:
        found.append(path)
        print(f'found {path}')
        return found
    # too many presses per button
    if len(path) >= 100 and path_has_max_presses(path):
        return found
    random.shuffle(buttons)
    for b in buttons:
        np = b.add_to_point(position)
        if np.x < prize.x and np.y < prize.y:
            found = prize_paths(prize, buttons, np, path + [b.id], found)
    return found


def line_to_button(line: str) -> Button:
    button, pos = line.split(':')
    _, id = button.split()
    xs, ys = pos.strip().split(', ')
    x = int(xs[2:])
    y = int(ys[2:])
    return Button(id, x, y)


def line_to_prize(line: str) -> aoc.utils.types.Point:
    _, pos = line.split(':')
    xs, ys = pos.strip().split(', ')
    x = int(xs[2:])
    y = int(ys[2:])
    return aoc.utils.types.Point(x, y)


def lines_to_machine(lines: list[str]) -> tuple[list[Button], aoc.utils.types.Point]:
    a = line_to_button(lines[0])
    b = line_to_button(lines[1])
    prize = line_to_prize(lines[2])
    return [a, b], prize


def lines_to_machines(lines: list[str]) -> list[tuple[list[Button], aoc.utils.types.Point]]:
    length = len(lines)
    machines = []
    line_index = 0
    while line_index < length:
        machine = lines_to_machine(lines[line_index:])
        machines.append(machine)
        line_index += 4
    return machines


def count_presses(buttons: list[Button], prize: aoc.utils.types.Point) -> list[list[int]]:
    counts = []
    a = buttons[0].delta
    b = buttons[1].delta
    max_a = int(max([prize.x / a.x, prize.y / a.y])) + 1
    max_b = int(max([prize.x / b.x, prize.y / b.y])) + 1
    max_a = min([max_a, max_button_presses])
    max_b = min([max_b, max_button_presses])
    for ac in range(max_a):
        for bc in range(max_b):
            x = a.x * ac + b.x * bc
            y = a.y * ac + b.y * bc
            if x == prize.x and y == prize.y:
                print(f'found: {ac, bc}')
                counts.append([ac, bc])
    return counts


def count_algebra(buttons: list[Button], prize: aoc.utils.types.Point) -> list[int] | None:
    A = buttons[0].delta
    B = buttons[1].delta
    a = (prize.x * B.y - prize.y * B.x) / (A.x * B.y - A.y * B.x)
    b = (prize.y - A.y * a) / B.y
    if a.is_integer() and b.is_integer():
        return [a, b]
    return None


def machine_to_cheapest_cost_recurse(buttons: list[Button], prize: aoc.utils.types.Point) -> int:
    start = aoc.utils.types.Point(0, 0)
    found = prize_paths(prize, buttons, start, [], [])
    if not found:
        return 0
    costs = []
    for p in found:
        costs.append(path_to_costs(p))
    return sorted(costs)[0]


def machine_to_cheapest_cost_presses(buttons: list[Button], prize: aoc.utils.types.Point) -> int:
    found = count_presses(buttons, prize)
    if not found:
        return 0
    costs = []
    for p in found:
        costs.append(p[0] * 3 + p[1])
    return sorted(costs)[0]


def machine_to_cheapest_cost_algebra(buttons: list[Button], prize: aoc.utils.types.Point) -> int:
    found = count_algebra(buttons, prize)
    if not found:
        return 0
    return int(found[0] * 3 + found[1])


def part1_presses() -> int:
    lines = aoc.utils.data.day_input_lines(13)
    costs = 0
    for buttons, prize in lines_to_machines(lines):
        costs += machine_to_cheapest_cost_presses(buttons, prize)
    return costs


def part1_recurse() -> int:
    lines = aoc.utils.data.day_test_lines(13)
    costs = 0
    for buttons, prize in lines_to_machines(lines):
        costs += machine_to_cheapest_cost_recurse(buttons, prize)
    return costs


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(13)
    costs = 0
    for buttons, prize in lines_to_machines(lines):
        costs += machine_to_cheapest_cost_algebra(buttons, prize)
    return costs


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(13)
    costs = 0
    for buttons, prize in lines_to_machines(lines):
        prize = aoc.utils.types.Point(prize.x + 10000000000000, prize.y + 10000000000000)
        costs += machine_to_cheapest_cost_algebra(buttons, prize)
    return costs


def main() -> None:
    lines = ['day13:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
