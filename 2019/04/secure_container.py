#!/usr/bin/env python3
from collections import Counter

def can_be_password_part1(num):
    return all(int(i) <= int(j) for i, j in zip(num, num[1:])) and any(i == j for i, j in zip(num, num[1:]))

part1 = sum(map(can_be_password_part1, map(str, range(108457, 562042))))
print(part1)
assert(part1 == 2779)

def can_be_password_part2(num):
    return all(int(i) <= int(j) for i, j in zip(num, num[1:])) and 2 in Counter(num).values()

part2 = sum(map(can_be_password_part2, map(str, range(108457, 562042))))
print(part2)
assert(part2 == 1972)
