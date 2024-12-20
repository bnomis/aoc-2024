#!/usr/bin/env python
from __future__ import annotations

import heapq

import aoc.utils.data
import aoc.utils.types

direction_to_vector = {
    'N': aoc.utils.types.Position(0, -1),
    'S': aoc.utils.types.Position(0, 1),
    'E': aoc.utils.types.Position(1, 0),
    'W': aoc.utils.types.Position(-1, 0),
}


class Grid:
    def __init__(self, bites: list[aoc.utils.types.Position], size: int, fallen: int) -> None:
        self.bites = bites
        self.size = size
        self.fallen = fallen
        self.width = size
        self.height = size
        self.max_width = size - 1
        self.max_height = size - 1
        self.grid = self.make_grid()

    def make_grid(self) -> list[list[str]]:
        grid = []
        for _ in range(self.size):
            line = []
            for _ in range(self.size):
                line.append('.')
            grid.append(line)
        for i in range(self.fallen):
            pos = self.bites[i]
            grid[pos.y][pos.x] = '#'
        return grid

    def nodes(self) -> list[aoc.utils.types.Position]:
        nodes = []
        for row_index, row in enumerate(self.grid):
            for column_index, c in enumerate(row):
                if c == '#':
                    continue
                nodes.append(aoc.utils.types.Position(column_index, row_index))
        return nodes

    def neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def is_in_grid(self, position: aoc.utils.types.Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def is_wall(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def shortest_path(self) -> list[aoc.utils.types.Position] | None:
        start = aoc.utils.types.Position(0, 0)
        end = aoc.utils.types.Position(self.max_width, self.max_height)

        # init

        # costs
        distances = {}
        previous = {}
        for n in self.nodes():
            distances[n] = float('inf')
            previous[n] = None
        distances[start] = 0

        # priority queue
        pq = [(0, start)]
        found = False
        while pq:
            current_distance, current_pos = heapq.heappop(pq)

            # If we've reached the end, we can stop
            if current_pos == end:
                found = True
                break

            # If the distance we have is greater than what we've already processed, skip
            if current_distance > distances[current_pos]:
                continue

            # Check all four directions
            for next_pos in self.neighbours(current_pos):
                distance = current_distance + 1
                if distance < distances[next_pos]:
                    distances[next_pos] = distance
                    previous[next_pos] = current_pos
                    heapq.heappush(pq, (distance, next_pos))

        if found:
            # Reconstruct the path
            path = []
            current = end
            while current:
                path.append(current)
                current = previous[current]
            return path[::-1]
        return None


def lines_to_bites(lines: list[str]) -> list[aoc.utils.types.Position]:
    bites = []
    for line in lines:
        x, y = line.split(',')
        bites.append(aoc.utils.types.Position(int(x), int(y)))
    return bites


def part1() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(18, which=0)
    lines = aoc.utils.data.day_input_lines(18)
    bites = lines_to_bites(lines)
    # grid = Grid(bites, 7, 12)
    grid = Grid(bites, 71, 1024)
    path = grid.shortest_path()
    if path:
        return len(path) - 1
    return 0


def part2() -> str:
    # return 0
    # lines = aoc.utils.data.day_test_lines(18, which=0)
    lines = aoc.utils.data.day_input_lines(18)
    bites = lines_to_bites(lines)
    blocked = False
    # fallen = 13
    fallen = 1025
    size = 71
    while not blocked:
        grid = Grid(bites, size, fallen)
        path = grid.shortest_path()
        if not path:
            break
        fallen += 1
    return str(bites[fallen - 1])


def main() -> None:
    lines = ['day18:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
