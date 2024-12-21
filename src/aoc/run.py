#!/usr/bin/env python
from __future__ import annotations

import datetime
import importlib


def run_day(day: int) -> None:
    module_name = 'aoc.days.day%02d.run' % day
    mod = importlib.import_module(module_name)
    mod.main()


def main() -> None:
    print('Advent of code 2024')
    today = datetime.date.today()
    xmas = datetime.date(2024, 12, 25)
    end = 25
    if today < xmas:
        end = today.day

    for day in range(1, end + 1):
        try:
            run_day(day)
        except:
            print(f'Failed on day {day}')
            break


if __name__ == '__main__':
    main()
