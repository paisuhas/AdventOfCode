#!/usr/bin/env python3
from math import atan2
from math import hypot
from math import pi
from itertools import cycle
from itertools import dropwhile

rows = 0
asteroids = []
with open('input.txt') as asteroid_map:
    for i, row in enumerate(asteroid_map):
        for asteroid in row.strip():
            asteroids.append(1 if asteroid == '#' else 0)
    else:
        rows = i + 1
assert(len(asteroids) % rows == 0)
columns = len(asteroids) // rows

max_visibility = 0
best_position = None
for i, asteroid0 in enumerate(asteroids):
    if not asteroid0:
        continue
    visibility = []
    x0, y0 = i % columns, i // columns
    for j, asteroid1 in enumerate(asteroids):
        if not asteroid1:
            continue
        x1, y1 = j % columns, j // columns
        visibility.append(atan2(y1 - y0, x1 - x0))
    count = len(set(visibility))
    if count > max_visibility:
        max_visibility = count
        best_position = i % columns, i // columns
print(max_visibility)
assert(max_visibility == 280)

# Part 2
metadata = []
x0, y0 = best_position
for i, asteroid in enumerate(asteroids):
    if not asteroid:
        continue
    x1, y1 = i % columns, i // columns
    if (x1, y1) == (x0, y0):
        continue
    angle = atan2(x1 - x0, y1 - y0)
    metadata.append((angle, hypot(x1 - x0, y1 - y0), (x1, y1)))

sorted_metadata = sorted(metadata, key=lambda x: (x[0], -x[1]), reverse=True)

unique_angles = sorted(list(set([x for x, y, z in sorted_metadata])), reverse=True)

evaporated = 0
for angle in cycle(unique_angles):
    asteroid = next(dropwhile(lambda x: x[0] != angle, sorted_metadata))
    sorted_metadata.remove(asteroid)
    evaporated += 1
    if evaporated == 200:
        coordinates = asteroid[2]
        part2 = coordinates[0] * 100 + coordinates[1]
        print(part2)
        assert(part2 == 706)
        break
