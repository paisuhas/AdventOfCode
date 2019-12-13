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
screen = dict()
output_count = -1
left = None
top = None
paddle = None
ball = None

def draw_screen():
    global screen
    layout = [(left, top) for left, top in list(screen.keys())]
    max_left = max(layout, key=lambda x:x[0])[0]
    max_top = max(layout, key=lambda x:x[1])[1]
    for v in range(max_top+1):
        row = str(v)[-1]
        for h in range(max_left+1):
            if (h, v) not in screen:
                row += ' '
            elif screen[(h, v)] == 0:
                # Nothing
                row += ' '
            elif screen[(h, v)] == 1:
                # Wall
                row += '#'
            elif screen[(h, v)] == 2:
                # Block
                row += 'b'
            elif screen[(h, v)] == 3:
                # Paddle
                row += 'T'
            elif screen[(h, v)] == 4:
                # Ball
                row += 'o'
            else:
                assert(False)
        print(row)

def get_inputs(draw=0):
    global ball
    global paddle
    while True:
        if draw:
            draw_screen()
        if ball[0] < paddle[0]:
            # Follow ball to left
            yield -1
        elif ball[0] > paddle[0]:
            # Follow ball to right
            yield 1
        else:
            # Stay where you are
            yield 0

def put_output(outp):
    global screen
    global output_count
    global left
    global top
    global paddle
    global ball
    output_count += 1
    phase = output_count % 3
    if phase == 0:
        left = outp
    elif phase == 1:
        top = outp
    else:
        assert(phase == 2)
        if left == -1 and top == 0:
            print("score is", outp)
        else:
            screen[(left, top)] = outp
            if outp == 4:
                ball = (left, top)
            elif outp == 3:
                paddle = (left, top)
    return

next_pc = 0
relative_base = 0

three_op_instructions = [1, 2]
one_op_instructions = [3, 4, 9]
jump_instructions = [5, 6]
comparison_instructions = [7, 8]

input_port = get_inputs()
while True:
    pc = next_pc
    opcode = program[pc]
    modes, op = decode(opcode)
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
