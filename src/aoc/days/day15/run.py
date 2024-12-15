#!/usr/bin/env python
from __future__ import annotations

import curses

import aoc.utils.data
import aoc.utils.grid
import aoc.utils.types


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'{self.x},{self.y}'

    def __eq__(self, value: Position) -> bool:  # type: ignore
        return self.x == value.x and self.y == value.y

    def __neq__(self, value: Position) -> bool:  # type: ignore
        return self.x != value.x or self.y != value.y

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


def vertical_vector(vector: Position) -> bool:
    return vector.y in (-1, 1)


class Movable:
    def __init__(self, id: str, position: Position) -> None:
        self.id = id
        self.position = position

    def __str__(self) -> str:
        if self.width() == 1:
            return f'{self.position.x},{self.position.y}'
        return f'{self.position.x},{self.position.y} - {self.position.x +self.width() - 1},{self.position.y}'

    def __eq__(self, value: Movable) -> bool:  # type: ignore
        return self.id == value.id and self.position == value.position

    def __neq__(self, value: Movable) -> bool:  # type: ignore
        return self.id != value.id or self.position != value.position

    def __hash__(self) -> int:
        return hash((self.id, self.position.x, self.position.y))

    def move(self, position: Position) -> None:
        self.position = position

    def occupies(self, position: Position) -> bool:
        width = len(self.id)
        if width == 1:
            return self.position == position
        for i in range(width):
            my_position = Position(self.position.x + i, self.position.y)
            if my_position == position:
                return True
        return False

    def width(self) -> int:
        return len(self.id)

    def impose(self, vector: Position) -> Movable:
        position = self.position + vector
        return Movable(self.id, position)


