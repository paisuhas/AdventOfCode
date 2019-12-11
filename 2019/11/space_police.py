#!/usr/bin/env python3

def decode(opcode):
    op = opcode % 100
    modes = []
    for i in [100, 1000, 10000]:
        modes.append((opcode // i) % 10)
    return (modes, op)

def store(value, pc, offset, mode):
    if mode == 0:
        address = program[pc + offset]
    elif mode == 1:
        address = pc + offset
    else:
        assert(mode == 2)
        address = relative_base + program[pc + offset]
    if address >= len(program):
        for i in range(len(program), address+1):
            program.append(0)
    program[address] = value

def get_operands(pc, modes):
    global program
    operands = []
    for offset, mode in enumerate(modes, 1):
        if mode == 0:
            address = program[pc + offset]
        elif mode == 1:
            address = pc + offset
        else:
            assert(mode == 2)
            address = relative_base + program[pc + offset]
        if address >= len(program):
            for i in range(len(program), address+1):
                program.append(0)
        operands.append(program[address])
    return operands

program = list(map(int, open("input.txt").readlines()[0].strip().split(',')))

# Part 1
panel = dict()
position = (0, 0)
panel[position] = 1 # 0 for Part 1
output_count = 0
orientation = 0 # 0 is up, 1 is left, 2 is down, 3 is right

def update_position(turn):
    global panel
    global position
    global orientation
    if turn == 0:
        if orientation == 0:
            position = position[0] - 1, position[1]
        elif orientation == 1:
            position = position[0], position[1] - 1
        elif orientation == 2:
            position = position[0] + 1, position[1]
        else:
            assert(orientation == 3)
            position = position[0], position[1] + 1
        orientation = (orientation + 1) % 4
    else:
        assert(turn == 1)
        if orientation == 0:
            position = position[0] + 1, position[1]
        elif orientation == 1:
            position = position[0], position[1] + 1
        elif orientation == 2:
            position = position[0] - 1, position[1]
        else:
            assert(orientation == 3)
            position = position[0], position[1] - 1
        orientation = (orientation - 1) % 4
    if position not in panel:
        panel[position] = 0

def get_inputs():
    global panel
    global position
    while True:
        yield panel[position]

def put_output(outp):
    global output_count
    global panel
    global position
    output_count += 1
    if output_count % 2:
        panel[position] = outp
    else:
        update_position(outp)

next_pc = 0
relative_base = 0

three_op_instructions = [1, 2]
one_op_instructions = [3, 4, 9]
jump_instructions = [5, 6]
comparison_instructions = [7, 8]

while True:
    pc = next_pc
    opcode = program[pc]
    modes, op = decode(opcode)
    input_port = get_inputs()
    if op in three_op_instructions:
        operands = get_operands(pc, modes)
        next_pc = pc + 4
        if op == 1:
            result = operands[0] + operands[1]
        else:
            assert(op == 2)
            result = operands[0] * operands[1]
        store(result, pc, 3, modes[2])
    elif op in one_op_instructions:
        next_pc = pc + 2
        if op == 3:
            # Input is 1 for Part 1 and 2 for Part 2
            inp = input_port.__next__()
            store(inp, pc, 1, modes[0])
        elif op == 4:
            assert(op == 4)
            if modes[0] == 1:
                outp = program[pc+1]
                put_output(outp)
            elif modes[0] == 0:
                outp = program[program[pc+1]]
                put_output(outp)
            else:
                assert(modes[0] == 2)
                outp = program[relative_base + program[pc+1]]
                put_output(outp)
        else:
            assert(op == 9)
            if modes[0] == 1:
                relative_base = relative_base + program[pc+1]
            elif modes[0] == 0:
                relative_base = relative_base + program[program[pc+1]]
            else:
                assert(modes[0] == 2)
                relative_base = relative_base + program[relative_base + program[pc + 1]]
    elif op in jump_instructions:
        operands = get_operands(pc, modes)
        if (op == 5 and operands[0]) or (op == 6 and not operands[0]):
            next_pc = operands[1]
        else:
            next_pc = pc + 3
    elif op in comparison_instructions:
        next_pc = pc + 4
        operands = get_operands(pc, modes)
        if (op == 7 and operands[0] < operands[1]) or (op == 8 and operands[0] == operands[1]):
            store(1, pc, 3, modes[2])
        else:
            store(0, pc, 3, modes[2])
    else:
        assert(op == 99)
        break

print(len(panel))

# Part 2
panes = list(panel.keys())
xmax = max(panes, key=lambda x: x[0])
ymax = max(panes, key=lambda x: x[1])
xmin = min(panes, key=lambda x: x[0])
ymin = min(panes, key=lambda x: x[1])
xlo = xmin[0]
xhi = xmax[0] + 1
ylo = ymax[1]
yhi = ymin[1] - 1

# negative y-axis
for y in range(ylo, yhi, -1):
    row = ''
    # positive y axis
    for x in range(xlo, xhi):
        if (x, y) not in panel:
            row += ' '
        elif panel[(x, y)]:
            row += '#'
        else:
            row += ' '
    print(row)
