#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


def is_even(index: int) -> bool:
    return index % 2 == 0


class Disk:
    def __init__(self, state: str) -> None:
        self.state = state
        self.map = []
        self.spaces = []
        self.state_to_map(state)

    def state_to_map(self, state: str) -> list[str]:
        disk_map = []
        spaces = []
        files = []
        for index, c in enumerate(state):
            file = is_even(index)
            file_id = int(index / 2)
            length = int(c)
            map_len = len(disk_map)
            if not file:
                parts = ['.']
                for i in range(map_len, map_len + length):
                    spaces.append(i)
            else:
                parts = [file_id]
                for i in range(map_len, map_len + length):
                    files.append(i)
            disk_map.extend(parts * length)

        self.map = disk_map
        self.spaces = spaces
        self.files = files
        return disk_map

    def print_map(self) -> None:
        print(self.map)

    def print_spaces(self) -> None:
        print(f'spaces: {self.spaces}')

    def print_files(self) -> None:
        print(f'files:  {self.files}')

    def print(self, step: int) -> None:
        print(step)
        self.print_map()
        self.print_spaces()
        self.print_files()

    def defraged(self) -> bool:
        index = self.spaces[0]
        for s in self.spaces:
            if s != index:
                return False
            index += 1
        return True

    def defrag(self) -> None:
        step = 0
        while not self.defraged():
            # self.print(step)
            left_space_index = self.spaces[0]
            right_file_index = self.files[-1]
            right_file = self.map[right_file_index]
            self.map[left_space_index] = right_file
            self.map[right_file_index] = '.'
            self.spaces.pop(0)
            self.spaces.append(right_file_index)
            self.spaces = sorted(self.spaces)
            self.files.pop()
            self.files.append(left_space_index)
            self.files = sorted(self.files)
            step += 1
        # self.print(step)

    def checksum(self) -> int:
        total = 0
        for index, file_id in enumerate(self.map):
            if file_id == '.':
                break
            total += (index * file_id)
        return total


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(9)
    disk = Disk(lines[0])
    disk.defrag()
    return disk.checksum()


def part2() -> int:
    return 0


def main() -> None:
    lines = ['day09:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