class Grid:
    def __init__(
        self,
        grid: list[list[str]],
        boxes: list[Movable],
        robot: Movable,
        wide: bool = False,
    ) -> None:
        self.grid = grid
        self.boxes = boxes
        self.robot = robot
        self.width = len(grid[0])
        self.height = len(grid)
        self.max_width = self.width - 1
        self.max_height = self.height - 1
        self.wide = wide

    def box_count(self) -> int:
        return len(self.boxes)

    def print_grid(self) -> None:
        print('\n'.join(self.print_lines()))

    def print_lines(self) -> list[str]:
        lines = []
        for row_index, row in enumerate(self.grid):
            line = []
            i = 0
            while i < self.width:
                c = row[i]
                if c == '#':
                    line.append(c)
                    i += 1
                else:
                    position = Position(i, row_index)
                    if self.is_robot(position):
                        line.append('@')
                        i += 1
                    else:
                        box = False
                        for b in self.boxes:
                            if b.occupies(position):
                                line.append(b.id)
                                i += len(b.id)
                                box = True
                                break
                        if not box:
                            line.append('.')
                            i += 1
            lines.append(''.join(line))
        return lines

    def curse_grid(self, window: curses.window):
        lines = self.print_lines()
        for row_index, row in enumerate(lines):
            for line_index, c in enumerate(row):
                window.addch(row_index, line_index, c)
        window.refresh()
        # time.sleep(0.01)

    def is_space(self, position: Position) -> bool:
        return self.grid[position.y][position.x] == '.' and not self.is_movable(position)

    def are_space(self, positions: list[Position]) -> bool:
        return all(self.is_space(p) for p in positions)

    def span_is_space(self, position: Position, width: int) -> bool:
        for i in range(width):  # noqa: SIM110
            if not self.is_space(Position(position.x + i, position.y)):
                return False
        return True

    def movable_in_space(self, mover: Movable) -> bool:
        for i in range(mover.width()):
            pos = Position(mover.position.x + i, mover.position.y)
            if not self.is_space(pos):
                return False
        return True

    def is_wall(self, position: Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def are_wall(self, positions: list[Position]) -> bool:
        return all(self.is_wall(p) for p in positions)

    def span_is_wall(self, position: Position, width: int) -> bool:
        for i in range(width):  # noqa: SIM110
            if self.is_wall(Position(position.x + i, position.y)):
                return True
        return False

    def movable_in_wall(self, mover: Movable) -> bool:
        for i in range(mover.width()):
            pos = Position(mover.position.x + i, mover.position.y)
            if self.is_wall(pos):
                return True
        return False

    def is_box(self, position: Position) -> bool:
        return any(m.occupies(position) for m in self.boxes)

    def span_is_box(self, position: Position, width: int) -> bool:
        for i in range(width):  # noqa: SIM110
            if self.is_box(Position(position.x + i, position.y)):
                return True
        return False

    def is_robot(self, position: Position) -> bool:
        return self.robot.position == position

    def is_movable(self, position: Position) -> bool:
        return self.is_box(position) or self.is_robot(position)

    def box_at(self, position: Position) -> Movable:
        for b in self.boxes:
            if b.occupies(position):
                return b
        raise Exception('no box')

    def lhs_box(self, position: Position) -> Position:
        while self.is_box(position):
            position = Position(position.x - 1, position.y)
        return Position(position.x + 1, position.y)

    def is_box_lhs(self, position: Position) -> bool:
        try:
            box = self.box_at(position)
        except:
            return False
        width = box.width()
        if width == 1:
            return False
        return position.x == box.position.x

    def is_box_rhs(self, position: Position) -> bool:
        try:
            box = self.box_at(position)
        except:
            return False
        width = box.width()
        if width == 1:
            return False
        return position.x == box.position.x + width - 1

    def boxes_span(self, position: Position) -> int:
        count = 0
        while self.is_box(position):
            count += 1
            position = Position(position.x + 1, position.y)
        return count

    def boxes_in_span(self, position: Position, width: int) -> list[Movable]:
        boxes = set()
        for i in range(width):
            pos = Position(position.x + i, position.y)
            b = self.box_at(pos)
            if b:
                boxes.add(b)
        return list(boxes)

    def lhs_rhs(self, movers: list[Movable]) -> tuple[int, int]:
        lhs = self.width
        rhs = 0
        for m in movers:
            if m.position.x < lhs:
                lhs = m.position.x
            if m.position.x > rhs:
                rhs = m.position.x
        return lhs, rhs

    def is_in_grid(self, position: Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def are_in_grid(self, positions: list[Position]) -> bool:
        return all(self.is_in_grid(p) for p in positions)

    def movable_in_grid(self, mover: Movable) -> bool:
        lhs = mover.position
        rhs = Position(lhs.x + mover.width() - 1, lhs.y)
        return self.is_in_grid(lhs) and self.is_in_grid(rhs)

    def movables_in_grid(self, movers: set[Movable]) -> bool:
        for m in movers:  # noqa: SIM110
            if not self.movable_in_grid(m):
                return False
        return True

    def intersecting_boxes(self, mover: Movable) -> set[Movable]:
        boxes = set()
        for i in range(mover.width()):
            pos = Position(mover.position.x + i, mover.position.y)
            try:
                box = self.box_at(pos)
            except:
                pass
            else:
                boxes.add(box)
        return boxes

    def execute(self, instructions: str) -> None:
        # window = curses.initscr()
        # self.curse_grid(window)
        for i in instructions:
            vector = instruction_map[i]
            new_position = self.robot.position + vector
            # print(f'{i} {vector} {self.robot.position} -> {new_position}')
            # immovable walls
            if self.is_wall(new_position):
                # self.curse_grid(window)
                continue
            # move into space
            if self.is_space(new_position):
                self.robot.move(new_position)
                # self.curse_grid(window)
                continue
            # print('no space')
            # box
            if self.push_boxes(new_position, vector):
                # print('moved')
                self.robot.move(new_position)
            # else:
            # print('not moved')
            # self.curse_grid(window)
        # curses.endwin()
        # self.print_grid()

    def find_space(self, start: Position, vector: Position) -> Position | None:
        last_position = start
        while self.is_in_grid(last_position):
            new_position = last_position + vector
            if self.is_wall(new_position):
                return None
            if self.is_space(new_position):
                return new_position
            last_position = new_position

    def find_boxes(self, start: Position, vector: Position) -> list[Movable]:
        boxes = set()
        last_position = start
        if self.is_box(start):
            boxes.add(self.box_at(start))

        while self.is_in_grid(last_position):
            new_position = last_position + vector
            if self.is_wall(new_position) or self.is_space(new_position):
                return list(boxes)
            if self.is_box(new_position):
                boxes.add(self.box_at(new_position))
            last_position = new_position
        return list(boxes)

    def find_wide_space(self, start: Position, vector: Position) -> bool:
        boxes = set()
        boxes.add(self.box_at(start))
        while self.movables_in_grid(boxes):
            new_boxes = set()
            in_space = True
            for b in boxes:
                imposed = b.impose(vector)
                # print(f'imposed {b} -> {imposed}')
                if self.movable_in_wall(imposed):
                    # print('in wall')
                    return False

                if self.movable_in_space(imposed):
                    # new_boxes.add(imposed)
                    # print('in space')
                    continue

                intersects = self.intersecting_boxes(imposed)
                # print(f'intersects {intersects}')
                in_space = False
                new_boxes |= intersects
            if in_space:
                return True
            boxes = new_boxes
        return False

    def find_wide_boxes(self, start: Position, vector: Position) -> set[Movable]:
        found = set()
        found.add(self.box_at(start))
        level = set()
        level.add(self.box_at(start))
        while self.movables_in_grid(level):
            new_boxes = set()
            in_space = True
            for b in level:
                imposed = b.impose(vector)
                if self.movable_in_wall(imposed):
                    return found
                if self.movable_in_space(imposed):
                    # new_boxes.add(imposed)
                    continue
                new_boxes |= self.intersecting_boxes(imposed)
                in_space = False
            if in_space:
                return found
            level = new_boxes
            found |= level
        return found

    def push_boxes(self, start: Position, vector: Position) -> bool:
        boxes = []
        if self.wide and vertical_vector(vector):
            space = self.find_wide_space(start, vector)
            if not space:
                return False
            boxes = self.find_wide_boxes(start, vector)
        else:
            space = self.find_space(start, vector)
            if not space:
                return False
            boxes = self.find_boxes(start, vector)
        for b in boxes:
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


def lines_to_grid2(lines: list[str]) -> Grid:
    boxes = []
    rows = []
    robot = Movable('@', Position(0, 0))
    for row_index, line in enumerate(lines):
        wor = []
        for column_index, c in enumerate(line):
            if c in ('.', '#'):
                wor.append(c)
                wor.append(c)
            else:
                if c == 'O':
                    boxes.append(Movable('[]', Position(column_index * 2, row_index)))
                else:
                    robot = Movable(c, Position(column_index * 2, row_index))
                wor.append('.')
                wor.append('.')
        rows.append(wor)
    return Grid(rows, boxes, robot, wide=True)


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
    # lines = aoc.utils.data.day_test_lines(15, which=2)
    lines = aoc.utils.data.day_input_lines(15)

    grid_lines, instructions = break_lines(lines)
    grid = lines_to_grid2(grid_lines)
    instructions = ''.join(instructions)
    grid.execute(instructions)
    return grid.gps()


def main() -> None:
    lines = ['day15:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
