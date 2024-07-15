import sys; args = sys.argv[1:]
#pzls = open(args[0], 'r').read().splitlines()
pzls = open('puzzles.txt', 'r').read().splitlines()
import math, time

global start, fixing, hardcode, count, sideLength, width, height, symbols, constraintSets, rows, cols, subblocks

def dimensions(num):
  width = [i for i in range(1, math.isqrt(num))+1 if num % i == 0][-1]
  height = num // width
  return [width, height]

def isInvalid(pzl):
    column = 0
    for i in range(0, len(pzl), sideLength):
        row = findRow(pzl, i)
        temp = set()
        for ch in row:
            if ch in temp:
                return True
            elif ch in symbols:
                temp.add(ch)
        col = findCol(pzl, column)
        temp = set()
        for ch in col:
            if ch in temp:
                return True
            elif ch in symbols:
                temp.add(ch)
        column += 1
    xIterations = sideLength // width
    yIterations = sideLength // height
    for i in range(xIterations):
        for j in range(yIterations):
            temp = set()
            for ch in findSubBlock(pzl, j*sideLength*height+i*width):
                if ch in temp:
                    return True
                elif ch in symbols:
                    temp.add(ch)
    return False

def display(board):
    '''
    temp = []
    for r in range(sideLength):
        for c in range(sideLength):
            temp.append(board[sideLength*r+c])
        if (r+1)%height == 0:
            iterations = sideLength // width
            for h in range(height):
                for n in range(iterations):
                    for i in range(width):
                        print(temp[n*sideLength+i+h*height], end='')
                    print(' ', end='')
                print()
            print()
            temp = []
    '''
    for r in range(sideLength):
        if r > 0 and r%height == 0:
            print()
        for c in range(sideLength):
            if c > 0 and c%width == 0:
                print(' ', end='')
            print(board[r*sideLength+c], end='')
        print()
    print()
    print()

def findRow(pzl, loc):
    startRow = loc // sideLength * sideLength
    temp = set()
    for r in range(startRow, startRow+sideLength):
        temp.add(r)
    return temp

def findCol(pzl, loc):
    col = loc % sideLength
    temp = set()
    for r in range(sideLength):
        temp.add(r*sideLength+col)
    return temp

def findSubBlock(pzl, loc):
    temp = set()
    diff = loc % sideLength
    subBlockLowerX = diff // width * width
    subBlockHigherX = subBlockLowerX + width
    row = loc // sideLength
    subBlockLowerY = row // height * height
    subBlockHigherY = subBlockLowerY + height
    for r in range(subBlockLowerY, subBlockHigherY):
        for c in range(subBlockLowerX, subBlockHigherX):
            temp.add(r*sideLength+c)
    return temp

def findBest(pzl):
    locs = [i for i, ch in enumerate(pzl) if ch == '.']
    ret = {}
    for loc in locs:
        ret[loc] = (len((s := test(pzl, loc))), s, loc)
    '''
    help = {1 : [],
            2 : [],
            3 : [],
            4 : [],
            5 : [],
            6 : [],
            7 : [],
            8 : [],
            9 : []}
    for loc in locs:
        s = test(pzl, loc)
        th = len(s)
        if th in help:
            help[th].append((th, s, loc))
    return help
    '''
    #return [(len((s := test(pzl, loc))), s, loc) for loc in locs]
    return ret

def findBest2(pzl, loc):
    one, two = isHiddenSingle(pzl, loc)
    if two > -1:
        return (1, one, {two})
    helper = {}
    for i in constraintSets[loc]:
        for sym in test(pzl, i):
            if pzl[i] == '.':
                if sym in helper:
                    helper[sym].add(i)
                else:
                    helper[sym] = set()
                    helper[sym].add(i)
    minV, minS, minP = 100, 1, {}
    for sym in helper:
        v = helper[sym]
        if len(v) < minV:
            minV = len(v)
            minS = sym
            minP = v
    return (minV, minS, minP)

def isFilledOut(pzl):
    return pzl.find('.') == -1

def test(pzl, loc):
    temp = {*symbols} - {pzl[i] for i in constraintSets[loc] if pzl[i] in symbols}
    return temp

