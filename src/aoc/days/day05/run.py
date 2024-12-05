#!/usr/bin/env python
from __future__ import annotations

import aoc.utils.data


def parse_rules(lines: list[str]) -> dict:
    # rules[X]['before'] = a list of ints X must be before
    # rules[X]['after'] = a list of ints X must be after
    rules = {}
    for line in lines:
        before, after = line.split('|')
        before = int(before)
        after = int(after)
        if before not in rules:
            rules[before] = {
                'before': [],
                'after': [],
            }
        if after not in rules:
            rules[after] = {
                'before': [],
                'after': [],
            }
        rules[before]['before'].append(after)
        rules[after]['after'].append(before)
    return rules


def parse_updates(lines: list[str]) -> list[list[int]]:
    updates = []
    for line in lines:
        ints = []
        for i in line.split(','):
            ints.append(int(i))
        updates.append(ints)
    return updates


def split_input(lines: list[str]) -> tuple[list[str], list[str]]:
    rules = []
    updates = []
    line_length = len(lines)
    updates_start = 0
    for i in range(line_length):
        line = lines[i]
        if not line:
            updates_start = i + 1
            break
        rules.append(line)

    for u in range(updates_start, line_length):
        updates.append(lines[u])

    return rules, updates


def order_ok(rules: dict, before: int, after: int) -> bool:
    if before in rules and after in rules[before]['after']:
        return False

    if after in rules and before in rules[after]['before']:  # noqa: SIM103
        return False

    return True


def passes_before_rules(rules: dict, page: int, befores: list[int]) -> bool:
    return all(order_ok(rules, b, page) for b in befores)


def passes_after_rules(rules: dict, page: int, afters: list[int]) -> bool:
    return all(order_ok(rules, page, a) for a in afters)


def passes_rules(rules: dict, updates: list[int]) -> bool:
    updates_length = len(updates)
    for i in range(updates_length):
        page = updates[i]
        before = updates[0:i]
        after = updates[i+1:updates_length]
        passes_before = passes_before_rules(rules, page, before)
        if not passes_before:
            return False

        passes_after = passes_after_rules(rules, page, after)
        if not passes_after:
            return False

    return True


def filter_updates(rules: dict, updates: list[list[int]]) -> list[list[int]]:
    filtered = []
    for u in updates:
        if passes_rules(rules, u):
            filtered.append(u)
    return filtered


def filter_bad_updates(rules: dict, updates: list[list[int]]) -> list[list[int]]:
    filtered = []
    for u in updates:
        if not passes_rules(rules, u):
            filtered.append(u)
    return filtered


def fix_an_issue(rules: dict, updates: list[int]) -> list[int]:
    updates_length = len(updates)
    for i in range(updates_length):
        page = updates[i]
        befores = updates[0:i]
        for before_index, b in enumerate(befores):
            if b in rules and page in rules[b]['after']:
                updates[i] = b
                updates[before_index] = page
                return updates

        afters = updates[i + 1 : updates_length]
        for after_index, a in enumerate(afters):
            if a in rules and page in rules[a]['before']:
                updates[i] = a
                updates[i + 1 + after_index] = page
                return updates

    return updates


def fix_update(rules: dict, updates: list[int]) -> list[int]:
    if passes_rules(rules, updates):
        return updates

    fixed = fix_an_issue(rules, updates)
    return fix_update(rules, fixed)


def fix_updates(rules: dict, updates: list[list[int]]) -> list[list[int]]:
    fixed = []
    for u in updates:
        fixed.append(fix_update(rules, u))
    return fixed


def print_rules(rules: dict) -> None:
    pages = sorted(rules.keys())
    for p in pages:
        print(f'{p} before {rules[p]["before"]}')
        print(f'{p} after {rules[p]["after"]}')


def part1() -> int:
    lines = aoc.utils.data.day_input_lines(5)
    rule_lines, update_lines = split_input(lines)
    rules = parse_rules(rule_lines)
    updates = parse_updates(update_lines)
    updates = filter_updates(rules, updates)
    count = 0
    for u in updates:
        mid = int(len(u) / 2)
        count += u[mid]
    return count


def part2() -> int:
    lines = aoc.utils.data.day_input_lines(5)
    rule_lines, update_lines = split_input(lines)
    rules = parse_rules(rule_lines)
    updates = parse_updates(update_lines)
    updates = filter_bad_updates(rules, updates)
    updates = fix_updates(rules, updates)
    count = 0
    for u in updates:
        mid = int(len(u) / 2)
        count += u[mid]
    return count


def main() -> None:
    lines = ['day05:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
