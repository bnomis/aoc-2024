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

left_right_vectors = [aoc.utils.types.Position(-1, 0), aoc.utils.types.Position(1, 0)]
up_down_vectors = [aoc.utils.types.Position(0, -1), aoc.utils.types.Position(0, 1)]


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

    def nodes(self) -> list[aoc.utils.types.Position]:
        nodes = []
        for row_index, row in enumerate(self.grid):
            for column_index, c in enumerate(row):
                if c == '#':
                    continue
                nodes.append(aoc.utils.types.Position(column_index, row_index))
        return nodes

    def internal_walls(self) -> list[aoc.utils.types.Position]:
        walls = []
        for y in range(1, self.max_height):
            for x in range(1, self.max_width):
                c = self.grid[y][x]
                if c == '#':
                    walls.append(aoc.utils.types.Position(x, y))
        return walls

    def neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def neighbours_with_walls(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_inside_grid(new_position):
                ns.append(new_position)
        return ns

    def neighbours_that_are_walls(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_inside_grid(new_position) and self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def neighbours_vectors_that_are_walls(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_inside_grid(new_position) and self.is_wall(new_position):
                ns.append(v)
        return ns

    def neighbours_remove(
        self,
        position: aoc.utils.types.Position,
        removables: list[aoc.utils.types.Position],  # list of removable walls
        remover: dict[aoc.utils.types.Position, list[aoc.utils.types.Position]],  # dict of walls with where they came from) -> list[aoc.utils.types.Position]:
    ) -> tuple[list[aoc.utils.types.Position], aoc.utils.types.Position | None]:
        ns = []
        removed = None
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_inside_grid(new_position):
                if self.is_space(new_position):
                    ns.append(new_position)
                elif not removed and new_position in removables:  # noqa: SIM102
                    through_position = new_position + v
                    if self.is_space(through_position):  # noqa: SIM102
                        if new_position not in remover or position not in remover[new_position]:
                            removed = new_position
        return ns, removed

    def neighbour_vectors(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in direction_to_vector.values():
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(v)
        return ns

    def left_right_neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in left_right_vectors:
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def up_down_neighbours(self, position: aoc.utils.types.Position) -> list[aoc.utils.types.Position]:
        ns = []
        for v in up_down_vectors:
            new_position = position + v
            if self.is_in_grid(new_position) and not self.is_wall(new_position):
                ns.append(new_position)
        return ns

    def is_inside_grid(self, position: aoc.utils.types.Position) -> bool:
        return position.x >= 1 and position.x < self.max_width and position.y >= 1 and position.y < self.max_height

    def is_in_grid(self, position: aoc.utils.types.Position) -> bool:
        return position.x >= 0 and position.x < self.width and position.y >= 0 and position.y < self.height

    def is_wall(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '#'

    def is_space(self, position: aoc.utils.types.Position) -> bool:
        return self.grid[position.y][position.x] == '.'

    def are_spaces(self, positions: list[aoc.utils.types.Position]) -> bool:
        return all([self.is_space(p) for p in positions])

    def shortest_path(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
    ) -> tuple[list[aoc.utils.types.Position] | None, dict]:
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
            return path[::-1], distances
        return None, distances

    def shortest_path_remove(
        self,
        start: aoc.utils.types.Position,
        end: aoc.utils.types.Position,
        removables: list[aoc.utils.types.Position],  # list of removable walls
        remover: dict[aoc.utils.types.Position, list[aoc.utils.types.Position]],  # dict of walls with where they came from
        max_len: float = 0,
    ) -> tuple[list[aoc.utils.types.Position] | None, dict[aoc.utils.types.Position, list[aoc.utils.types.Position]], list[aoc.utils.types.Position]]:
        # holds the wall and next position
        removed = []
        # costs
        distances = {}
        previous = {}
        if max_len == 0:
            max_len = float('inf')
        for n in self.nodes():
            distances[n] = max_len
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
            removed_pos = None
            if removed:
                neighbours = self.neighbours(current_pos)
            else:
                neighbours, removed_pos = self.neighbours_remove(current_pos, removables, remover)

            # through a wall
            if removed_pos:
                # add to remover
                if removed_pos not in remover:
                    remover[removed_pos] = []
                remover[removed_pos].append(current_pos)

                # moving through wall
                vector = removed_pos - current_pos
                final_pos = removed_pos + vector
                # removed 1,2
                removed = [removed_pos, final_pos]

                distance = current_distance + 1
                distances[removed_pos] = distance
                previous[removed_pos] = current_pos
                # heapq.heappush(pq, (distance, removed_pos))

                distance += 1
                if distance < distances[final_pos]:
                    distances[final_pos] = distance
                    previous[final_pos] = removed_pos
                    heapq.heappush(pq, (distance, final_pos))

            # other neighbours
            for next_pos in neighbours:
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
            return path[::-1], remover, removed
        return None, remover, removed

    def find_removables(self) -> list[aoc.utils.types.Position]:
        removables = []
        for w in self.internal_walls():
            ns = self.left_right_neighbours(w)
            if len(ns) == 2 and self.are_spaces(ns):
                removables.append(w)
                continue
            ns = self.up_down_neighbours(w)
            if len(ns) == 2 and self.are_spaces(ns):
                removables.append(w)
                continue
        return removables

    # this works but is, of course, too slow
    def find_cheats(self, min_save: int) -> int:
        base_path, _ = self.shortest_path(self.start, self.end)
        if not base_path:
            raise Exception('no path')
        base_path_length = len(base_path) - 1
        removables = self.find_removables()
        remover = {}
        saved = {}
        max_len = base_path_length - min_save
        while True:
            path, remover, removed = self.shortest_path_remove(self.start, self.end, removables, remover, max_len)
            if not removed:
                break
            if path:
                path_length = len(path) - 1
                saving = base_path_length - path_length
                if saving not in saved:
                    saved[saving] = []
                saved[saving].append(removed)

        total = 0
        for s in sorted(saved.keys()):
            count = len(saved[s])
            print(f'{s}: {count}')
            if s >= min_save:
                total += count
        return total

    def find_cheats2(self, min_save: int) -> int:
        base_path, distances = self.shortest_path(self.start, self.end)
        if not base_path:
            raise Exception('no path')
        # go along path finding walls to walk through which shorten the total
        savings = {}
        for p in base_path:
            for nv in self.neighbours_vectors_that_are_walls(p):
                # through wall to space on path
                dest = p + (nv * 2)
                if self.is_space(dest) and dest in base_path:
                    current_cost = distances[p]
                    jumped_cost = current_cost + 2
                    original_cost = distances[dest]
                    if jumped_cost < original_cost:
                        saved = original_cost - jumped_cost
                        if min_save == 0 or saved >= min_save:
                            if saved not in savings:
                                savings[saved] = []
                            savings[saved].append([p + nv, dest])
        total = 0
        for s in sorted(savings.keys()):
            count = len(savings[s])
            # print(f'{s}: {count}')
            if s >= min_save:
                total += count
        return total

    def find_cheats3(self, min_save: int, max_cheat_length: int) -> int:
        base_path, distances = self.shortest_path(self.start, self.end)
        if not base_path:
            raise Exception('no path')

        base_path_length = len(base_path)
        # go along path finding walls to walk through which shorten the total
        savings = {}
        for s in range(base_path_length):
            current_position = base_path[s]
            current_cost = distances[current_position]
            for e in range(s + 1, base_path_length):
                dest_position = base_path[e]
                original_cost = distances[dest_position]
                cheat_distance = current_position.distance(dest_position)
                if cheat_distance <= max_cheat_length:
                    jump_cost = current_cost + cheat_distance
                    saved = original_cost - jump_cost
                    if saved >= min_save:
                        cheat = (current_position, dest_position)
                        if saved not in savings:
                            savings[saved] = set()
                        savings[saved].add(cheat)

        total = 0
        for s in sorted(savings.keys()):
            count = len(savings[s])
            # print(f'{s}: {count}')
            if s >= min_save:
                total += count
        return total


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
    # return 0
    # lines = aoc.utils.data.day_test_lines(20, which=0)
    # grid = lines_to_grid(lines)
    # return grid.find_cheats2(0)
    lines = aoc.utils.data.day_input_lines(20)
    grid = lines_to_grid(lines)
    return grid.find_cheats2(100)


def part2() -> int:
    # return 0
    # lines = aoc.utils.data.day_test_lines(20, which=0)
    # grid = lines_to_grid(lines)
    # return grid.find_cheats3(50, 20)
    lines = aoc.utils.data.day_input_lines(20)
    grid = lines_to_grid(lines)
    return grid.find_cheats3(100, 20)


def main() -> None:
    lines = ['20:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
