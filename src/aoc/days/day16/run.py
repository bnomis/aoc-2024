#!/usr/bin/env python
from __future__ import annotations

import curses
import sys
import time

import aoc.utils.data
import aoc.utils.grid
import aoc.utils.types

direction_to_vector = {
    'N': aoc.utils.types.Position(0, -1),
    'S': aoc.utils.types.Position(0, 1),
    'E': aoc.utils.types.Position(1, 0),
    'W': aoc.utils.types.Position(-1, 0),
}

vector_to_direction = {
    aoc.utils.types.Position(0, -1): 'N',
    aoc.utils.types.Position(0, 1): 'S',
    aoc.utils.types.Position(1, 0): 'E',
    aoc.utils.types.Position(-1, 0): 'W',
}

direction_to_char = {
    'N': '^',
    'S': 'v',
    'E': '>',
    'W': '<',
}


def direction_rotate_right(direction: str) -> str:
    directions = {
        'N': 'E',
        'S': 'W',
        'E': 'S',
        'W': 'N',
    }
    return directions[direction]


def direction_rotate_left(direction: str) -> str:
    directions = {
        'N': 'W',
        'S': 'E',
        'E': 'N',
        'W': 'S',
    }
    return directions[direction]


def direction_to_rotations(start: str, end: str) -> int:
    mapper = {
        'N': {
            'N': 0,
            'E': 1,
            'W': 1,
            'S': 2,
        },
        'S': {
            'S': 0,
            'E': 1,
            'W': 1,
            'N': 2,
        },
        'E': {
            'E': 0,
            'N': 1,
            'S': 1,
            'W': 2,
        },
        'W': {
            'W': 0,
            'N': 1,
            'S': 1,
            'E': 2,
        },
    }
    return mapper[start][end]


def forward(position: aoc.utils.types.Position, direction: str) -> aoc.utils.types.Position:
    return position + direction_to_vector[direction]


class Reindeer:
    def __init__(self, position: aoc.utils.types.Position, direction: str) -> None:
        self.position = position
        self.direction = direction

    def forward_position(self) -> aoc.utils.types.Position:
        return self.position + direction_to_vector[self.direction]

    def rotate_right(self) -> str:
        self.direction = direction_rotate_right(self.direction)
        return self.direction

    def rotate_left(self) -> str:
        self.direction = direction_rotate_left(self.direction)
        return self.direction


