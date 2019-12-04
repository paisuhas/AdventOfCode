#!/usr/bin/env python3
from collections import Counter

def can_be_password_part1(num):
    return any(i == j for i, j in zip(str(num)[:-1], str(num)[1:])) and all(int(i) <= int(j) for i, j in zip(str(num)[:-1], str(num)[1:]))

part1 = sum(map(can_be_password_part1, range(108457, 562042)))

print(part1)
assert(part1 == 2779)

def can_be_password_part2(num):
    c = Counter(str(num))
    return can_be_password_part1(num) and any(c[i] == 2 for i in c)

part2 = sum(map(can_be_password_part2, range(108457, 562042)))
print(part2)
