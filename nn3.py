import sys; args = sys.argv[1:]
rightSide = float(args[0][args[0].index('.') - 1:])
operator = args[0][args[0].rindex('y') + 1:args[0].index('.') - 1]
import math, random, re


def t1(x):
    return x


def t2(x):
    if x >= 0:
        return abs(x)
    return 0


def t3(x):
    return 1 / (1 + math.exp(-x))


def t4(x):
    return 2 * t3(x) - 1


def getErrorTable(nn, weights, y):
    errors = []
    rev = nn[::-1]
    for i, layer in enumerate(nn[::-1]):
        if i == 0:
            error = []
            for i in range(len(y)):
                error.append(y[i] - nn[-1][i])
            errors.append(error)
        elif i == 1:
            error = []
            for j, yy in enumerate(y):
                error.append((yy - nn[-1][j]) * weights[-1][j] * nn[-2][j] * (1 - nn[-2][j]))
            errors.append(error)
        else:
            error = []
            for j, yy in enumerate(layer):
                errSum = 0
                for k in range(len(rev[i - 1])):
                    errSum += weights[-i][j + k * len(layer)] * errors[-1][k]  # error here
                error.append(errSum * yy * (1 - yy))
            errors.append(error)
    return errors[::-1]


def bProp(nn, weights, y):
    errorTable = getErrorTable(nn, weights, y)
    for i, wList in enumerate(weights):
        for j, w in enumerate(wList):
            if i + 1 < len(weights):
                weights[i][j] += 0.1 * errorTable[i + 1][j // len(nn[i])] * nn[i][j % len(nn[i])]
            else:
                weights[i][j] += 0.1 * errorTable[i + 1][j] * nn[i][j]


def forwardProp(inputs, weights):
    transferF = 'T3'
    nn = []
    nn.append(inputs[:])
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
        nn.append(temp)
    return nn


X, y = [], []

for i in range(1000):
    px = random.random() * 3 - 1.5
    py = random.random() * 3 - 1.5
    X.append([px, py, 1])
    if operator == '<':
        if px * px + py * py < rightSide:
            y.append([1])
        else:
            y.append([0])
    elif operator == '<=':
        if px * px + py * py <= rightSide:
            y.append([1])
        else:
            y.append([0])
    elif operator == '>':
        if px * px + py * py > rightSide:
            y.append([1])
        else:
            y.append([0])
    elif operator == '>=':
        if px * px + py * py >= rightSide:
            y.append([1])
        else:
            y.append([0])
    else:
        print(operator)

#weights1 = [random.random() for i in range(12)]
#weights2 = [random.random() for i in range(20)]
#weights3 = [random.random() for i in range(25)]
#weights4 = [random.random() for i in range(5)]
#weights5 = [random.random()]
weights1 = [4.1851, -5.0124, -4.5023, -5.3326, -5.1318, 5.3735, -6.3426, -5.8358, -6.4281, -5.6734, 5.225, -5.3809]
weights2 = [4.5228, -4.2728, 4.4995, 4.4892, 1.0333, 2.886, 1.0223, 0.6443, 7.5025, -6.7578, 7.4429, 7.4941, 3.1199, -3.228, 3.1165, 3.1504, 5.6083, -5.1468, 5.5458, 5.5919]
weights3 = [-2.2688, -0.5865, -3.6942, -1.8957, -3.3279, -3.367, 3.7584, -6.2725, -1.5633, -4.1454, -2.6868, 1.5223, -4.9183, -2.3183, -3.5093, -2.5535, -0.5539, -3.9413, -1.8368, -2.8791, -3.2768, 4.4239, -6.5786, -1.7865, -4.488]
weights4 = [-3.6996, -5.7083, -4.6438, -3.735, -6.0285]
weights5 = [2.0465]
weights = [weights1, weights2, weights3, weights4, weights5]

for epoch in range(500):
    for c, inp in enumerate(X):
        nn = forwardProp(inp, weights)
        bProp(nn, weights, y[c])

print('Layer counts:', 3, 4, 5, 5, 1, 1)
print(weights1)
print(weights2)
print(weights3)
print(weights4)
print(weights5)

# Vishal Kotha, 4, 2023