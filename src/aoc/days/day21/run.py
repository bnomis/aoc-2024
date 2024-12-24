#!/usr/bin/env python
from __future__ import annotations

import heapq

import aoc.utils.data
import aoc.utils.types

numeric_positions = {
    '7': aoc.utils.types.Position(1, 1),
    '8': aoc.utils.types.Position(2, 1),
    '9': aoc.utils.types.Position(3, 1),
    '4': aoc.utils.types.Position(1, 2),
    '5': aoc.utils.types.Position(2, 2),
    '6': aoc.utils.types.Position(3, 2),
    '1': aoc.utils.types.Position(1, 3),
    '2': aoc.utils.types.Position(2, 3),
    '3': aoc.utils.types.Position(3, 3),
    '0': aoc.utils.types.Position(2, 4),
    'A': aoc.utils.types.Position(3, 4),
}

position_to_numeric = {
    aoc.utils.types.Position(1, 1): '7',
    aoc.utils.types.Position(2, 1): '8',
    aoc.utils.types.Position(3, 1): '9',
    aoc.utils.types.Position(1, 2): '4',
    aoc.utils.types.Position(2, 2): '5',
    aoc.utils.types.Position(3, 2): '6',
    aoc.utils.types.Position(1, 3): '1',
    aoc.utils.types.Position(2, 3): '2',
    aoc.utils.types.Position(3, 3): '3',
    aoc.utils.types.Position(2, 4): '0',
    aoc.utils.types.Position(3, 4): 'A',
}

directional_positions = {
    '^': aoc.utils.types.Position(2, 1),
    'A': aoc.utils.types.Position(3, 1),
    '<': aoc.utils.types.Position(1, 2),
    'v': aoc.utils.types.Position(2, 2),
    '>': aoc.utils.types.Position(3, 2),
}

position_to_direction = {
    aoc.utils.types.Position(2, 1): '^',
    aoc.utils.types.Position(3, 1): 'A',
    aoc.utils.types.Position(1, 2): '<',
    aoc.utils.types.Position(2, 2): 'v',
    aoc.utils.types.Position(3, 2): '>',
}

direction_to_vector = {
    '^': aoc.utils.types.Position(0, -1),
    '<': aoc.utils.types.Position(-1, 0),
    'v': aoc.utils.types.Position(0, 1),
    '>': aoc.utils.types.Position(1, 0),
}

vector_to_direction = {
    aoc.utils.types.Position(0, -1): '^',
    aoc.utils.types.Position(-1, 0): '<',
    aoc.utils.types.Position(0, 1): 'v',
    aoc.utils.types.Position(1, 0): '>',
}

numeric_moves = {}
directional_moves = {}


# this works but only finds one path
# which may not give the shortest in the next phase
def press(
    start: aoc.utils.types.Position,
    end: aoc.utils.types.Position,
    avoid: list[aoc.utils.types.Position],
) -> list[str]:
    # print(f'{start} -> {end}')
    moves = []
    current = start
    xp = yp = '|'
    xv = yv = aoc.utils.types.Position(0, 0)
    if end.x < start.x:
        xp = '<'
    elif end.x > start.x:
        xp = '>'
    if end.y < start.y:
        yp = '^'
    elif end.y > start.y:
        yp = 'v'
    if xp != '|':
        xv = direction_to_vector[xp]
    if yp != '|':
        yv = direction_to_vector[yp]
    # print(f'{xv} {yv}')
    while current != end:
        # print(f'{current}')
        if current.x != end.x:
            nextp = current + xv
            if nextp not in avoid:
                moves.append(xp)
                current = nextp
                continue

        if current.y != end.y:
            nextp = current + yv
            if nextp not in avoid:
                moves.append(yp)
                current = nextp

    moves.append('A')
    return moves


test_sequences = {
    '029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
    '980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
    '179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
    '456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
    '379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
}


def line_to_number(line: str) -> int:
    ns = []
    for c in line:
        if c.isdigit():
            ns.append(c)
    return int(''.join(ns))


