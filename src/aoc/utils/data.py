from __future__ import annotations

import pathlib

import aoc.utils.paths


def readlines(path: pathlib.Path) -> list[str]:
    with path.open() as fp:
        lines = fp.readlines()
    return lines


def day_input_lines(day: int) -> list[str]:
    return readlines(aoc.utils.paths.day_input_path(day))


def day_test_lines(day: int) -> list[str]:
    return readlines(aoc.utils.paths.day_test_path(day))
