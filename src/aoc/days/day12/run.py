#!/usr/bin/env python
from __future__ import annotations

import aoc.types
import aoc.utils.data
import aoc.utils.grid

"""
Corners == Sides

A
- no neighbours, 4 corners = 4 sides

AA
- each has
- one neighbour, 2 corners x 2 = 4 sides

AAA
- consider centre A
-- two opposite neighbours, 0 corners
- at end each has one neighbour, 2 corners x 2 = 4 sides

XA
AA
- top, one neighbour, 2 corners
- bottom left, one neighbour, 2 corners
- bottom right, two neighbours, 2 corners if X!=A else 1
= 6 sides

XAX
AAA
- top = 2
- bottom left = 2
- bottom right = 2
- bottom mid, 3 neighbours,
-- 2 corners if Xs != A
-- 1 corner if 1 X = A
-- 0 if both Xs == A

AAA
AAA
- top left, 2 neighbours, corners = 1
- top mid, 3 neighbours, corners = 0
- top right, 2 neighbours, corners = 1
- bottom left, 2 neighbours, corners = 1
- bottom mid, 3 neighbours, corners = 0
- bottom right, 2 neighbours, corners = 1

XAX
AAA
xAX
- top = 2
- mid left = 2
- centre, 4 neighbours, 4 corners
- mid right = 2
- bottom = 2
= 12 sides

neighbours -> corners
0: 4
1: 2
2: 0
3: 2
4: 4
"""


def opposites(points: list[aoc.types.Point]) -> bool:
    a = points[0]
    b = points[1]
    return a.x == b.x or a.y == b.y


def gap_is(
    grid: list[list[str]],
    points: list[aoc.types.Point],
    plant: str,
) -> bool:
    min_x = max_x = points[0].x
    min_y = max_y = points[0].y
    for p in points[1:]:
        if p.x < min_x:
            min_x = p.x
        if p.x > max_x:
            max_x = p.x
        if p.y < min_y:
            min_y = p.y
        if p.y > max_y:
            max_y = p.y
    gap = None
    for x in [min_x, max_x]:
        for y in [min_y, max_y]:
            p = aoc.types.Point(x, y)
            if p not in points:
                gap = p
                break
    return aoc.utils.grid.char_at_point(grid, gap) == plant


def find_gaps(points: list[aoc.types.Point]) -> list[aoc.types.Point]:
    min_x = max_x = points[0].x
    min_y = max_y = points[0].y
    for p in points[1:]:
        if p.x < min_x:
            min_x = p.x
        if p.x > max_x:
            max_x = p.x
        if p.y < min_y:
            min_y = p.y
        if p.y > max_y:
            max_y = p.y
    gaps = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = aoc.types.Point(x, y)
            if p not in points:
                gaps.append(p)
    return gaps


def count_of_plants_in_gaps(
    grid: list[list[str]],
    points: list[aoc.types.Point],
    plant: str,
) -> int:
    gaps = find_gaps(points)
    chars = aoc.utils.grid.chars_at_points(grid, gaps)
    # print(f'{plant} {points} {gaps} {chars}')
    count = 0
    for c in chars:
        if c == plant:
            count += 1
    return count


def compass_opposites(neighbours: list[str]):
    return ('N' in neighbours and 'S' in neighbours) or ('W' in neighbours and 'E' in neighbours)


def inside_corner(neighbours: list[str]):
    combs = [
        ['N', 'E', 'NE'],
        ['N', 'W', 'NW'],
        ['S', 'E', 'SE'],
        ['S', 'W', 'SW'],
    ]
    for c in combs:
        presents = []
        for p in c:
            presents.append(p in neighbours)
        if all(presents):
            return True
    return False


def all_points(neighbours: list[str]):
    return 'N' in neighbours and 'S' in neighbours and 'W' in neighbours and 'E' in neighbours


def count_corner_compass(neighbours: list[str]) -> int:
    count = 0
    if 'NE' in neighbours:
        count += 1
    if 'NW' in neighbours:
        count += 1
    if 'SE' in neighbours:
        count += 1
    if 'SW' in neighbours:
        count += 1
    return count


def missing_compass(four_compass_neighbours: list[str]) -> str:
    for c in ['N', 'S', 'E', 'W']:
        if c not in four_compass_neighbours:
            return c
    raise Exception('nothing missing')


def is_block(four_compass_neighbours, compass_neighbours) -> bool:
    missing = missing_compass(four_compass_neighbours)
    missing_to_corners = {
        'N': ['SW', 'SE'],
        'S': ['NW', 'NE'],
        'E': ['NW', 'SW'],
        'W': ['NE', 'SE'],
    }
    presents = []
    for c in missing_to_corners[missing]:
        presents.append(c in compass_neighbours)
    return all(presents)


def compass_opposite(cin: str) -> str:
    opps = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E',
    }
    return opps[cin]


def t_diag(cin: str) -> list[str]:
    diags = {
        'N': ['NE', 'NW'],
        'S': ['SE', 'SW'],
        'E': ['SE', 'NE'],
        'W': ['SW', 'NW'],
    }
    return diags[cin]


def t_corners(four_compass_neighbours, compass_neighbours) -> int:
    missing = missing_compass(four_compass_neighbours)
    opp = compass_opposite(missing)
    count = 0
    for d in t_diag(opp):
        if d in compass_neighbours:
            count += 1
    if count == 0:
        return 2
    if count == 1:
        return 1
    return 0


