#!/usr/bin/env python
from __future__ import annotations

import collections
import curses
import heapq
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


class Node:
    def __init__(self, position: aoc.utils.types.Position, direction: str, cost: int) -> None:
        self.position = position
        self.direction = direction
        self.cost = cost

    def __lt__(self, other: Node) -> bool:
        return self.cost < other.cost

    def __gt__(self, other: Node) -> bool:
        return self.cost > other.cost

    def __eq__(self, other: Node) -> bool:  # type: ignore
        return self.cost == other.cost

    def __hash__(self) -> int:
        return hash((self.position.x, self.position.y, self.direction))


class NodePath(Node):
    def __init__(self, position: aoc.utils.types.Position, direction: str, cost: int, path: list[aoc.utils.types.Position]) -> None:
        super().__init__(position, direction, cost)
        self.path = path


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

    def print_grid_with_tiles(self, tiles: set[aoc.utils.types.Position]) -> None:
        lines = []
        for _, row in enumerate(self.grid):
            line = []
            i = 0
            while i < self.width:
                c = row[i]
                line.append(c)
                i += 1
            lines.append(line)
        for t in tiles:
            lines[t.y][t.x] = 'O'
        print('\n'.join([''.join(li) for li in lines]))

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

    def neighbour_vectors_directioned(self, direction: str) -> list[aoc.utils.types.Position]:
        ns = [
            direction_to_vector[direction],
            direction_to_vector[direction_rotate_left(direction)],
            direction_to_vector[direction_rotate_right(direction)],
        ]
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

    # this works but is slow for the real input data
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

    def run_recurse(self) -> int:
        score = 0
        # window = curses.initscr()
        # founds = self.find_end(self.start, 'E', self.end, window=window)
        # curses.endwin()
        founds = self.find_end(self.start, 'E', self.end)
        found = self.best_founds(founds)
        if found:
            score = self.calculate_score(found[0], found[1])
        return score

    def heuristic(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> int:
        return abs(start.x - end.x) + abs(start.y - end.y)

    def nodes(self) -> list[aoc.utils.types.Position]:
        nodes = []
        for row_index, row in enumerate(self.grid):
            for column_index, c in enumerate(row):
                if c == '#':
                    continue
                nodes.append(aoc.utils.types.Position(column_index, row_index))
        return nodes

    def cost_to_move(
        self,
        start: Node,
        end: aoc.utils.types.Position,
        new_direction: str,
    ) -> int:
        rotations = direction_to_rotations(start.direction, new_direction)
        return 1 + (1000 * rotations)

    # ask grok for an astar example
    def astar(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> tuple[list[aoc.utils.types.Position], int]:
        # init scores for all nodes to max
        g_score = {}
        for node in self.nodes():
            g_score[node] = float('inf')
        # but be clever about starting node
        g_score[start] = 0

        # keep track
        open_list = []
        closed_list = set()
        came_from = {}

        # cost from start to end
        start_h = self.heuristic(start, end)
        heapq.heappush(open_list, Node(start, 'E', start_h))

        # loopy
        while open_list:
            current_node = heapq.heappop(open_list)
            current = current_node.position

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path, current_node.cost

            closed_list.add(current)

            for nv in self.neighbour_vectors(current):
                n = current + nv
                new_direction = vector_to_direction[nv]
                tentative_g_score = g_score[current] + self.cost_to_move(current_node, n, new_direction)
                if n in closed_list and tentative_g_score >= g_score[n]:
                    continue

                if tentative_g_score < g_score[n] or n not in [ol.position for ol in open_list]:
                    came_from[n] = current
                    g_score[n] = tentative_g_score
                    f_score = g_score[n] + self.heuristic(n, end)
                    heapq.heappush(open_list, Node(n, new_direction, f_score))

        # not found
        return [], 0

    def cost_string(self, costs: list) -> str:
        cp = []
        for p in costs:
            cp.append(f'[{str(p[1])} {p[0]}]')
        return ', '.join(cp)

    def dijkstra(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> list[list[aoc.utils.types.Position]]:
        # this is a modified dijkstra to return all the best path costs
        paths = {
            start: [(0, None)],
        }
        # priority queue
        pq = [Node(start, 'E', 0)]
        all_paths = []
        while pq:
            current_node = heapq.heappop(pq)
            current = current_node.position

            # found
            if current == end:
                print('found')
                all_paths.append(self.backtrack(paths, end))
                continue
                return self.backtrack(paths, end)

            current_cost = current_node.cost
            for nv in self.neighbour_vectors(current):
                n = current + nv

                new_direction = vector_to_direction[nv]
                new_cost = current_cost + self.cost_to_move(current_node, end, new_direction)

                # new node or cheaper that what we currently have
                if n not in paths or new_cost <= min(p[0] for p in paths[n]):
                    if n not in paths:
                        paths[n] = []
                    else:
                        # filter existing paths which are the same cost
                        paths[n] = [p for p in paths[n] if p[0] == new_cost]
                    # add the new path
                    paths[n].append((new_cost, current))
                    heapq.heappush(pq, Node(n, new_direction, new_cost))

        # not found
        return all_paths

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

    def dijkstra_all_paths(self, start, end):
        # https://github.com/elklepo/aoc/blob/main/2024/day16/xpl.py
        all_shortest_paths = []
        min_cost = float('inf')
        # priority queue
        pq = [NodePath(start, 'E', 0, [start])]
        path_costs = collections.defaultdict(lambda: float('inf')) | {start: 0}

        while pq:
            current_node = heapq.heappop(pq)
            cost = current_node.cost
            if cost > min_cost:
                break

            current = current_node.position
            path = current_node.path
            if current == end:
                if cost < min_cost:
                    min_cost = cost
                    all_shortest_paths = [path]
                elif cost == min_cost:
                    all_shortest_paths.append(path)
                continue

            current_direction = current_node.direction
            for nv in self.neighbour_vectors_directioned(current_direction):
                n = current + nv
                new_direction = vector_to_direction[nv]
                # new_cost = cost + self.cost_to_move(current_node, end, new_direction)
                new_cost = cost + 1

                if new_cost <= path_costs[n]:
                    path_costs[n] = new_cost
                    heapq.heappush(pq, NodePath(n, new_direction, new_cost, path + [n]))
        return all_shortest_paths, min_cost

    def dijkstra3(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ):
        # https://www.reddit.com/r/adventofcode/comments/1hfboft/comment/m2e4uhy/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
        current_node = NodePath(start, 'E', 0, [start])
        work = [current_node]
        best_costs = {current_node: 0}
        best_end_cost = 0
        best_seats = set()

        while work:
            current_node = heapq.heappop(work)
            current_position = current_node.position
            current_direction = current_node.direction
            current_path = current_node.path
            current_cost = current_node.cost
            if current_position == end:
                best_seats |= {*current_path}
                best_end_cost = current_cost
            elif best_end_cost == 0 or current_cost < best_end_cost:
                for nv in self.neighbour_vectors_directioned(current_direction):
                    new_position = current_position + nv
                    new_direction = vector_to_direction[nv]
                    new_cost = current_cost + self.cost_to_move(current_node, end, new_direction)
                    new_node = NodePath(new_position, new_direction, new_cost, current_path + [new_position])
                    if new_node not in best_costs or best_costs[new_node] >= new_cost:
                        best_costs[new_node] = new_cost
                        heapq.heappush(work, new_node)

        return best_end_cost, best_seats

    def dijkstra4(
        self,
        startp: aoc.utils.types.Position,
        endp: aoc.utils.types.Position,
    ):
        # https://www.reddit.com/r/adventofcode/comments/1hfboft/comment/m2e4uhy/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
        start = (startp.x, startp.y)
        end = (endp.x, endp.y)
        work = [(0, (start,), 1, 0)]
        best_costs = {(*start, 1, 0): 0}
        best_end_cost = 0
        best_seats = set()

        while work:
            cost, path, dx, dy = heapq.heappop(work)
            x, y = pos = path[-1]
            if pos == end:
                best_seats |= {*path}
                best_end_cost = cost
            elif not best_end_cost or cost < best_end_cost:
                for ncost, nx, ny, ndx, ndy in (
                    (cost + 1, x + dx, y + dy, dx, dy),  # straight
                    (cost + 1000, x, y, dy, -dx),  # left
                    (cost + 1000, x, y, -dy, dx),  # right
                ):
                    pos = nx, ny, ndx, ndy
                    if self.grid[ny][nx] != '#' and best_costs.get(pos, ncost + 1) >= ncost:
                        best_costs[pos] = ncost
                        heapq.heappush(work, (ncost, path + ((nx, ny),), ndx, ndy))

        return best_end_cost, best_seats

    def run(self) -> int:
        path, cost = self.astar(self.start, self.end)
        if path:
            return cost
        return 0

    def run2(self) -> int:
        _, best_seats = self.dijkstra4(self.start, self.end)
        return len(best_seats)


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


def part1_recurse() -> int:
    lines = aoc.utils.data.day_input_lines(16)
    # lines = aoc.utils.data.day_test_lines(16)

    grid = lines_to_grid(lines)
    return grid.run_recurse()


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(16)
    # lines = aoc.utils.data.day_test_lines(16, which=2)

    grid = lines_to_grid(lines)
    return grid.run()


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(16)
    # lines = aoc.utils.data.day_test_lines(16, which=2)

    grid = lines_to_grid(lines)
    return grid.run2()


def main() -> None:
    sys.setrecursionlimit(10**5)
    lines = ['day16:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
