#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


def value(grid: list[list[int]], point: list[int]) -> int:
    return grid[point[1]][point[0]]


def neighbours(grid: list[list[int]], point: list[int]) -> list[list[int]]:
    ns = []
    grid_width = len(grid[0])
    grid_height = len(grid)
    px = point[0]
    py = point[1]
    if px > 0:
        ns.append([px - 1, py])
    if px < grid_width - 1:
        ns.append([px + 1, py])
    if py > 0:
        ns.append([px, py - 1])
    if py < grid_height - 1:
        ns.append([px, py + 1])
    return ns


def climb(grid: list[list[int]], current: list[int], summits: list[list[int]] | None = None) -> list[list[int]]:
    summits = summits or []
    current_value = value(grid, current)
    if current_value == 9:
        if current not in summits:
            summits.append(current)
        return summits

    next_value = current_value + 1
    for n in neighbours(grid, current):
        if value(grid, n) == next_value:
            summits = climb(grid, n, summits=summits)
    return summits


def find(grid: list[list[int]], path: list[list[int]], found: list[list[list[int]]] | None = None) -> list[list[list[int]]]:
    found = found or []
    current_value = value(grid, path[-1])
    if current_value == 9:
        if path not in found:
            found.append(path)
        return found

    next_value = current_value + 1
    for n in neighbours(grid, path[-1]):
        if value(grid, n) == next_value:
            new_path = path[:]
            new_path.append(n)
            found = find(grid, new_path, found=found)
    return found


def part1() -> int:
    grid = aoc.utils.data.day_input_grid_ints(10)
    summits = []
    for row_index, row in enumerate(grid):
        for column_index, column in enumerate(row):
            if column == 0:
                found = climb(grid, [column_index, row_index])
                if found:
                    summits.extend(found)
    return len(summits)


def part2() -> int:
    grid = aoc.utils.data.day_input_grid_ints(10)
    paths = {}
    for row_index, row in enumerate(grid):
        for column_index, column in enumerate(row):
            if column == 0:
                point = [column_index, row_index]
                path = [point]
                found = find(grid, path)
                paths[f'{column_index},{row_index}'] = found
    total = 0
    for _, v in paths.items():
        total += len(v)
    return total


def main() -> None:
    lines = ['day10:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
