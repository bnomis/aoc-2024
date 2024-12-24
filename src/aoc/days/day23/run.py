#!/usr/bin/env python
from __future__ import annotations

import itertools

import aoc.utils.data


def find_triangles(graph) -> list[tuple[str]]:
    triangles = []
    for node in graph:
        neighbors = graph[node]
        for pair in itertools.combinations(neighbors, 2):
            if pair[1] in graph[pair[0]]:
                triangles.append(tuple(sorted([node, pair[0], pair[1]])))

    # Remove duplicates since we might count the same triangle multiple times from different nodes
    return list(set(triangles))


def lines_to_adj_list(lines: list[str]) -> dict:
    graph = {}
    for line in lines:
        a, b = line.split('-')
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def find_largest_connected_set(graph):
    def dfs(node, visited):
        stack = [node]
        component = []
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.append(current)
                stack.extend(neighbor for neighbor in graph[current] if neighbor not in visited)
        return component

    visited = set()
    largest_component = []
    for node in graph:
        if node not in visited:
            component = dfs(node, visited)
            if len(component) > len(largest_component):
                largest_component = component

    return largest_component


def find_largest_clique(graph):
    nodes = list(graph.keys())

    def is_clique(subset):
        return all(all(j in graph[i] for j in subset if i != j) for i in subset)

    largest_clique = []
    for r in range(len(nodes), 0, -1):  # Start from the largest possible size
        for subset in itertools.combinations(nodes, r):
            if is_clique(subset):
                return list(subset)  # Found a clique, no need to continue if we want the largest
        if r < len(largest_clique):  # If we've gone below our current largest clique size, stop
            break

    return largest_clique


def bron_kerbosch(R, P, X, graph):
    """
    R: Current clique being extended
    P: Set of nodes that could potentially be added to the current clique
    X: Set of nodes already examined
    """
    if not P and not X:
        # If P and X are empty, R is a maximal clique
        yield set(R)
        return

    # Choose a pivot to reduce the size of P
    pivot = next(iter(P.union(X))) if P or X else None
    for v in P - graph[pivot]:  # For all nodes in P not adjacent to the pivot
        yield from bron_kerbosch(R + [v], P.intersection(graph[v]), X.intersection(graph[v]), graph)
        P.remove(v)
        X.add(v)


def find_all_cliques(graph):
    nodes = set(list(graph.keys()))

    # Convert to sets for efficient operations
    graph = {node: set(neighbors) for node, neighbors in graph.items()}

    cliques = list(bron_kerbosch([], nodes, set(), graph))

    # Find the largest clique among all maximal cliques
    largest_clique = max(cliques, key=len, default=[])  # Default to empty list if no cliques found

    return largest_clique


def part1() -> int:
    # return 0
    total = 0
    # lines = aoc.utils.data.day_test_lines(23)
    lines = aoc.utils.data.day_input_lines(23)
    graph = lines_to_adj_list(lines)
    triangles = find_triangles(graph)
    for t in triangles:
        for n in t:
            if n[0] == 't':
                total += 1
                break
    return total


def part2() -> str:
    # return ''
    # lines = aoc.utils.data.day_test_lines(23)
    lines = aoc.utils.data.day_input_lines(23)
    graph = lines_to_adj_list(lines)
    largest_component = find_all_cliques(graph)
    return ','.join(sorted(largest_component))


def main() -> None:
    lines = ['23:']
    p1 = part1()
    lines.append(f'part 1: {p1}')
    p2 = part2()
    lines.append(f'part 2: {p2}')
    print('\n  '.join(lines))


if __name__ == '__main__':
    main()
