#!/usr/bin/env python3

with open('input.txt') as orbits:
    orbit_dict = dict()
    for orbit in orbits:
        center, orbiter = orbit.strip().split(')')
        orbit_dict[orbiter] = center

    total = len(orbit_dict.keys())
    for k in orbit_dict:
        v = orbit_dict[k]
        while v in orbit_dict.keys():
            total += 1
            v = orbit_dict[v]
    print(total)
    assert(total == 122782)

    k = 'YOU'
    your_path = []
    while k in orbit_dict.keys():
        k = orbit_dict[k]
        your_path.append(k)

    k = 'SAN'
    santas_path = []
    while k in orbit_dict.keys():
        k = orbit_dict[k]
        santas_path.append(k)

    transfers = sum(k not in santas_path for k in your_path) + sum(k not in your_path for k in santas_path)
    print(transfers)
    assert(transfers == 271)