def all_corners(four_compass_neighbours, compass_neighbours) -> int:
    corners = 0
    if 'N' in four_compass_neighbours and 'E' in four_compass_neighbours and 'NE' not in compass_neighbours:
        corners += 1
    if 'N' in four_compass_neighbours and 'W' in four_compass_neighbours and 'NW' not in compass_neighbours:
        corners += 1
    if 'S' in four_compass_neighbours and 'E' in four_compass_neighbours and 'SE' not in compass_neighbours:
        corners += 1
    if 'S' in four_compass_neighbours and 'W' in four_compass_neighbours and 'SW' not in compass_neighbours:
        corners += 1
    return corners


class Region:
    def __init__(self, plant: str, points: list[aoc.types.Point]) -> None:
        self.plant = plant
        self.points = points
        self._perimeter_path = []
        self._border_cells = []

    def __str__(self) -> str:
        lines = [self.plant]
        for p in self.points:
            lines.append(f'[{p.x}, {p.y}]')
        return '\n'.join(lines)

    def area(self) -> int:
        return len(self.points)

    def perimeter_path(self, grid: list[list[str]]) -> list[aoc.types.Point]:
        if not self._perimeter_path:
            perimeter = []
            for p in self.points:
                if aoc.utils.grid.point_is_on_grid_edge(grid, p):
                    perimeter.append(p)
                    continue
                for n in aoc.utils.grid.neighbours(grid, p):
                    if aoc.utils.grid.char_at_point(grid, n) != self.plant:
                        perimeter.append(p)
                        break
            self._perimeter_path = perimeter
        return self._perimeter_path

    def perimeter_length(self, grid: list[list[str]]) -> int:
        length = 0
        for p in self.perimeter_path(grid):
            edges = aoc.utils.grid.point_grid_edge_count(grid, p)
            for n in aoc.utils.grid.neighbours(grid, p):
                if aoc.utils.grid.char_at_point(grid, n) != self.plant:
                    edges += 1
            length += edges
        return length

    def border_cells(self, grid: list[list[str]]) -> list[aoc.types.Point]:
        if not self._border_cells:
            border = []
            for p in self.points:
                if aoc.utils.grid.point_is_on_grid_edge(grid, p):
                    border.append(p)
                    continue
                for n in aoc.utils.grid.all_neighbours(grid, p):
                    if aoc.utils.grid.char_at_point(grid, n) != self.plant:
                        border.append(p)
                        break
            self._border_cells = border
        return self._border_cells

    def sides(self, grid: list[list[str]]) -> int:
        total = 0
        for p in self.border_cells(grid):
            compass_neighbours = aoc.utils.grid.compass_neighbours(grid, p)
            four_compass_neighbours = aoc.utils.grid.four_compass_neighbours(grid, p)
            neighbour_count = len(four_compass_neighbours)

            sides = 0
            if neighbour_count == 0:
                sides = 4
            elif neighbour_count == 1:
                sides = 2
            elif neighbour_count == 2:
                if compass_opposites(compass_neighbours):
                    # XXX
                    sides = 0
                else:
                    if inside_corner(compass_neighbours):
                        sides = 1
                    else:
                        # outside corner
                        # XX
                        # X
                        sides = 2
            elif neighbour_count in (3, 4):
                # consider top middle X
                # XXX
                #  X
                # 2 corners
                # XXX
                # XX
                # 1 corner
                # XXX
                # XXX
                # 0 corners
                # XX
                # XXX
                # X
                # 2 corners
                # XX
                # XXX
                #   X
                # 2 corners
                sides = all_corners(four_compass_neighbours, compass_neighbours)
            else:
                raise Exception(f'{self.plant} {p} neighbours {neighbour_count}')

            # print(f'{self.plant} {p} neighbours {neighbour_count} corner {compass_corner_count} sides {sides}')
            total += sides
        # print(f'{self.plant} sides {total}')
        return total


def region_points(
    grid: list[list[str]],
    plant: str,
    points: list[aoc.types.Point],
    visited: list[aoc.types.Point],
) -> tuple[list[aoc.types.Point], list[aoc.types.Point]]:
    current = points[-1]
    unvisited_neighbours = []
    for n in aoc.utils.grid.neighbours(grid, current):
        if n in visited:
            continue
        if aoc.utils.grid.char_at_point(grid, n) == plant:
            unvisited_neighbours.append(n)
    for n in unvisited_neighbours:
        if n in visited:
            continue
        points.append(n)
        visited.append(n)
        points, visited = region_points(grid, plant, points, visited)

    return points, visited


def find_region(grid: list[list[str]], point: aoc.types.Point, visited: list[aoc.types.Point]) -> tuple[Region, list[aoc.types.Point]]:
    plant = aoc.utils.grid.char_at_point(grid, point)
    visited.append(point)
    points = [point]
    points, visited = region_points(grid, plant, points, visited)
    region = Region(plant, points)
    return region, visited


def grid_to_regions(grid: list[list[str]]) -> list[Region]:
    regions = []
    visited = []
    for row_index, row in enumerate(grid):
        for column_index, _ in enumerate(row):
            p = aoc.types.Point(column_index, row_index)
            if p in visited:
                continue
            region, visited = find_region(grid, p, visited)
            regions.append(region)
    return regions


def part1() -> int:
    grid = aoc.utils.data.day_input_grid(12)
    regions = grid_to_regions(grid)
    total = 0
    for r in regions:
        total += r.area() * r.perimeter_length(grid)
    return total


def part2() -> int:
    grid = aoc.utils.data.day_input_grid(12)
    regions = grid_to_regions(grid)
    total = 0
    for r in regions:
        total += r.area() * r.sides(grid)
    return total


def main() -> None:
    lines = ['day12:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
