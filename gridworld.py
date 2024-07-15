import sys; #args = sys.argv[1:]
#50 B0 B3 B6 B9 B30 B33 B36 B39 B42 B45 B18E B48E B2S B33S B29E B17E B47E B5S R12:400 R45:400 R44:200 G0 R18 B29S B36E B6W
args = '50 B0 B3 B6 B9 B30 B33 B36 B39 B42 B45 B18E B48E B2S B33S B29E B17E B47E B5S R12:400 R45:400 R44:200 G0 R18 B29S B36E B6W'.split(' ')
import math, re, random
area = int(args[0])
if re.match(r'/^\d*$', args[1]):
    width = int(args[1])
    height = area // width
    args = args[2:]
else:
    for i in range(int(math.sqrt(area)), area+1):
        if area%i == 0:
            width = i
            height = area // width
            break
    args = args[1:]
neighbors = {}
for i in range(area):
    nbrs = set()
    if i // width > 0:
        nbrs.add(i-width)
    if i%width > 0:
        nbrs.add(i-1)
    if i // width < height-1:
        nbrs.add(i+width)
    if i%width < width-1:
        nbrs.add(i+1)
    neighbors[i] = nbrs
default = 12
rewards = [0] * area
gZero = True
for arg in args:
    if arg[:2].upper() == 'R:':
        default = int(arg[2:])
for arg in args:
    if arg[0].upper() == 'R':
        if ':' not in arg:
            rewards[int(arg[1:])] = default
        elif arg[:2].upper() != 'R:':
            spl = arg.split(':')
            ind = int(spl[0][1:])
            rew = int(spl[1])
            rewards[ind] = rew
    elif arg[0].upper() == 'B':
        if 'N' in arg.upper() or 'S' in arg.upper() or 'E' in arg.upper() or 'W' in arg.upper():
            ind = int(arg[1:-1])
            if 'N' in arg.upper() and ind//width > 0:
                if ind-width in neighbors[ind]:
                    neighbors[ind].remove(ind-width)
                    neighbors[ind-width].remove(ind)
                else:
                    neighbors[ind].add(ind - width)
                    neighbors[ind - width].add(ind)
            elif 'S' in arg.upper() and ind//width < height-1:
                if ind+width in neighbors[ind]:
                    neighbors[ind].remove(ind+width)
                    neighbors[ind+width].remove(ind)
                else:
                    neighbors[ind].add(ind + width)
                    neighbors[ind + width].add(ind)
            elif 'E' in arg.upper() and ind%width < width-1:
                if ind+1 in neighbors[ind]:
                    neighbors[ind].remove(ind+1)
                    neighbors[ind+1].remove(ind)
                else:
                    neighbors[ind].add(ind + 1)
                    neighbors[ind + 1].add(ind)
            elif 'W' in arg.upper() and ind%width > 0:
                if ind-1 in neighbors[ind]:
                    neighbors[ind].remove(ind-1)
                    neighbors[ind-1].remove(ind)
                else:
                    neighbors[ind].add(ind - 1)
                    neighbors[ind - 1].add(ind)
        else:
            ind = int(arg[1:])
            if ind // width > 0:
                if ind - width in neighbors[ind]:
                    neighbors[ind].remove(ind - width)
                    neighbors[ind - width].remove(ind)
                else:
                    neighbors[ind].add(ind - width)
                    neighbors[ind - width].add(ind)
            if ind // width < height-1:
                if ind + width in neighbors[ind]:
                    neighbors[ind].remove(ind + width)
                    neighbors[ind + width].remove(ind)
                else:
                    neighbors[ind].add(ind + width)
                    neighbors[ind + width].add(ind)
            if ind%width < width-1:
                if ind + 1 in neighbors[ind]:
                    neighbors[ind].remove(ind + 1)
                    neighbors[ind + 1].remove(ind)
                else:
                    neighbors[ind].add(ind + 1)
                    neighbors[ind + 1].add(ind)
            if ind%width > 0:
                if ind - 1 in neighbors[ind]:
                    neighbors[ind].remove(ind - 1)
                    neighbors[ind - 1].remove(ind)
                else:
                    neighbors[ind].add(ind - 1)
                    neighbors[ind - 1].add(ind)
    elif arg[0].upper() == 'G':
        if '0' not in arg:
            gZero = False
output = ['x'] * area
fossil = []
for i in range(area):
    if rewards[i] > 0:
        output[i] = '*'
    else:
        queue = [(i, i, [], set())]
        queue[0][3].add(i)
        preserve = []
        while queue:
            start, ind, path, visited = queue[0]
            del queue[0]
            if rewards[ind] > 0 and len(path) > 0:
                preserve.append((ind, path, start))
                continue
            passed = 0
            for nbr in neighbors[ind]:
                temp = visited.copy()
                if nbr in visited:
                    continue
                passed += 1
                temp.add(nbr)
                d = ''
                if nbr == ind-width:
                    d = 'U'
                elif nbr == ind+width:
                    d = 'D'
                elif nbr == ind-1:
                    d = 'L'
                elif nbr == ind+1:
                    d = 'R'
                queue.append((start, nbr, path + [d], temp))
            if passed == 0:
                preserve.append((ind, path, start))
        fossil.append(preserve)
#print(fossil)
for temp in fossil:
    #print(temp)
    maxReward = 0
    for w in temp:
        maxReward = max(maxReward, rewards[w[0]])
    minIndex, minPathLength, minPaths = -1, 10000000, []
    for w in temp:
        if rewards[w[0]] == maxReward and len(w[1]) <= minPathLength:
            minPathLength = len(w[1])
            minPaths.append(w[1])
            minIndex = w[2]
    varDirs = set()
    for x in minPaths:
        if x:
            varDirs.add(x[0])
    symb = ''
    if maxReward == 0 or len(minPaths) == 0:
        symb = '.'
        minIndex = temp[0][2]
    elif len(varDirs) == 1:
        symb = varDirs.pop()
    elif len(varDirs) == 2:
        if 'U' in varDirs and 'R' in varDirs:
            symb = 'V'
        elif 'R' in varDirs and 'D' in varDirs:
            symb = 'S'
        elif 'D' in varDirs and 'L' in varDirs:
            symb = 'E'
        elif 'L' in varDirs and 'U' in varDirs:
            symb = 'M'
        elif 'U' in varDirs and 'D' in varDirs:
            symb = '|'
        elif 'L' in varDirs and 'R' in varDirs:
            symb = '-'
    elif len(varDirs) == 3:
        if 'L' not in varDirs:
            symb = 'W'
        if 'U' not in varDirs:
            symb = 'T'
        if 'R' not in varDirs:
            symb = 'F'
        if 'D' not in varDirs:
            symb = 'N'
    else:
        symb = '+'
    #print(minIndex)
    output[minIndex] = symb
for o in output:
    print(o, '', end='')

#Vishal Kotha, 4, 2023