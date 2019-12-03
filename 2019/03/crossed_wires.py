#!/usr/bin/env python3
from itertools import accumulate

def compute_grid(paths):
    """
    Compute grid
    """
    grid = []
    for path in paths:
        dls = map(lambda x: (x[0], int(x[1:])), path.strip().split(','))
        center = (0, 0)
        points = [center]
        for d, l in dls:
            x, y = points[-1]
            if d == 'R':
                points.append((x + l, y))
            elif d == 'L':
                points.append((x - l, y))
            elif d == 'U':
                points.append((x, y + l))
            else:
                assert(d == 'D')
                points.append((x, y - l))
        grid.append(points)

    return grid

def compute_points(grid):
    """
    Compute points on plane
    """
    plane = []
    for points in grid:
        lines = []
        for point1, point2 in zip(points[:-1], points[1:]):
            if point1[0] == point2[0]:
                lo = min(point1[1], point2[1])
                hi = max(point1[1], point2[1])
                lines.append(('V', point1[0], range(lo, hi + 1), point1[1], hi - lo))
            elif point1[1] == point2[1]:
                lo = min(point1[0], point2[0])
                hi = max(point1[0], point2[0])
                lines.append(('H', point1[1], range(lo, hi + 1), point1[0], hi - lo))
            else:
                assert(False)
        plane.append(lines)

    return plane

def find_intersections(plane):
    """
    Find intersections
    """
    steps0 = list(accumulate(map(lambda x: x[4], plane[0])))
    steps1 = list(accumulate(map(lambda x: x[4], plane[1])))

    intersections = []
    for i, line1 in enumerate(plane[0]):
        for j, line2 in enumerate(plane[1]):
            if line1[0] != line2[0]:
                if line1[1] in line2[2] and line2[1] in line1[2]:
                    intersections.append((line1[1], line2[1],
                                            steps0[i-1] + steps1[j-1]
                                            + abs(line1[1] - line2[3])
                                            + abs(line2[1] - line1[3])))
    return intersections

with open('input.txt') as paths:
    grid = compute_grid(paths)

    plane = compute_points(grid)

    intersections = find_intersections(plane)

    print(min(filter(lambda x: x[0] != 0 or x[1] != 0, intersections), key=(lambda x: abs(x[0]) + abs(x[1]))))
    print(min(filter(lambda x: x[0] != 0 or x[1] != 0, intersections), key=(lambda x: x[2])))
