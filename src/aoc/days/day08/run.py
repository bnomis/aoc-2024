#!/usr/bin/env python
from __future__ import annotations

import itertools

import aoc.utils.data


def parse_grid(grid: list[list[str]]) -> dict:
    locations = {}
    for row, line in enumerate(grid):
        for column, c in enumerate(line):
            if c == '.':
                continue
            if c not in locations:
                locations[c] = []
            locations[c].append([column, row])
    return locations


def pair_nodes(pair: list[list[int]], grid_width: int, grid_height: int) -> list[list[int]]:
    a = pair[0]
    b = pair[1]
    a_x = a[0]
    a_y = a[1]
    b_x = b[0]
    b_y = b[1]

    delta_x = abs(a_x - b_x)
    delta_y = abs(a_y - b_y)

    if delta_x == 0 and delta_y == 0:
        return []

    if delta_x == 0:
        node1_x = node2_x = a_x
    if delta_y == 0:
        node1_y = node2_y = a_y

    node1_x = node1_y = node2_x = node2_y = 0
    if delta_x > 0:
        if a_x < b_x:
            node1_x = a_x - delta_x
            node2_x = b_x + delta_x
        else:
            node1_x = a_x + delta_x
            node2_x = b_x - delta_x

    if delta_y > 0:
        if a_y < b_y:
            node1_y = a_y - delta_y
            node2_y = b_y + delta_y
        else:
            node1_y = a_y - delta_y
            node2_y = b_y + delta_y

    nodes = []
    if node1_x >= 0 and node1_x < grid_width and node1_y >= 0 and node1_y < grid_height:
        nodes.append([node1_x, node1_y])
    if node2_x >= 0 and node2_x < grid_width and node2_y >= 0 and node2_y < grid_height:
        nodes.append([node2_x, node2_y])

    return nodes


def resonant_nodes(pair: list[list[int]], grid_width: int, grid_height: int) -> list[list[int]]:
    nodes = []

    a = pair[0]
    b = pair[1]
    a_x = a[0]
    a_y = a[1]
    b_x = b[0]
    b_y = b[1]

    delta_x = abs(a_x - b_x)
    delta_y = abs(a_y - b_y)

    if delta_x == 0 and delta_y == 0:
        return []

    # vertical line
    if delta_x == 0:
        if a_y < b_y:
            y = a_y
        else:
            y = b_y
        start_y = y
        # up
        while y < grid_height:
            nodes.append([a_x, y])
            y += delta_y
        # down
        y = start_y - delta_y
        while y >= 0:
            nodes.append([a_x, y])
            y -= delta_y
        return nodes

    # horizontal line
    if delta_y == 0:
        if a_x < b_x:
            x = a_x
        else:
            x = b_x
        start_x = x
        # right
        while x < grid_width:
            nodes.append([x, a_y])
            x += delta_x
        # left
        x = start_x - delta_x
        while x >= 0:
            nodes.append([x, a_y])
            x -= delta_x
        return nodes

    # diagonal

    # a above b
    if a_y < b_y:
        x = a_x
        y = a_y
        # a left of b
        if a_x < b_x:
            # moving down right
            while x < grid_width and y < grid_height:
                nodes.append([x, y])
                x += delta_x
                y += delta_y
            # moving up left
            x = a_x - delta_x
            y = a_y - delta_y
            while x >= 0 and y >= 0:
                nodes.append([x, y])
                x -= delta_x
                y -= delta_y
        # a right of b
        else:
            # moving down left
            while x >= 0 and y < grid_height:
                nodes.append([x, y])
                x -= delta_x
                y += delta_y
            # moving up right
            x = a_x + delta_x
            y = a_y - delta_y
            while x < grid_width and y >= 0:
                nodes.append([x, y])
                x += delta_x
                y -= delta_y
    # b above a
    else:
        x = b_x
        y = b_y
        # b left of a
        if b_x < a_x:
            # moving down right
            while x < grid_width and y < grid_height:
                nodes.append([x, y])
                x += delta_x
                y += delta_y
            # moving up left
            x = b_x - delta_x
            y = b_y - delta_y
            while x >= 0 and y >= 0:
                nodes.append([x, y])
                x -= delta_x
                y -= delta_y
        # b right of a
        else:
            # moving down left
            while x >= 0 and y < grid_height:
                nodes.append([x, y])
                x -= delta_x
                y += delta_y
            # moving up right
            x = b_x + delta_x
            y = b_y - delta_y
            while x < grid_width and y >= 0:
                nodes.append([x, y])
                x += delta_x
                y -= delta_y

    # print(f'pair: {pair}')
    # print(f'nodes: {nodes}')
    return nodes


def find_nodes(grid: list[list[str]], locations: dict, resonant: bool = False) -> list[list[int]]:
    grid_width = len(grid[0])
    grid_height = len(grid)
    nodes = []
    for c in locations:
        for pair in itertools.combinations(locations[c], 2):
            if resonant:
                nn = resonant_nodes(pair, grid_width, grid_height)
            else:
                nn = pair_nodes(pair, grid_width, grid_height)
            for n in nn:
                if n not in nodes:
                    nodes.append(n)
    return nodes


def print_nodes(grid: list[list[str]], nodes: list[list[int]]) -> None:
    for n in nodes:
        grid[n[1]][n[0]] = '#'
    for row in grid:
        print(''.join(row))


def part1() -> int:
    grid = aoc.utils.data.day_input_grid(8)
    locations = parse_grid(grid)
    nodes = find_nodes(grid, locations)
    return len(nodes)


def part2() -> int:
    grid = aoc.utils.data.day_input_grid(8)
    locations = parse_grid(grid)
    nodes = find_nodes(grid, locations, resonant=True)
    # print_nodes(grid, nodes)
    return len(nodes)


def main() -> None:
    lines = ['day08:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
