from __future__ import annotations

import aoc.types


def neighbours(grid: list[list[str]], point: aoc.types.Point) -> list[aoc.types.Point]:
    ns = []
    grid_width = len(grid[0])
    grid_height = len(grid)
    if point.x > 0:
        ns.append(aoc.types.Point(point.x - 1, point.y))
    if point.x < grid_width - 1:
        ns.append(aoc.types.Point(point.x + 1, point.y))
    if point.y > 0:
        ns.append(aoc.types.Point(point.x, point.y - 1))
    if point.y < grid_height - 1:
        ns.append(aoc.types.Point(point.x, point.y + 1))
    return ns


def all_neighbours(grid: list[list[str]], point: aoc.types.Point) -> list[aoc.types.Point]:
    ns = []
    grid_width = len(grid[0])
    grid_height = len(grid)
    if point.x > 0:
        ns.append(aoc.types.Point(point.x - 1, point.y))
        if point.y > 0:
            ns.append(aoc.types.Point(point.x - 1, point.y - 1))
        if point.y < grid_height - 1:
            ns.append(aoc.types.Point(point.x - 1, point.y + 1))

    if point.x < grid_width - 1:
        ns.append(aoc.types.Point(point.x + 1, point.y))
        if point.y > 0:
            ns.append(aoc.types.Point(point.x + 1, point.y - 1))
        if point.y < grid_height - 1:
            ns.append(aoc.types.Point(point.x + 1, point.y + 1))

    if point.y > 0:
        ns.append(aoc.types.Point(point.x, point.y - 1))

    if point.y < grid_height - 1:
        ns.append(aoc.types.Point(point.x, point.y + 1))
    return ns


def compass_neighbours(grid: list[list[str]], point: aoc.types.Point) -> list[str]:
    ns = []
    target = grid[point.y][point.x]
    grid_width = len(grid[0])
    grid_height = len(grid)
    if point.x > 0:
        if char_at_point(grid, aoc.types.Point(point.x - 1, point.y)) == target:
            ns.append('W')
        if point.y > 0:  # noqa: SIM102
            if char_at_point(grid, aoc.types.Point(point.x - 1, point.y - 1)) == target:
                ns.append('NW')
        if point.y < grid_height - 1:  # noqa: SIM102
            if char_at_point(grid, aoc.types.Point(point.x - 1, point.y + 1)) == target:
                ns.append('SW')

    if point.x < grid_width - 1:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x + 1, point.y)) == target:
            ns.append('E')
        if point.y > 0:  # noqa: SIM102
            if char_at_point(grid, aoc.types.Point(point.x + 1, point.y - 1)) == target:
                ns.append('NE')
        if point.y < grid_height - 1:  # noqa: SIM102
            if char_at_point(grid, aoc.types.Point(point.x + 1, point.y + 1)) == target:
                ns.append('SE')

    if point.y > 0:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x, point.y - 1)) == target:
            ns.append('N')

    if point.y < grid_height - 1:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x, point.y + 1)) == target:
            ns.append('S')
    return ns


def four_compass_neighbours(grid: list[list[str]], point: aoc.types.Point) -> list[str]:
    ns = []
    target = grid[point.y][point.x]
    grid_width = len(grid[0])
    grid_height = len(grid)
    if point.x > 0:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x - 1, point.y)) == target:
            ns.append('W')

    if point.x < grid_width - 1:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x + 1, point.y)) == target:
            ns.append('E')

    if point.y > 0:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x, point.y - 1)) == target:
            ns.append('N')

    if point.y < grid_height - 1:  # noqa: SIM102
        if char_at_point(grid, aoc.types.Point(point.x, point.y + 1)) == target:
            ns.append('S')
    return ns


def char_at_point(grid: list[list[str]], point: aoc.types.Point) -> str:
    return grid[point.y][point.x]


def chars_at_points(grid: list[list[str]], points: list[aoc.types.Point]) -> list[str]:
    chars = []
    for p in points:
        chars.append(char_at_point(grid, p))
    return chars


def point_is_on_grid_edge(grid: list[list[str]], point: aoc.types.Point) -> bool:
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    return point.x == 0 or point.y == 0 or point.x == max_x or point.y == max_y


def point_grid_edge_count(grid: list[list[str]], point: aoc.types.Point) -> int:
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    count = 0
    if point.x == 0:
        count += 1
    if point.y == 0:
        count += 1
    if point.x == max_x:
        count += 1
    if point.y == max_y:
        count += 1
    return count
