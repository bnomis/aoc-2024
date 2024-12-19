import heapq

# asked grok to give an example using dijkstra


def dijkstra_all_shortest_paths(grid, start, end):
    rows, cols = len(grid), len(grid[0])

    # Dictionary to hold all shortest paths to each node
    # (distance, previous_node)
    paths = {tuple(start): [(0, None)]}

    pq = [(0, start)]  # priority queue

    while pq:
        current_distance, (x, y) = heapq.heappop(pq)

        if (x, y) == end:
            # We've reached the end, now backtrack to find all shortest paths
            all_paths = backtrack(paths, end)
            return all_paths

        for dx, dy in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]:  # assuming no diagonal movement
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'obstacle':
                new_distance = current_distance + 1

                if (nx, ny) not in paths or new_distance <= min(path[0] for path in paths[(nx, ny)]):
                    # If this new path is either the first path to this node or is among the shortest
                    if (nx, ny) in paths:
                        paths[(nx, ny)] = [p for p in paths[(nx, ny)] if p[0] == new_distance]
                    else:
                        paths[(nx, ny)] = []

                    paths[(nx, ny)].append((new_distance, (x, y)))
                    heapq.heappush(pq, (new_distance, (nx, ny)))

    return []  # No path found


def backtrack(paths, end):
    print(f'backtrack: {paths} {end}')

    def reconstruct_paths(current, path):
        print(f'reconstruct: {current} {path}')
        # None if the start
        if current is None:
            # reverse
            return [path[::-1]]
        # all_paths is a list of a list
        # so we use extend rather than append
        # to get the contents (the list in the list)
        all_paths = []
        for _, prev in paths[current]:
            rp = reconstruct_paths(prev, path + [current])
            print(f'all_paths: extending {all_paths} with {rp}')
            all_paths.extend(rp)
            print(f'all_paths: result {all_paths}')
        print(f'all_paths: return {all_paths}')
        return all_paths

    return reconstruct_paths(end, [])


if __name__ == '__main__':
    grid = [
        ['.', '.', '.'],
        ['.', '#', '.'],
        ['.', '.', '.'],
    ]
    start = (0, 0)
    end = (2, 2)

    paths = dijkstra_all_shortest_paths(grid, start, end)
    for p in paths:
        print(p)


# Usage:
# grid could be [['.', '.', '.'], ['.', '#', '.'], ['.', '.', '.']] where '#' might represent obstacles
# start = (0, 0), end = (2, 2)
