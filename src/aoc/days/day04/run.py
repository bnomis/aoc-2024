#!/usr/bin/env python
from __future__ import annotations

from typing import Optional

import aoc.utils.data

directions = [
    [1, 0],
    [1, 1],
    [0, 1],
    [-1, 1],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
]


def grid_to_width_height(grid: list[str]) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def point_to_neighbours(grid: list[str], point: list[int]) -> list[list[int]]:
    grid_width, grid_height = grid_to_width_height(grid)
    max_x = grid_width - 1
    max_y = grid_height - 1
    start_x = point[0]
    start_y = point[1]
    possible = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            if x == 0 and y == 0:
                continue
            new_x = start_x + x
            new_y = start_y + y
            if new_x < 0 or new_x > max_x:
                continue
            if new_y < 0 or new_y > max_y:
                continue
            possible.append([new_x, new_y])
    return possible


def is_a(grid: list[str], x: int, y: int, target: str) -> bool:
    return grid[y][x] == target


def point_is_a(grid: list[str], point: list[int], target: str) -> bool:
    return is_a(grid, point[0], point[1], target)


def find_word(grid: list[str], point: list[int], word: str) -> int:
    c = word[0]
    if not point_is_a(grid, point, c):
        return 0

    # found, end
    if len(word) == 1:
        return 1

    new_word = word[1:]
    total = 0
    for neighbour in point_to_neighbours(grid, point):
        total += find_word(grid, neighbour, new_word)
    return total


class FoundException(Exception):
    pass


def point_in_path(path: list[list[int]], point: list[int]) -> bool:
    return any(p == point for p in path)


def point_in_found_paths(found_paths: list[list[list[int]]], point: list[int]) -> bool:
    return any(point_in_path(p, point) for p in found_paths)


def path_to_word(grid: list[str], path: list[list[int]]) -> list[str]:
    word = []
    for p in path:
        word.append(grid[p[1]][p[0]])
    return word


def find_word_part(
    grid: list[str],
    point: list[int],
    word: str,
    found_paths: list[list[list[int]]],
    path: Optional[list[list[int]]] = None,
) -> tuple[int, list[list[list[int]]]]:
    path = path or []
    c = word[0]
    if not point_is_a(grid, point, c):
        return 0, found_paths

    path.append(point)

    # found, end
    if len(word) == 1:
        print(f'{path} {path_to_word(grid, path)}')
        found_paths.append(path)
        return 1, found_paths

    new_word = word[1:]
    neighbours = point_to_neighbours(grid, point)
    for neighbour in neighbours:
        if point_in_path(path, neighbour):
            continue

        if point_in_found_paths(found_paths, neighbour):
            continue

        found, found_paths = find_word_part(grid, neighbour, new_word, found_paths, path=path[:])
        if found > 0:
            return 1, found_paths
    return 0, found_paths


def part1() -> int:
    grid = aoc.utils.data.day_test_lines(4)
    grid_width, grid_height = grid_to_width_height(grid)
    count = 0
    found_paths = []
    for row_index in range(grid_height):
        for line_index in range(grid_width):
            found, found_paths = find_word_part(grid, [line_index, row_index], 'XMAS', found_paths)
            count += found
    return count


def part2() -> int:
    count = 0
    return count


def main() -> None:
    lines = ['day04:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
