#!/usr/bin/env python
from __future__ import annotations

import collections
import enum
import sys

import aoc.utils.data

Point = collections.namedtuple('Point', ['x', 'y'])
Node = collections.namedtuple('Node', ['x', 'y', 'direction'])


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3


moves = {
    Direction.UP: [0, -1],
    Direction.RIGHT: [1, 0],
    Direction.LEFT: [-1, 0],
    Direction.DOWN: [0, 1],
}

rotations = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

char_to_direction = {'^': Direction.UP, '>': Direction.RIGHT, 'v': Direction.DOWN, '<': Direction.LEFT}


class ObstructionException(Exception):
    pass


class OffGridException(Exception):
    pass


class LoopException(Exception):
    pass


class Grid:
    def __init__(self, test: bool = False) -> None:
        self.grid = [[]]
        self.width = 0
        self.height = 0
        self.max_width = 0
        self.max_height = 0

        if test:
            self.load_test()
        else:
            self.load_input()

        self.size_grid()

    def load_input(self) -> None:
        self.grid = aoc.utils.data.day_input_grid(6)

    def load_test(self) -> None:
        self.grid = aoc.utils.data.day_test_grid(6)

    def size_grid(self) -> None:
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.max_width = self.width - 1
        self.max_height = self.height - 1

    def point_is_outside_of_grid(self, point: Point) -> bool:
        return point.x < 0 or point.y < 0 or point.x > self.max_width or point.y > self.max_height

    def point_is_obstruction(self, point: Point) -> bool:
        return self.grid[point.y][point.x] == '#'

    def guard_position(self) -> Point:
        for row_index, row in enumerate(self.grid):
            for column_index, c in enumerate(row):
                if c not in ['.', '#']:
                    return Point(column_index, row_index)
        raise Exception('guard not found')

    def guard_direction(self, point: Point | None) -> Direction:
        if not point:
            point = self.guard_position()
        c = self.grid[point.y][point.x]
        return char_to_direction[c]

    def add_obstruction(self, point: Point) -> None:
        if self.grid[point.y][point.x] != '.':
            raise Exception(f'not a space: {point}')
        self.grid[point.y][point.x] = '#'

    def remove_obstruction(self, point: Point) -> None:
        if self.grid[point.y][point.x] != '#':
            raise Exception(f'not an obstruction: {point}')
        self.grid[point.y][point.x] = '.'


class Guard:
    def __init__(
        self,
        position: Point,
        direction: Direction,
        loopy: bool = False,
    ) -> None:
        self.loopy = loopy
        self.starting_position = position
        self.starting_direction = direction
        self.position = position
        self.direction = direction
        self.path = [self.position]
        self.current_node = Node(position.x, position.y, direction)
        self.graph = {self.current_node: set()}

    def next_point(self) -> Point:
        move = moves[self.direction]
        return Point(self.position.x + move[0], self.position.y + move[1])

    def print_graph(self, name: str) -> None:
        print(name)
        nodes = sorted(list(self.graph.keys()))
        for k in nodes:
            kids = sorted(list(self.graph[k]))
            print(f'{k} -> {kids}')
        print('\n')

    def cyclic(self, current: Node, visited: dict, recursed: dict) -> bool:
        if not visited[current]:
            visited[current] = True
            recursed[current] = True

            for x in self.graph[current]:
                if (not visited[x] and self.cyclic(x, visited, recursed)) or recursed[x]:
                    return True

        recursed[current] = False
        return False

    def cycle(self, start: Node) -> bool:
        # https://www.geeksforgeeks.org/detect-cycle-in-a-graph/

        # start at start
        nodes = list(self.graph.keys())
        nodes.remove(start)
        nodes = [start] + nodes

        visited = {}
        recursed = {}
        for k in nodes:
            visited[k] = False
            recursed[k] = False

        return any(not visited[k] and self.cyclic(k, visited, recursed) for k in nodes)

    def move(self, grid: Grid) -> None:
        nextp = self.next_point()

        if grid.point_is_outside_of_grid(nextp):
            raise OffGridException()

        if grid.point_is_obstruction(nextp):
            raise ObstructionException()

        self.position = nextp
        self.path.append(self.position)

        if self.loopy:
            next_node = Node(nextp.x, nextp.y, self.direction)
            self.graph[self.current_node].add(next_node)

            possible_loop = False
            if next_node not in self.graph:
                self.graph[next_node] = set()
            else:
                possible_loop = True

            if possible_loop and self.cycle(next_node):
                raise LoopException()

            self.current_node = next_node

    def rotate(self) -> None:
        self.direction = rotations[self.direction]

    def patrol(self, grid: Grid) -> int:
        while True:
            try:
                self.move(grid)
            except ObstructionException:
                self.rotate()
            except OffGridException:
                break
            except LoopException:
                if self.loopy:
                    raise
        path_set = set(self.path)
        return len(path_set)


def part1() -> int:
    grid = Grid()
    guard_position = grid.guard_position()
    guard = Guard(guard_position, grid.guard_direction(guard_position))
    return guard.patrol(grid)


def part2() -> int:
    grid = Grid()
    guard_position = grid.guard_position()
    # walk the default path
    guard_direction = grid.guard_direction(guard_position)
    guard = Guard(guard_position, guard_direction)
    guard.patrol(grid)
    guard_start_set = set([guard.path[0]])
    possibles = set(guard.path) - guard_start_set
    found = 0
    for p in possibles:
        grid.add_obstruction(p)
        loopy = Guard(guard_position, guard_direction, loopy=True)
        try:
            loopy.patrol(grid)
        except LoopException:
            found += 1
        grid.remove_obstruction(p)
    return found


def main() -> None:
    sys.setrecursionlimit(10**4)
    lines = ['day06:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