def isHiddenSingle(pzl, loc):
    row = loc // sideLength
    diff = loc % sideLength
    subBlockLowerX = diff // width * width
    subBlockLowerY = row // height * height
    if diff % width == 0:
        col1 = {pzl[i] for i in cols[loc + 1]}
        col1i = {*cols[loc+1]}
        col2 = {pzl[i] for i in cols[loc + 2]}
        col2i = {*cols[loc+2]}
    elif diff % width == 1:
        col1 = {pzl[i] for i in cols[loc - 1]}
        col1i = {*cols[loc-1]}
        col2 = {pzl[i] for i in cols[loc + 1]}
        col2i = {*cols[loc+1]}
    else:
        col1 = {pzl[i] for i in cols[loc - 2]}
        col1i = {*cols[loc-2]}
        col2 = {pzl[i] for i in cols[loc - 1]}
        col2i = {*cols[loc-1]}
    if row % height == 0:
        row1 = {pzl[i] for i in rows[loc + sideLength]}
        row1i = {*rows[loc+sideLength]}
        row2 = {pzl[i] for i in rows[loc + 2 * sideLength]}
        row2i = {*rows[loc+2*sideLength]}
    elif row % height == 1:
        row1 = {pzl[i] for i in rows[loc - sideLength]}
        row1i = {*rows[loc-sideLength]}
        row2 = {pzl[i] for i in rows[loc + sideLength]}
        row2i = {*rows[loc+sideLength]}
    else:
        row1 = {pzl[i] for i in rows[loc - sideLength]}
        row1i = {*rows[loc-sideLength]}
        row2 = {pzl[i] for i in rows[loc - 2 * sideLength]}
        row2i = {*rows[loc-2*sideLength]}
    sub = {i for i in findSubBlock(pzl, loc) if pzl[i] == '.'}
    for sym in test(pzl, loc):
        subblock = sub.copy()
        if sym in row1:
            subblock = subblock - row1i
        if sym in row2:
            subblock = subblock - row2i
        if sym in col1:
            subblock = subblock - col1i
        if sym in col2:
            subblock = subblock - col2i
        if len(subblock) == 1:
            return (sym, subblock.pop())
    return -1, -1

'''
def bruteForce(pzl, possible):
    global count
    count += 1
    if isFilledOut(pzl): return pzl
    minVal, minSet, minPos = 100, {}, -1
    for i in possible:
        v, s, k = possible[i]
        if v < minVal:
            minVal = v
            minSet = s
            minPos = k
        if v == 1:
            break
    constraintSet = constraintSets[minPos]
    if minVal <= 2:
        del possible[minPos]
        for num in minSet:
            subPzl = ''.join([pzl[:minPos], num, pzl[minPos + 1:]])
            if len(possible) > 1:
                possibilities = possible.copy()
            else:
                possibilities = possible
            for i in possibilities:
                tv, ts, tk = possibilities[i]
                if tk in constraintSet and num in ts:
                    possibilities[i] = (len(ts) - 1, ts - {num}, tk)
            bf = bruteForce(subPzl, possibilities)
            if bf:
                return bf
        possible[minPos] = (minVal, minSet, minPos)
    else:
        mV, mS, mP = findBest2(pzl, minPos)
        if mV < minVal:
            for p in mP:
                subPzl = pzl[:p] + mS + pzl[p+1:]
                if len(possible) > 1:
                    possibilities = possible.copy()
                else:
                    possibilities = possible
                ind = -1
                for i in possibilities:
                    tv, ts, tk = possibilities[i]
                    if tk == p:
                        ind = i
                    elif tk in constraintSets[p] and mS in ts:
                        possibilities[i] = (len(ts) - 1, ts - {mS}, tk)
                del possibilities[ind]
                bf = bruteForce(subPzl, possibilities)
                if bf:
                    return bf
            else:
                del possible[minPos]
                for num in minSet:
                    subPzl = ''.join([pzl[:minPos], num, pzl[minPos + 1:]])
                    if len(possible) > 1:
                        possibilities = possible.copy()
                    else:
                        possibilities = possible
                    for i in possibilities:
                        tv, ts, tk = possibilities[i]
                        if tk in constraintSet and num in ts:
                            possibilities[i] = (len(ts) - 1, ts - {num}, tk)
                    bf = bruteForce(subPzl, possibilities)
                    if bf:
                        return bf
                possible[minPos] = (minVal, minSet, minPos)
    return ''
'''

def bruteForce(pzl, possible):
    global count
    count += 1
    if len(possible) == 0: return pzl
    minVal, minSet, minPos = 100, {}, -1
    for key in possible:
        v, s, k = possible[key]
        if len(s) < minVal:
            minVal = len(s)
            minSet = s
            minPos = k
        if len(s) == 1:
            break
    constraintSet = constraintSets[minPos]
    del possible[minPos]
    subset = {k for k in possible if possible[k][2] in constraintSet}
    for num in minSet:
        subPzl = ''.join([pzl[:minPos], num, pzl[minPos+1:]])
        tofix = []
        for k in subset:
            tv, ts, tk = possible[k]
            if num in ts:
                possible[k] = (len(ts)-1, ts-{num}, tk)
                tofix.append((k, tv, ts, tk))
        bf = bruteForce(subPzl, possible)
        if bf:
            return bf
        for tup in tofix:
            k, tv, ts, tk = tup
            possible[k] = (tv, ts, tk)
    possible[minPos] = (minVal, minSet, minPos)
    return ''

