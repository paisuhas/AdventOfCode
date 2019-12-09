#!/usr/bin/env python3
from itertools import permutations
from itertools import cycle

def decode(opcode):
    op = opcode % 100
    modes = []
    for i in [100, 1000]:
        modes.append((opcode // i) % 10)
    return (modes, op)

def get_operands(pc, modes, program):
    operands = []
    for offset, mode in enumerate(modes, 1):
        address = pc + offset if mode else program[pc+offset]
        operands.append(program[address])
    return operands

def get_inputs(in1, in2):
    yield in1
    yield in2

def run_program(in1, in2, i, part=2, next_pc = 0):
    global progs
    program = progs[i]
    pc = next_pc

    three_op_instructions = [1, 2]
    one_op_instructions = [3, 4]
    jump_instructions = [5, 6]
    comparison_instructions = [7, 8]

    inputs = get_inputs(in1, in2)
    output_signal = in1

    while True:
        opcode = program[pc]
        if pc == next_pc:
            modes, op = decode(opcode)
            if op in three_op_instructions:
                operands = get_operands(pc, modes, program)
                next_pc = pc + 4
                if op == 1:
                    result = sum(operands)
                else:
                    assert(op == 2)
                    result = operands[0] * operands[1]
    
                program[program[pc + 3]] = result
            elif op in one_op_instructions:
                next_pc = pc + 2
                if op == 3:
                    program[program[pc+1]] = inputs.__next__();
                else:
                    assert(op == 4)
                    if modes[0]:
                        output_signal = program[pc+1]
                    else:
                        output_signal = program[program[pc+1]]
                    return (next_pc, output_signal, False, program)
            elif op in jump_instructions:
                operands = get_operands(pc, modes, program)
                if (op == 5 and operands[0]) or (op == 6 and not operands[0]):
                    next_pc = operands[1]
                else:
                    next_pc = pc + 3
            elif op in comparison_instructions:
                next_pc = pc + 4
                operands = get_operands(pc, modes, program)
                if (op == 7 and operands[0] < operands[1]) or (op == 8 and operands[0] == operands[1]):
                    program[program[pc+3]] = 1
                else:
                    program[program[pc+3]] = 0
            else:
                assert(op == 99)
                break
            pc = next_pc
    assert(output_signal is not None)
    return (next_pc, output_signal, True, program)

max_output = None
for phases in permutations(range(5, 9+1), 5):
    programi = list(map(int, open("input.txt").readlines()[0].strip().split(',')))
    inp = 0
    pcs = [None] * 5
    outputs = [0] * 5
    halted = [None] * 5
    progs = [None] * 5
    for i, phase in enumerate(phases):
        progs[i] = programi.copy()
        pcs[i], outputs[i], halted[i], progs[i] = run_program(phase, inp, i)
        inp = outputs[i]
    for i in cycle(range(5)):
        pcs[i], outputs[i], halted[i], progs[i] = run_program(inp, None, i, next_pc=pcs[i])
        inp = outputs[i]
        if halted[4]:
            break
        if halted[i]:
            continue
    if max_output is None or inp > max_output:
        max_output = inp

print(max_output)