class Grid:
    def __init__(
        self,
        grid: list[list[str]],
    ) -> None:
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.max_width = self.width - 1
        self.max_height = self.height - 1

    def is_in_grid(self, position: aoc.utils.types.Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def is_wall(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def dijkstra(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> list[list[aoc.utils.types.Position]]:
        # priority queue
        pq = [(0, start)]
        paths = {
            start: [(0, None)],
        }

        while pq:
            current_cost, current_pos = heapq.heappop(pq)

            # found
            if current_pos == end:
                return self.backtrack(paths, current_pos)

            for n in self.neighbours(current_pos):
                cost = current_cost + 1

                # new node or cheaper that what we currently have
                if n not in paths or cost <= min(p[0] for p in paths[n]):
                    if n not in paths:
                        paths[n] = []
                    else:
                        # filter existing paths which are the same cost
                        paths[n] = [p for p in paths[n] if p[0] == cost]
                    # add the new path
                    paths[n].append((cost, current_pos))
                    heapq.heappush(pq, (cost, n))

        # not found
        return []

    def backtrack(
        self,
        paths: dict[aoc.utils.types.Position, list],
        end: aoc.utils.types.Position,
    ) -> list[list[aoc.utils.types.Position]]:
        def reconstruct_paths(current, path) -> list[list[aoc.utils.types.Position]]:
            # None if the start
            if current is None:
                # reverse
                return [path[::-1]]
            # all_paths is a list containing a list
            # so we use extend rather than append
            # to get the contents (the list in the list)
            all_paths = []
            for _, prev in paths[current]:
                all_paths.extend(reconstruct_paths(prev, path + [current]))
            return all_paths

        return reconstruct_paths(end, [])


def lines_to_grid(lines: list[str]) -> Grid:
    grid = []
    for row in lines:
        line = []
        for c in row:
            line.append(c)
        grid.append(line)
    return Grid(grid)


def make_numeric_grid() -> Grid:
    return lines_to_grid(aoc.utils.data.day_file_lines(21, 'numeric.txt'))


def make_directional_grid() -> Grid:
    return lines_to_grid(aoc.utils.data.day_file_lines(21, 'directional.txt'))


def paths_to_moves(paths: list[list[aoc.utils.types.Position]]) -> set[str]:
    movers = set()
    for p in paths:
        moves = []
        for i in range(len(p) - 1):
            current = p[i]
            nextp = p[i + 1]
            vector = nextp - current
            moves.append(vector_to_direction[vector])
        movers.add(''.join(moves))
    return movers


def numbers_to_moves(numbers: str, start: str = 'A') -> list[str]:
    s = start + numbers
    str_length = len(s)
    accumulator = [[]]
    for i in range(str_length - 1):
        new_accumulator = []
        moves = numeric_moves[s[i]][s[i + 1]]
        for a in accumulator:
            for m in moves:
                b = a[:]
                b.append(m)
                b.append('A')
                new_accumulator.append(b)
        accumulator = new_accumulator

    out = []
    for a in accumulator:
        out.append(''.join(a))
    return out


def moves_to_moves(moves: str, start: str = 'A') -> list[str]:
    s = start + moves
    str_length = len(s)
    accumulator = [[]]
    for i in range(str_length - 1):
        new_accumulator = []
        moves = directional_moves[s[i]][s[i + 1]]
        for a in accumulator:
            for m in moves:
                b = a[:]
                b.append(m)
                b.append('A')
                new_accumulator.append(b)
        accumulator = new_accumulator

    out = []
    for a in accumulator:
        out.append(''.join(a))
    return out


def sequence_to_moves_orig(sequence: str) -> str:
    # numeric
    moves = numbers_to_moves(sequence)
    # print(moves)

    # directional
    moves1 = set()
    for m in moves:
        mset = set(moves_to_moves(m))
        moves1 |= mset

    # find shortest
    lengths = []
    for m in moves1:
        lengths.append(len(m))
    min_len = sorted(lengths)[0]
    short_moves = []
    for m in moves1:
        if len(m) == min_len:
            short_moves.append(m)

    # directional
    moves2 = set()
    for m in short_moves:
        mset = set(moves_to_moves(m))
        moves2 |= mset

    # find shortest
    lengths = []
    for m in moves2:
        lengths.append(len(m))
    min_len = sorted(lengths)[0]
    short_moves2 = []
    for m in moves2:
        if len(m) == min_len:
            short_moves2.append(m)

    # print(short_moves2)
    return short_moves2[0]


def sequence_to_moves(sequence: str, numerics: int = 2) -> str:
    # numeric
    moves = numbers_to_moves(sequence)
    # print(moves)

    # directional
    for _ in range(numerics):
        moves1 = set()
        for m in moves:
            mset = set(moves_to_moves(m))
            moves1 |= mset

        # find shortest
        lengths = []
        for m in moves1:
            lengths.append(len(m))
        min_len = sorted(lengths)[0]
        short_moves = []
        for m in moves1:
            if len(m) == min_len:
                short_moves.append(m)
        moves = short_moves

    # print(short_moves2)
    return moves[0]


def sequence_pairs_to_moves(sequence: str, numerics: int = 2) -> str:
    s = 'A' + sequence
    sequence_length = len(s)
    accumulator = []
    for i in range(sequence_length - 1):
        shorter = s[i] + s[i + 1]
        # numeric
        moves = numbers_to_moves(shorter, start='')
        # print(moves)

        # directional
        for _ in range(numerics):
            moves1 = set()
            for m in moves:
                mset = set(moves_to_moves(m))
                moves1 |= mset

            # find shortest
            lengths = []
            for m in moves1:
                lengths.append(len(m))
            min_len = sorted(lengths)[0]
            short_moves = []
            for m in moves1:
                if len(m) == min_len:
                    short_moves.append(m)
            moves = short_moves

        # print(short_moves2)
        accumulator.append(moves[0])
    return ''.join(accumulator)


def make_numeric_moves() -> None:
    numeric_grid = make_numeric_grid()
    positions = list(position_to_numeric.keys())
    positions_length = len(positions)
    for i in range(positions_length):
        source_key = positions[i]
        source_numeric = position_to_numeric[source_key]
        numeric_moves[source_numeric] = {}
        for j in range(positions_length):
            dest_key = positions[j]
            dest_numeric = position_to_numeric[dest_key]
            numeric_moves[source_numeric][dest_numeric] = []
            if source_numeric == dest_numeric:
                numeric_moves[source_numeric][dest_numeric] = ['']
                continue
            paths = numeric_grid.dijkstra(source_key, dest_key)
            numeric_moves[source_numeric][dest_numeric] = list(paths_to_moves(paths))


def make_directional_moves() -> None:
    directional_grid = make_directional_grid()
    positions = list(position_to_direction.keys())
    positions_length = len(positions)
    for i in range(positions_length):
        source_key = positions[i]
        source_directional = position_to_direction[source_key]
        directional_moves[source_directional] = {}
        for j in range(positions_length):
            dest_key = positions[j]
            dest_directional = position_to_direction[dest_key]
            directional_moves[source_directional][dest_directional] = []
            if source_directional == dest_directional:
                directional_moves[source_directional][dest_directional] = ['']
                continue
            paths = directional_grid.dijkstra(source_key, dest_key)
            directional_moves[source_directional][dest_directional] = list(paths_to_moves(paths))


def print_moves(moves: dict, desc: str) -> None:
    print(desc)
    keys = sorted(moves.keys())
    for k in keys:
        for d in keys:
            print(f'{k} -> {d}')
            s = '\n  '.join(moves[k][d])
            print(f'  {s}')


# https://github.com/oshlern/adventofcode/blob/main/advent24/2024/python/18/concise.py
def calc_fewest(code, N_ROBOT_KEYBOARDS):
    KEY_COORDS = {c: (x, y) for y, row in enumerate([' ^A', '<v>']) for x, c in enumerate(row)}
    # Fewest of MY presses to hit kf when starting at ki (at layer 0)
    leg_lengths = {(0, ki, kf): 1 for ki in KEY_COORDS for kf in KEY_COORDS}

    # Fewest of MY presses to hit all ks when starting at A (at layer l)
    def fewest_presses(la, ks):
        return sum(leg_lengths[la, ki, kf] for ki, kf in zip('A' + ks, ks))

    for layer in range(1, N_ROBOT_KEYBOARDS + 1):
        if layer == N_ROBOT_KEYBOARDS:
            KEY_COORDS = {c: (x, y) for y, row in enumerate(['789', '456', '123', ' 0A']) for x, c in enumerate(row)}
        for ki, (xi, yi) in KEY_COORDS.items():
            for kf, (xf, yf) in KEY_COORDS.items():
                hor_ks = ('>' if xf > xi else '<') * abs(xf - xi)
                ver_ks = ('^' if yf < yi else 'v') * abs(yf - yi)
                fewest_hor_first = fewest_presses(layer - 1, hor_ks + ver_ks + 'A') if (xf, yi) != KEY_COORDS[' '] else float('inf')
                fewest_ver_first = fewest_presses(layer - 1, ver_ks + hor_ks + 'A') if (xi, yf) != KEY_COORDS[' '] else float('inf')
                leg_lengths[(layer, ki, kf)] = min(fewest_hor_first, fewest_ver_first)
    return fewest_presses(layer, code)


def part1() -> int:
    # return 0
    total = 0
    # lines = aoc.utils.data.day_test_lines(21, which=0)
    lines = aoc.utils.data.day_input_lines(21)
    for line in lines:
        moves = sequence_pairs_to_moves(line)
        moves_length = len(moves)
        num = line_to_number(line)
        total += moves_length * num
        # print(line)
        # print(moves)
        # print(f'{moves_length} {num}')
    return total


def part2_orig() -> int:
    # I give up!
    # return 0
    total = 0
    lines = aoc.utils.data.day_test_lines(21, which=0)
    # lines = aoc.utils.data.day_input_lines(21)
    for line in lines:
        print(line)
        moves = sequence_pairs_to_moves(line, numerics=25)
        moves_length = len(moves)
        num = line_to_number(line)
        total += moves_length * num
        # print(line)
        # print(moves)
        # print(f'{moves_length} {num}')
    return total


def part2() -> int:
    # return 0
    total = 0
    # lines = aoc.utils.data.day_test_lines(21, which=0)
    lines = aoc.utils.data.day_input_lines(21)
    for line in lines:
        moves_length = calc_fewest(line, 26)
        num = line_to_number(line)
        total += moves_length * num
        # print(line)
        # print(moves)
        # print(f'{moves_length} {num}')
    return total


def main() -> None:
    make_numeric_moves()
    make_directional_moves()
    # print_moves(numeric_moves, 'numeric')
    # print_moves(directional_moves, 'directional')

    lines = ['21:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
