import sys; args = sys.argv[1:]
weightfile = open('weights.txt').read().splitlines()
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
    print(nn)
    errors = []
    rev = nn[::-1]
    for i, layer in enumerate(nn[::-1]):
        if i == 0:
            error = []
            for i in range(len(y)):
                error.append(y[i] - nn[-1][i])
            errors.append(error)
            #print('0 ', error)
        elif i == 1:
            error = []
            for j, yy in enumerate(y):
                error.append((yy - nn[-1][j]) * weights[-1][j] * nn[-2][j] * (1 - nn[-2][j]))
            errors.append(error)
            #print('1 ', error)
            #print(yy-nn[-1][j])
            #print(weights[-1][j])
            #print(nn[-2][j])
        else:
            error = []
            for j, yy in enumerate(layer):
                errSum = 0
                for k in range(len(rev[i-1])):
                    errSum += weights[-i][j + k * len(layer)] * errors[-1][k] #error here
                error.append(errSum * yy * (1 - yy))
            errors.append(error)
            #print('2 ', error)
    return errors[::-1]


def bProp(nn, weights, y):
    errorTable = getErrorTable(nn, weights, y)
    for i, wList in enumerate(weights):
        for j, w in enumerate(wList):
            if i+1 < len(weights):
                weights[i][j] += 0.1 * errorTable[i + 1][j // len(nn[i])] * nn[i][j % len(nn[i])]
            else:
                weights[i][j] += 0.1 * errorTable[i+1][j] * nn[i][j]

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
for line in weightfile:
    inp = [int(x) for x in line.split('=>')[0] if x != ' ']
    inp.append(1)
    X.append(inp)
    out = [int(x) for x in line.split('=>')[1] if x != ' ']
    y.append(out)
    print(inp, out)

weights1 = [random.random() for i in range(len(X[0]) * 3)]
weights2 = [random.random() for i in range(3 * len(y[0]))]
weights3 = [random.random() for i in range(len(y[0]))]
weights = [weights1, weights2, weights3]

for epoch in range(1):
    for c, inp in enumerate(X):
        nn = forwardProp(inp, weights)
        bProp(nn, weights, y[c])

'''
print('Layer counts:', len(X[0]), 3, len(y[0]), len(y[0]))
print(weights1)
print(weights2)
print(weights3)
'''

# Vishal Kotha, 4, 2023