class Grid:
    def __init__(
        self,
        grid: list[list[str]],
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> None:
        self.grid = grid
        self.start = start
        self.end = end
        self.width = len(grid[0])
        self.height = len(grid)
        self.max_width = self.width - 1
        self.max_height = self.height - 1

    def print_grid(self, current: aoc.utils.types.Position, direction: str, end: aoc.utils.types.Position) -> None:
        print('\n'.join(self.print_lines(current, direction, end)))

    def print_lines(self, current: aoc.utils.types.Position, direction: str, end: aoc.utils.types.Position) -> list[str]:
        lines = []
        for row_index, row in enumerate(self.grid):
            line = []
            i = 0
            while i < self.width:
                if current.x == i and current.y == row_index and end.x == i and end.y == row_index:
                    c = '*'
                elif current.x == i and current.y == row_index:
                    c = direction_to_char[direction]
                elif end.x == i and end.y == row_index:
                    c = '@'
                else:
                    c = row[i]
                line.append(c)
                i += 1
            lines.append(line)
        return lines

    def curse_grid(self, window: curses.window, current: aoc.utils.types.Position, direction: str, end: aoc.utils.types.Position) -> None:
        lines = self.print_lines(current, direction, end)
        for row_index, row in enumerate(lines):
            for line_index, c in enumerate(row):
                try:  # noqa: SIM105
                    window.addch(row_index, line_index, c)
                except Exception:
                    # print(f'Exception: {line_index},{row_index}: {e}')
                    pass
        window.refresh()
        time.sleep(0.1)

    def is_space(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '.'

    def are_space(self, positions: list[aoc.utils.types.Position]) -> bool:
        return all(self.is_space(p) for p in positions)

    def span_is_space(self, position: aoc.utils.types.Position, width: int) -> bool:
        for i in range(width):  # noqa: SIM110
            if not self.is_space(aoc.utils.types.Position(position.x + i, position.y)):
                return False
        return True

    def is_wall(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def are_wall(self, positions: list[aoc.utils.types.Position]) -> bool:
        return all(self.is_wall(p) for p in positions)

    def span_is_wall(self, position: aoc.utils.types.Position, width: int) -> bool:
        for i in range(width):  # noqa: SIM110
            if self.is_wall(aoc.utils.types.Position(position.x + i, position.y)):
                return True
        return False

    def is_in_grid(self, position: aoc.utils.types.Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def are_in_grid(self, positions: list[aoc.utils.types.Position]) -> bool:
        return all(self.is_in_grid(p) for p in positions)

    def calculate_score(self, path: list[aoc.utils.types.Position], rotations: int) -> int:
        return len(path) - 1 + (rotations * 1000)

    def exceeds_best(self, best, rotations: int, path: list[aoc.utils.types.Position]) -> bool:
        if best == 0:
            return False
        return self.calculate_score(path, rotations) > best

    def is_best(self, best, rotations: int, path: list[aoc.utils.types.Position]) -> bool:
        if best == 0:
            return True
        return self.calculate_score(path, rotations) < best

    def neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def neighbour_vectors(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if not self.is_wall(new_position):
                ns.append(v)
        return ns

    def print_path(self, path: list[aoc.utils.types.Position]) -> None:
        if not path:
            print('no path')
        lines = ['path']
        for p in path:
            lines.append(str(p))
        print('\n '.join(lines))

    def best_founds(self, founds: list[tuple[list[aoc.utils.types.Position], int]] | None) -> tuple[list[aoc.utils.types.Position], int] | None:
        if founds is None or len(founds) == 0:
            return None
        best = -1
        best_index = 0
        for index, found in enumerate(founds):
            if best == -1:
                best = self.calculate_score(found[0], found[1])
                best_index = index
            else:
                score = self.calculate_score(found[0], found[1])
                if score < best:
                    best = score
                    best_index = index
        return founds[best_index]

    def best_founds_score(self, founds: list[tuple[list[aoc.utils.types.Position], int]]) -> int:
        if len(founds) == 0:
            return -1
        best = self.calculate_score(founds[0][0], founds[0][1])
        for f in founds[1:]:
            score = self.calculate_score(f[0], f[1])
            if score < best:
                best = score
        return best

    def find_end(
        self,
        current: aoc.utils.types.Position,
        direction: str,
        end: aoc.utils.types.Position,
        path: list[aoc.utils.types.Position] | None = None,
        rotations: int = 0,
        visited: set[tuple[aoc.utils.types.Position, str]] | None = None,
        founds: list[tuple[list[aoc.utils.types.Position], int]] | None = None,
        window: curses.window | None = None,
    ) -> list[tuple[list[aoc.utils.types.Position], int]] | None:
        if path is None:
            path = []
        if visited is None:
            visited = set()
        if founds is None:
            founds = []

        if window:
            self.curse_grid(window, current, direction, end)

        # found
        if current == end:
            found_path = path + [current]
            score = self.calculate_score(found_path, rotations)
            best = self.best_founds_score(founds)
            # only interesting if better than current best
            if best == -1 or score < best:
                founds.append((found_path, rotations))
                return founds
            return founds

        # deadend
        visit = (current, direction)
        if visit in visited or self.is_wall(current):
            return founds

        # previous
        previous = None
        if path:
            previous = path[-1]

        visited.add(visit)
        path.append(current)

        # bail if too expensive
        best = self.best_founds_score(founds)
        if best != -1 and self.calculate_score(path, rotations) >= best:
            return founds

        for nv in self.neighbour_vectors(current):
            n = current + nv
            # where we just came from?
            if previous and previous == n:
                continue
            new_direction = vector_to_direction[nv]
            new_visit = (n, new_direction)
            if new_visit not in visited:
                rotation_delta = direction_to_rotations(direction, new_direction)
                founds = self.find_end(
                    n, new_direction, end, path=path[:], rotations=rotations + rotation_delta, visited=visited.copy(), founds=founds, window=window
                )

        return founds

    def run(self) -> int:
        score = 0
        # window = curses.initscr()
        # founds = self.find_end(self.start, 'E', self.end, window=window)
        # curses.endwin()
        founds = self.find_end(self.start, 'E', self.end)
        found = self.best_founds(founds)
        if found:
            score = self.calculate_score(found[0], found[1])
        return score


def lines_to_grid(lines: list[str]) -> Grid:
    grid = []
    start = end = aoc.utils.types.Position(0, 0)
    for row_index, row in enumerate(lines):
        line = []
        for column_index, c in enumerate(row):
            if c not in ('S', 'E'):
                line.append(c)
            else:
                if c == 'S':
                    start = aoc.utils.types.Position(column_index, row_index)
                else:
                    end = aoc.utils.types.Position(column_index, row_index)
                line.append('.')
        grid.append(line)
    return Grid(grid, start, end)


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(16)
    # lines = aoc.utils.data.day_test_lines(16)

    grid = lines_to_grid(lines)
    return grid.run()


def part2() -> int:
    return 0


def main() -> None:
    sys.setrecursionlimit(10**4)
    lines = ['day16:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
