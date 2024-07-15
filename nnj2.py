import sys;

args = sys.argv[1:]
lines = open('weights.txt').read().splitlines()

import math, random


def T1(x):
    return x


def T2(x):
    return max(0, x)


def T3(x):
    return 1 / (1 + math.exp(-x))


def T4(x):
    return 2 * (1 / (1 + math.exp(-x))) - 1


func = T3
x = []
y = []
for line in lines:
    line = line.split()
    splitPoint = line.index('=>')
    x.append([float(i) for i in line[:splitPoint]] + [1.0])
    y.append([float(i) for i in line[splitPoint + 1:]])


def backPropogation(w, x, y):
    forward = forwardPropogation(w, x)
    print(forward)
    back = forward[::-1]
    allError = []
    for index, val in enumerate(back):
        if index == 0:
            error = [y[i] - val[i] for i in range(len(y))]
            #print('0 ', error)
        elif index == 1:
            error = [allError[0][i] * w[-1][i] * back[2][i] * (-1 * back[2][i] + 1) for i in range(len(y))]
            #for i in range(len(y)):
                #print(allError[0][i])
                #print(w[-1][i])
                #print(val[i])
        else:
            error = [sum([allError[-1][i] * w[-index][i + j] * val[j] * (-1 * val[j] + 1) for i in range(len(y))]) for j
                     in range(len(val))]
            #print('2 ', error)
        allError.append(error)
    allError = allError[::-1]

    for index, weight in enumerate(w):
        for i in range(len(weight)):
            w[index][i] += 0.1 * allError[index + 1][i // len(forward[index])] * forward[index][
                i % len(forward[index])] if index < len(w) + 1 else 0.05 * allError[index + 1][i] * forward[index][i]


def forwardPropogation(w, x):
    allX = [x]
    for index, layer in enumerate(w):
        if index + 1 < len(w):
            x = ([func(sum([x[i] * layer[i + j] for i in range(len(x))])) for j in range(0, len(layer), len(x))])
            allX.append(x.copy())
        else:
            for i in range(len(x)):

                x[i] = x[i] * w[-1][i]
            allX.append(x.copy())
    return allX


M = 3
N = 1

w = [[1 for i in range(len(x[0]) * M)], [1 for j in range(len(y[0]) * M)],
     [1 for k in range(len(y[0]))]]

for epoch in range(N):
    for i, val in enumerate(x):
        backPropogation(w, val, y[i])

print('Layer counts', len(x[0]), M, len(y[0]), len(y[0]))

for layer in w:
    print(layer)

# Jay Lalwani, pd. 2, 2023