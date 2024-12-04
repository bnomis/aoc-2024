from __future__ import annotations

import pathlib

import aoc.utils.paths


def readlines(path: pathlib.Path) -> list[str]:
    lines = []
    with path.open() as fp:
        for line in fp.readlines():
            lines.append(line.strip())
    return lines


def readlines_ints(path: pathlib.Path) -> list[list[int]]:
    lines = []
    for line in readlines(path):
        ints = []
        for p in line.split():
            ip = p.strip()
            if ip:
                ints.append(int(ip))
        if ints:
            lines.append(ints)
    return lines


def day_input_lines(day: int) -> list[str]:
    return readlines(aoc.utils.paths.day_input_path(day))


def day_test_lines(day: int, which: int = 0) -> list[str]:
    return readlines(aoc.utils.paths.day_test_path(day, which=which))


def day_input_grid(day: int) -> list[list[str]]:
    lines = []
    for line in readlines(aoc.utils.paths.day_input_path(day)):
        lines.append(list(line))
    return lines


def day_test_grid(day: int, which: int = 0) -> list[list[str]]:
    lines = []
    for line in readlines(aoc.utils.paths.day_test_path(day, which=which)):
        lines.append(list(line))
    return lines


def day_input_ints(day: int) -> list[list[int]]:
    return readlines_ints(aoc.utils.paths.day_input_path(day))


def day_test_ints(day: int) -> list[list[int]]:
    return readlines_ints(aoc.utils.paths.day_test_path(day))
