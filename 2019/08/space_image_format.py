#!/usr/bin/env python3
from itertools import islice
from itertools import dropwhile

image = open('input.txt').readlines()[0].strip()

columns = 25
rows = 6
pixels_per_layer = columns * rows
num_pixels = sum(1 for pixel in image)
num_layers = num_pixels // pixels_per_layer

min_count = (None, None, None)
    
for start in map(lambda x: x * pixels_per_layer, range(num_layers)):
    stop = start + pixels_per_layer
    counts = (0, 0, 0)
    for pixel in islice(image, start, stop):
        counts = tuple(map(sum, zip(counts, (pixel == '0', pixel == '1', pixel == '2'))))
    pixels_in_layer = sum(counts)
    if min_count[0] is None or counts[0] < min_count[0]:
        min_count = counts

part1 = min_count[1] * min_count[2]
print(part1)
assert(part1 == 2760)

# Part 2
stop = num_layers * pixels_per_layer
step = pixels_per_layer

for row in range(rows):
    row_pixels = ""
    for col in range(columns):
        start = row * columns + col
        pixel = next(dropwhile(lambda x: x == '2', islice(image, start, stop, step)))
        if pixel == '1':
            row_pixels += "#"
        else:
            assert(pixel == '0')
            row_pixels += " "
    print(row_pixels)
