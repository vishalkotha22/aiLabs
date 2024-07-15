import sys;

args = sys.argv[1:]
#weightfile = open(args[0], 'r').read().splitlines()
import math, random, re

weights = []
for line in weightfile:
    temp = []
    for w in line.split():
        temp.append(float(w))
    weights.append(temp)


def t1(x):
    return x


def t2(x):
    if x >= 0:
        return abs(x)
    else:
        return 0


def t3(x):
    return 1 / (1 + math.exp(-x))


def t4(x):
    return 2 * t3(x) - 1


transferF = args[1]
inputs = []
for num in args[2:]:
    inputs.append(float(num))
print(inputs)

for c, layer in enumerate(weights):
    temp = []
    nodes = len(layer) // len(inputs)
    for i in range(nodes):
        if c + 1 < len(weights):
            sum = 0
            for w in range(len(inputs)):
                sum += layer[i * len(inputs) + w] * inputs[w]
            if transferF == 'T1':
                temp.append(sum)
            elif transferF == 'T2':
                temp.append(t2(sum))
            elif transferF == 'T3':
                temp.append(t3(sum))
            elif transferF == 'T4':
                temp.append(t4(sum))
        else:
            for w in range(len(inputs)):
                temp.append(layer[w] * inputs[w])
    inputs = temp
    print(inputs)

# Vishal Kotha, 4, 2023