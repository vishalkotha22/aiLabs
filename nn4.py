import sys; args = sys.argv[1:]
tFile = open(args[0], 'r').read().splitlines()
weightsFile = []
for line in tFile:
    if '0' not in line and '1' not in line and '2' not in line and '3' not in line and '4' not in line and '5' not in line and '6' not in line and '7' not in line and '8' not in line and '9' not in line:
        continue
    else:
        weightsFile.append(line)
weightsFile = [x.split(', ') for x in weightsFile]
import math, random, re
operator = '<='
if '>=' in args[1]:
    operator = '>='
elif '>' in args[1]:
    operator = '>'
if '<=' in args[1]:
    operator = '<='
elif '<' in args[1]:
    operator = '<'
rightSide = float(args[1][args[1].index(operator)+len(operator):])
print(operator, rightSide)
for i in range(len(weightsFile)):
    weightsFile[i] = [float(x) for x in weightsFile[i]]
layerCts = [2]
for weights in weightsFile:
    layerCts.append(len(weights) // layerCts[-1])
bigLayerCts = [3]
for ct in layerCts[1:]:
    bigLayerCts.append(ct*2)
bigLayerCts[-1] = 1
bigLayerCts.append(1)
retWeights = []
newWeights = []
for x in range(layerCts[1]):
    newWeights.append(weightsFile[0][x*2])
    newWeights.append(0)
    newWeights.append(weightsFile[0][x*2+1])
for x in range(layerCts[1]):
    newWeights.append(0)
    newWeights.append(weightsFile[0][x*2])
    newWeights.append(weightsFile[0][x*2+1])
retWeights.append(newWeights)
for i, ct in enumerate(layerCts):
    if i == 0 or i >= len(layerCts)-2:
        continue
    newWeights = []
    for x in range(layerCts[i+1]):
        for y in range(ct):
            newWeights.append(weightsFile[i][x*ct+y])
        newWeights.extend([0] * ct)
    for x in range(layerCts[i+1]):
        newWeights.extend([0] * ct)
        for y in range(ct):
            newWeights.append(weightsFile[i][x*ct+y])
    retWeights.append(newWeights)
retWeights.append([weightsFile[-1][0] / rightSide, weightsFile[-1][0] / rightSide])
retWeights.append([(1+math.exp(1))/(2*math.exp(1))])
if '<' in operator:
    retWeights[-1][0] = retWeights[-1][0] * math.exp(1)
    retWeights[-2][0] *= -1
    retWeights[-2][1] *= -1
print('Layer counts:', bigLayerCts)
for rWeight in retWeights:
    print(rWeight)

#Vishal Kotha, 4, 2023