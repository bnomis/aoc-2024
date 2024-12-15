#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data
import aoc.utils.grid
import aoc.utils.types


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, value: Position) -> bool:  # type: ignore
        return self.x == value.x and self.y == value.y

    def __add__(self, value: Position) -> Position:
        return Position(self.x + value.x, self.y + value.y)

    def __mul__(self, value: int) -> Position:
        return Position(self.x * value, self.y * value)

    def update(self, value: Position) -> Position:
        self.x += value.x
        self.y += value.y
        return self


instruction_map = {
    '<': Position(-1, 0),
    '^': Position(0, -1),
    '>': Position(1, 0),
    'v': Position(0, 1),
}


def horizontal_vector(vector: Position) -> bool:
    return vector.x in (-1, 1)


class Movable:
    def __init__(self, id: str, position: Position) -> None:
        self.id = id
        self.position = position

    def move(self, position: Position) -> None:
        self.position = position


class Grid:
    def __init__(self, grid: list[list[str]], boxes: list[Movable], robot: Movable) -> None:
        self.grid = grid
        self.boxes = boxes
        self.robot = robot
        self.width = len(grid[0])
        self.height = len(grid)
        self.max_width = self.width - 1
        self.max_height = self.height - 1

    def is_space(self, position: Position) -> bool:
        return self.grid[position.y][position.x] == '.' and not self.is_movable(position)

    def is_wall(self, position: Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def is_box(self, position: Position) -> bool:
        return any(m.position == position for m in self.boxes)

    def is_robot(self, position: Position) -> bool:
        return self.robot.position == position

    def is_movable(self, position: Position) -> bool:
        return self.is_box(position) or self.is_robot(position)

    def box_at(self, position: Position) -> Movable:
        for b in self.boxes:
            if b.position == position:
                return b
        raise Exception('no box')

    def is_in_grid(self, position: Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def execute(self, instructions: str) -> None:
        for i in instructions:
            vector = instruction_map[i]
            new_position = self.robot.position + vector
            # immovable walls
            if self.is_wall(new_position):
                continue
            # move into space
            if self.is_space(new_position):
                self.robot.move(new_position)
                continue
            # box
            if self.push_boxes(new_position, vector):
                self.robot.move(new_position)

    def find_space(self, start: Position, vector: Position) -> Position | None:
        last_position = start
        while self.is_in_grid(last_position):
            new_position = last_position + vector
            if self.is_wall(new_position):
                return None
            if self.is_space(new_position):
                return new_position
            last_position = new_position

    def find_double_space(self, start: Position, vector: Position) -> Position | None:
        last_position = start
        next_last_position = start + vector
        while self.are_in_grid([last_position, next_last_position]):
            new_position = last_position + vector
            next_new_position = next_last_position + vector
            if self.are_wall([new_position, next_new_position]):
                return None
            if self.are_space([new_position, next_new_position]):
                return new_position
            last_position = new_position
            next_last_position = next_new_position

    def find_boxes(self, start: Position, vector: Position) -> list[Movable]:
        boxes = []
        last_position = start
        if self.is_box(start):
            boxes.append(self.box_at(start))

        while self.is_in_grid(last_position):
            new_position = last_position + vector
            if self.is_wall(new_position) or self.is_space(new_position):
                return boxes
            if self.is_box(new_position):
                boxes.append(self.box_at(new_position))
            last_position = new_position
        return boxes

    def push_boxes(self, start: Position, vector: Position) -> bool:
        if horizontal_vector(vector):
            space = self.find_double_space(start, vector)
        else:
            space = self.find_space(start, vector)
        if not space:
            return False
        for b in self.find_boxes(start, vector):
            b.position = b.position + vector
        return True

    def gps(self) -> int:
        total = 0
        for b in self.boxes:
            total += b.position.x
            total += b.position.y * 100
        return total


def lines_to_grid(lines: list[str]) -> Grid:
    boxes = []
    rows = []
    robot = Movable('@', Position(0, 0))
    for row_index, line in enumerate(lines):
        wor = []
        for column_index, c in enumerate(line):
            if c in ('.', '#'):
                wor.append(c)
            else:
                if c == 'O':
                    boxes.append(Movable(c, Position(column_index, row_index)))
                else:
                    robot = Movable(c, Position(column_index, row_index))
                wor.append('.')
        rows.append(wor)
    return Grid(rows, boxes, robot)


def break_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    lines_length = len(lines)
    grid_lines = []
    instructions = []
    instructions_start = 0

    for i in range(lines_length):
        line = lines[i]
        if not line:
            instructions_start = i + 1
            break
        grid_lines.append(lines[i])

    for i in range(instructions_start, lines_length):
        line = lines[i]
        if line:
            instructions.append(lines[i])

    return grid_lines, instructions


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(15)
    grid_lines, instructions = break_lines(lines)
    grid = lines_to_grid(grid_lines)
    instructions = ''.join(instructions)
    grid.execute(instructions)
    return grid.gps()


def part2() -> int:
    return 0


def main() -> None:
    lines = ['day15:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
