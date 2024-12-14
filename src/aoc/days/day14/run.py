#!/usr/bin/env python
from __future__ import annotations

import functools
import operator

import aoc.utils.data
import aoc.utils.grid
import aoc.utils.types


class Robot:
    def __init__(
        self,
        position: aoc.utils.types.Point,
        velocity: aoc.utils.types.Point,
    ) -> None:
        self.position = position
        self.velocity = velocity

    def __str__(self) -> str:
        return f'{self.position.x},{self.position.y} {self.velocity.x},{self.velocity.y}'

    def move(self, width: int, height: int) -> aoc.utils.types.Point:
        x = self.position.x + self.velocity.x
        y = self.position.y + self.velocity.y
        if x >= width:
            x = x - width
        elif x < 0:
            x = width + x
        if y >= height:
            y = y - height
        elif y < 0:
            y = height + y
        self.position = aoc.utils.types.Point(x, y)
        return self.position

    def quadrant(self, width: int, height: int) -> int:
        width_half = int(width / 2)
        height_half = int(height / 2)
        lhs = self.position.x < width_half
        rhs = self.position.x > width_half
        top = self.position.y < height_half
        bottom = self.position.y > height_half
        quad = 0
        if lhs:
            if top:
                quad = 1
            elif bottom:
                quad = 3
        elif rhs:
            if top:
                quad = 2
            elif bottom:
                quad = 4
        # print(f'quad {self.position.x},{self.position.y} {quad}')
        return quad


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.robots = []

    def add_robot(self, robot: Robot) -> None:
        self.robots.append(robot)

    def print_robots(self) -> None:
        for r in self.robots:
            print(r)

    def tick(self) -> None:
        # print('\n--before--')
        # self.print_robots()
        for r in self.robots:
            r.move(self.width, self.height)
        # print('\n--after--')
        # self.print_robots()

    def safety_factor(self) -> int:
        # self.print_robots()
        quads = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }
        for r in self.robots:
            q = r.quadrant(self.width, self.height)
            if q > 0:
                quads[q] += 1
        # print(quads)
        return functools.reduce(operator.mul, quads.values())

    def grid(self) -> list[list[int]]:
        grid = []
        for _ in range(self.height):
            row = [0] * self.width
            grid.append(row)

        for r in self.robots:
            grid[r.position.y][r.position.x] += 1
        # print(grid)
        return grid


def print_grid(grid: list[list[int]]) -> None:
    lines = []
    for row in grid:
        lines.append(''.join(map(str, row)))
    print('\n'.join(lines))


def line_to_robot(line: str) -> Robot:
    pos, vel = line.split()
    posa, posb = pos.split(',')
    px = int(posa[2:])
    py = int(posb)
    vela, velb = vel.split(',')
    vx = int(vela[2:])
    vy = int(velb)
    return Robot(aoc.utils.types.Point(px, py), aoc.utils.types.Point(vx, vy))


def good_grid(grid: list[list[int]]) -> bool:
    for row in grid:
        for column in row:
            if column > 1:
                return False
    return True


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(14)
    grid = Grid(101, 103)
    for line in lines:
        if not line:
            continue
        robot = line_to_robot(line)
        grid.add_robot(robot)
    for _ in range(100):
        grid.tick()
    return grid.safety_factor()


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(14)
    grid = Grid(101, 103)
    for line in lines:
        if not line:
            continue
        robot = line_to_robot(line)
        grid.add_robot(robot)

    g = None
    ticks = 0
    while True:
        grid.tick()
        ticks += 1
        g = grid.grid()
        if good_grid(g):
            break

    # print_grid(g)
    # print('')
    return ticks


def main() -> None:
    lines = ['day14:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
