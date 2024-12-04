#!/usr/bin/env python
from __future__ import annotations

from typing import Optional

import aoc.utils.data


def grid_to_width_height(grid: list[list[str]]) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def is_a(grid: list[list[str]], x: int, y: int, target: str) -> bool:
    return grid[y][x] == target


def point_is_a(grid: list[list[str]], point: list[int], target: str) -> bool:
    return is_a(grid, point[0], point[1], target)


def path_to_word(grid: list[list[str]], path: list[list[int]]) -> list[str]:
    word = []
    for p in path:
        word.append(grid[p[1]][p[0]])
    return word


def add_direction_to_point(
    grid: list[list[str]],
    point: list[int],
    direction: list[int],
) -> Optional[list[int]]:
    grid_width, grid_height = grid_to_width_height(grid)
    max_x = grid_width - 1
    max_y = grid_height - 1
    x = point[0] + direction[0]
    y = point[1] + direction[1]
    if x < 0 or x > max_x or y < 0 or y > max_y:
        return None
    return [x, y]


def directional_word_search(
    grid: list[list[str]],
    point: list[int],
    word: str,
    direction: list[int],
    path: Optional[list[list[int]]] = None,
) -> tuple[int, list[list[int]]]:
    path = path or []
    c = word[0]
    # dead end
    if not point_is_a(grid, point, c):
        return 0, path

    path.append(point)
    # found end
    if len(word) == 1:
        # print(f'{path} {path_to_word(grid, path)}')
        return 1, path

    next_point = add_direction_to_point(grid, point, direction)
    if not next_point:
        return 0, path

    new_word = word[1:]
    return directional_word_search(grid, next_point, new_word, direction, path=path[:])


def char_at_point(
    grid: list[list[str]],
    point: list[int],
) -> str:
    x = point[0]
    y = point[1]
    if x < 0 or y < 0:
        return ''
    grid_width, grid_height = grid_to_width_height(grid)
    max_x = grid_width - 1
    max_y = grid_height - 1
    if x > max_x or y > max_y:
        return ''
    return grid[y][x]


def points_to_chars(
    grid: list[list[str]],
    points: list[list[int]],
) -> list[str]:
    chars = []
    for p in points:
        chars.append(char_at_point(grid, p))
    return chars


def x_points(
    grid: list[list[str]],
    point: list[int],
) -> list[str]:
    x = point[0]
    y = point[1]
    points = [
        [x - 1, y - 1],
        [x + 1, y - 1],
        [x - 1, y + 1],
        [x + 1, y + 1],
    ]
    return points_to_chars(grid, points)


def is_xmas(
    grid: list[list[str]],
    point: list[int],
) -> bool:
    chars = x_points(grid, point)
    p1 = chars[0] + chars[3]
    p2 = chars[1] + chars[2]
    return p1 in ['MS', 'SM'] and p2 in ['MS', 'SM']


def part1() -> int:
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
    grid = aoc.utils.data.day_input_grid(4)
    grid_width, grid_height = grid_to_width_height(grid)
    count = 0
    found_paths = []
    for row_index in range(grid_height):
        for line_index in range(grid_width):
            if is_a(grid, line_index, row_index, 'X'):
                found = 0
                for d in directions:
                    found, path = directional_word_search(grid, [line_index, row_index], 'XMAS', d)
                    if found:
                        found_paths.append(path)
                        count += 1
    return count


def part2() -> int:
    grid = aoc.utils.data.day_input_grid(4)
    grid_width, grid_height = grid_to_width_height(grid)
    count = 0
    for row_index in range(grid_height):
        for line_index in range(grid_width):
            if is_a(grid, line_index, row_index, 'A') and is_xmas(grid, [line_index, row_index]):
                count += 1
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
