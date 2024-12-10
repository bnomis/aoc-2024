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
        self.files = []
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


class Disk2:
    def __init__(self, state: str) -> None:
        self.state = state
        self.files = {}
        self.spaces = {}
        self.map_state(state)

    def map_state(self, state: str) -> None:
        files = {}
        spaces = {}
        start = 0
        for index, c in enumerate(state):
            file = is_even(index)
            file_id = int(index / 2)
            length = int(c)
            if length == 0:
                continue

            if file:
                files[file_id] = {
                    'start': start,
                    'length': length
                }
            else:
                spaces[file_id] = {
                    'start': start,
                    'length': length,
                }
            start += length

        self.files = files
        self.spaces = spaces
        # self.print()

    def print(self) -> None:
        self.print_files()
        self.print_spaces()
        self.print_map()

    def print_files(self) -> None:
        print('files')
        for fid in sorted(self.files.keys()):
            f = self.files[fid]
            print(f'  {fid}: {f["start"]} {f["length"]}')

    def print_spaces(self) -> None:
        print('spaces')
        for fid in sorted(self.spaces.keys()):
            f = self.spaces[fid]
            print(f'  {fid}: {f["start"]} {f["length"]}')

    def print_map(self) -> None:
        mapper = {}
        for k, v in self.files.items():
            index = v['start']
            for i in range(v['length']):
                mapper[index + i] = str(k)
        for _, v in self.spaces.items():
            index = v['start']
            for i in range(v['length']):
                mapper[index + i] = '.'
        out = []
        for k in sorted(mapper.keys()):
            out.append(mapper[k])
        print(''.join(out))

    def print_gaps(self, gaps) -> None:
        print('gaps')
        for k in sorted(gaps.keys()):
            print(f'  {k}: {gaps[k]}')

    def spaces_to_gaps(self, spaces) -> dict:
        gaps = {}
        space_ids = sorted(spaces.keys())
        for sid in space_ids:
            length = spaces[sid]['length']
            if length not in gaps:
                gaps[length] = []
            gaps[length].append(sid)
        return gaps

    def coalesce_spaces(self, spaces):
        new_spaces = {}
        new_space_id = 0
        sps = sorted(spaces.values(), key=lambda x: x['start'])
        spaces = {}
        for index, s in enumerate(sps):
            spaces[index] = s
        space_ids = sorted(spaces.keys())
        sid_index = 0
        sid_length = len(space_ids)
        while sid_index < sid_length:
            sid = space_ids[sid_index]
            space_start = spaces[sid]['start']
            space_length = spaces[sid]['length']
            next_sid_index = sid_index + 1
            while next_sid_index < sid_length:
                next_sid = space_ids[next_sid_index]
                if spaces[next_sid]['start'] != space_start + space_length:
                    break

                space_length += spaces[next_sid]['length']
                next_sid_index += 1

            sid_index = next_sid_index
            new_spaces[new_space_id] = {
                'start': space_start,
                'length': space_length,
            }
            new_space_id += 1

        return new_spaces

    def defrag(self):
        # print('-- defrag --')
        file_ids = sorted(self.files.keys(), reverse=True)
        for fid in file_ids:
            # print(f'before file: {fid}')
            self.spaces = self.coalesce_spaces(self.spaces)
            # self.print()

            gaps = self.spaces_to_gaps(self.spaces)
            # self.print_gaps(gaps)

            # no gaps left
            if len(gaps) == 0:
                break

            file_start = self.files[fid]['start']
            file_length = self.files[fid]['length']
            gap_lengths = sorted(gaps.keys())

            # no gap big enough for file
            if gap_lengths[-1] < file_length:
                # print('no space')
                continue

            # find first gap big enough
            found = False
            space = 0
            for space in sorted(self.spaces.keys()):
                if self.spaces[space]['length'] >= file_length:
                    found = True
                    break

            if not found:
                continue

            space_start = self.spaces[space]['start']

            # dont move right
            if space_start > file_start:
                continue

            # move file
            self.files[fid]['start'] = space_start
            # use up space
            remaining = self.spaces[space]['length'] - file_length
            if remaining == 0:
                self.spaces.pop(space)
            else:
                self.spaces[space]['start'] += file_length
                self.spaces[space]['length'] = remaining
            last_space_id = sorted(self.spaces.keys(), reverse=True)[0]
            # space left by removing file
            self.spaces[last_space_id + 1] = {
                'start': file_start,
                'length': file_length,
            }
            # print(f'after file: {fid}')
            # self.print()
        # self.print()

    def checksum(self) -> int:
        total = 0
        for fid in sorted(self.files.keys()):
            if fid == 0:
                continue
            start = self.files[fid]['start']
            for i in range(self.files[fid]['length']):
                total += (fid * (start + i))
        return total


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(9)
    disk = Disk(lines[0])
    disk.defrag()
    return disk.checksum()


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(9)
    disk = Disk2(lines[0])
    disk.defrag()
    return disk.checksum()


def main() -> None:
    lines = ['day09:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
