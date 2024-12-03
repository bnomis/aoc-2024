from __future__ import annotations

import pathlib


def data_dir() -> pathlib.Path:
    root_dir = pathlib.Path(__file__).absolute().parent.parent.parent.parent
    return root_dir / 'data'


def day_data_dir(day: int) -> pathlib.Path:
    day_dir = 'day%02d' % day
    return data_dir() / day_dir


def day_data_path(day: int, filename: str) -> pathlib.Path:
    return day_data_dir(day) / filename


def day_input_path(day: int) -> pathlib.Path:
    return day_data_path(day, 'input.txt')


def day_test_path(day: int, which: int = 0) -> pathlib.Path:
    if which == 0:
        return day_data_path(day, 'test.txt')
    return day_data_path(day, f'test{which}.txt')
