import numpy as np
import csv

filepath = "config/log/Graph1.txt"

data = []

with open(filepath, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

data.pop(0)
array = np.array(data, dtype=float)
res = np.std(array, axis=0)

print("The calculated standard deviations are: ", res)
