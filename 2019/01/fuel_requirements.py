#!/usr/bin/env python3

def total_fuel(mass):
    fuel = (mass // 3) - 2
    if fuel > 0:
        return fuel + total_fuel(fuel)
    else:
        return 0

with open('input.txt', 'r') as modules:
    print(sum(map(lambda x: ((int(x.strip()) // 3) - 2), modules)))

with open('input.txt', 'r') as modules:
    print(sum(map(total_fuel, map(lambda x: int(x.strip()), modules))))
