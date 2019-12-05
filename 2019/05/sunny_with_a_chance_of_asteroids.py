#!/usr/bin/env python3

def decode(opcode):
    op = opcode % 100
    modes = []
    for i in [100, 1000, 10000]:
        modes.append((opcode // i) % 10)
    return (modes, op)

program = list(map(int, open("input.txt").readlines()[0].strip().split(',')))

next_pc = 0

three_op_instructions = [1, 2]
one_op_instructions = [3, 4]

for pc, opcode in enumerate(program):
    if pc == next_pc:
        modes, op = decode(opcode)
        if op in three_op_instructions:
            operands = [program[pc+offset] if mode else program[program[pc+offset]] for offset, mode in enumerate(modes[:-1], 1)]
            next_pc = pc + 4
            if op == 1:
                result = sum(operands)
            else:
                assert(op == 2)
                result = operands[0] * operands[1]

            assert(modes[-1] == 0)
            program[program[pc + 3]] = result
        elif op in one_op_instructions:
            next_pc = pc + 2

            if op == 3:
                program[program[pc+1]] = 1
            else:
                assert(op == 4)
                if modes[0]:
                    print(program[pc+1])
                else:
                    print(program[program[pc+1]])
        else:
            assert(op == 99)
            break
