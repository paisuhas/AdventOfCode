#!/usr/bin/env python3

with open('input.txt', 'r') as source:
    program = list(map(int, source.readlines()[0].strip().split(',')))
    for i, opcode in enumerate(program):
        if i % 4 == 0:
            if opcode == 1:
                program[program[i + 3]] = program[program[i + 1]] + program[program[i + 2]]
            elif opcode == 2:
                program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
            elif opcode == 99:
                print(program[0])
                break
            else:
                assert(False)
