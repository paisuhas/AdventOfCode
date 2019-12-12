#!/usr/bin/env python3
from re import findall
from itertools import permutations
from itertools import count
from functools import reduce
from math import gcd

moons_status = dict()
with open('input.txt') as moons:
    for i, pos in enumerate(moons):
        moons_status[i] = (tuple(map(int, findall(r'-?\d+', pos))), (0, 0, 0))
    else:
        num_moons = i + 1

def one_iteration(num_moons):
    global moons_status
    velocities = [y for x, y in moons_status.values()]
    for j, k in permutations(range(num_moons), 2):
        pos0 = moons_status[j][0]
        pos1 = moons_status[k][0]
        velocities[j] = tuple(map(sum, zip(tuple(map(lambda x: -1 if x[0] > x[1] else 1 if x[0] < x[1] else 0, zip(pos0, pos1)))), velocities[j]))
    for j in range(num_moons):
        moons_status[j] = (tuple(map(sum, zip(moons_status[j][0], velocities[j]))), velocities[j])

for i in range(1000):
    one_iteration(num_moons)

part1 = sum([sum(map(abs, x)) * sum(map(abs, y)) for x, y in moons_status.values()])
print(part1)
assert(part1 == 6735)

iterations = list()
for axis in range(len(moons_status[0][0])):
    seen_before = set()
    for i in count():
        one_iteration(num_moons)
        prev_len = len(seen_before)
        seen_before.add(tuple([x[0][axis] for x in moons_status.values()] + [x[1][axis] for x in moons_status.values()]))
        if len(seen_before) == prev_len:
            break
    iterations.append(len(seen_before))

part2 = reduce(lambda x, y: x * y // gcd(x, y), iterations)
print(part2)
assert(part2 == 326489627728984)
