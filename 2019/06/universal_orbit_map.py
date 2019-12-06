#!/usr/bin/env python3
from collections import defaultdict
from itertools import takewhile

with open('input.txt') as orbits:
    orbit_dict = defaultdict(list)
    for orbit in orbits:
        center, orbiter = orbit.strip().split(')')
        orbit_dict[orbiter].append(center)

    total = len(orbit_dict.keys())
    for k in orbit_dict.keys():
        for v in orbit_dict[k]:
            while v in orbit_dict.keys():
                total += 1
                v = orbit_dict[v][0]
    print(total)
    assert(total == 122782)

    k = 'YOU'
    your_path = []
    while k in orbit_dict.keys():
        k = orbit_dict[k][0]
        your_path.append(k)

    k = 'SAN'
    santas_path = []
    while k in orbit_dict.keys():
        k = orbit_dict[k][0]
        santas_path.append(k)

    transfers = sum(1 for k in takewhile(lambda x: x not in santas_path, your_path))
    transfers += sum(1 for k in takewhile(lambda x: x not in your_path, santas_path))
    print(transfers)
    assert(transfers == 271)