def checkSum(pzl):
    pzlSum = 0
    for ch in pzl:
        pzlSum += ord(ch)
    return (pzlSum - len(pzl) * ord('1'))

def findNeighbors(loc):
    startRow = loc // sideLength * sideLength
    temp = {r for r in range(startRow, startRow+sideLength)}
    col = loc % sideLength
    for r in range(sideLength):
        temp.add(r*sideLength+col)
    diff = loc % sideLength
    subBlockLowerX = diff // width * width
    subBlockHigherX = subBlockLowerX + width
    row = loc // sideLength
    subBlockLowerY = row // height * height
    subBlockHigherY = subBlockLowerY + height
    for r in range(subBlockLowerY, subBlockHigherY):
        for c in range(subBlockLowerX, subBlockHigherX):
            temp.add(r*sideLength+c)
    return [*temp]

startTime = time.time()
for index, pzl in enumerate(pzls):
    if index == 0:
        #sideLength = math.isqrt(len(pzl))
        #width, height = dimensions(sideLength)
        #symbols = []
        #for n in range(1, sideLength+1):
            #symbols.append(str(n))
        sideLength = 9
        width, height = 3, 3
        symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        constraintSets = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80],
            [0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63, 72],
            [0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 55, 64, 73],
            [0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 56, 65, 74],
            [3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 30, 39, 48, 57, 66, 75],
            [3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58, 67, 76],
            [3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59, 68, 77],
            [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78],
            [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79],
            [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80],
            [0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63, 72],
            [0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55, 64, 73],
            [0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56, 65, 74],
            [3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 39, 48, 57, 66, 75],
            [3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 40, 49, 58, 67, 76],
            [3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 41, 50, 59, 68, 77],
            [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33, 42, 51, 60, 69, 78],
            [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 34, 43, 52, 61, 70, 79],
            [6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 44, 53, 62, 71, 80],
            [0, 9, 18, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63, 72],
            [1, 10, 19, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 64, 73],
            [2, 11, 20, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 65, 74],
            [3, 12, 21, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57, 66, 75],
            [4, 13, 22, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58, 67, 76],
            [5, 14, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59, 68, 77],
            [6, 15, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 60, 69, 78],
            [7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 61, 70, 79],
            [8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 62, 71, 80],
            [0, 9, 18, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63, 72],
            [1, 10, 19, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55, 64, 73],
            [2, 11, 20, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56, 65, 74],
            [3, 12, 21, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 57, 66, 75],
            [4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 58, 67, 76],
            [5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 59, 68, 77],
            [6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 60, 69, 78],
            [7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 61, 70, 79],
            [8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 62, 71, 80],
            [0, 9, 18, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63, 72],
            [1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 64, 73],
            [2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 65, 74],
            [3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57, 66, 75],
            [4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 58, 67, 76],
            [5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 68, 77],
            [6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60, 69, 78],
            [7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 61, 70, 79],
            [8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 62, 71, 80],
            [0, 9, 18, 27, 36, 45, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
            [1, 10, 19, 28, 37, 46, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
            [2, 11, 20, 29, 38, 47, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74],
            [3, 12, 21, 30, 39, 48, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77],
            [4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77],
            [5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77],
            [6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80],
            [7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80],
            [8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80],
            [0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
            [1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
            [2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
            [3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77],
            [4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77],
            [5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77],
            [6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80],
            [7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80],
            [8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80],
            [0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
            [8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
        ]
        rows = [0] * len(pzl)
        cols = [0] * len(pzl)
        subblocks = [0] * len(pzl)
        for i in range(len(pzl)):
            rows[i] = findRow(pzl, i)
            cols[i] = findCol(pzl, i)
            subblocks[i] = findSubBlock(pzl, i)
        #samplePzl = '....9...6.....2..58..4.372..49...........4...1.3.6.9..5.4..6.8.......1.771.....4.'
        #samplePzl = '......5..16.9.......9.64...........44...2.1.....3...5...2.89....1.25..3.7..1....9'
        #samplePzl = '.28..7.6..16.83.7.....2.85113729.......73........463.729..7.......86.14....3..7..'
        #for i in range(81):
            #print(isHiddenSingle(samplePzl, i))
        #display(samplePzl)
        count = 0
    print(index+1, pzl)
    start = time.time()
    helped = 0
    for val in range(len(pzl)):
        sym, pos = isHiddenSingle(pzl, val)
        if pos > -1:
            pzl = pzl[:pos] + sym + pzl[pos+1:]
            helped += 1
    solvedPzl = bruteForce(pzl, findBest(pzl))
    #display(pzl)
    print(' ' * len(str(index+1)), solvedPzl, checkSum(solvedPzl), str(time.time() - start)[:4], helped)
print(time.time() - startTime)
print('Count', count)

#Vishal Kotha, 4, 2023