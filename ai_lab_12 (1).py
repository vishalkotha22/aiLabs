import sys; args = sys.argv[1:]
#arg = open(args[0], 'r').read().splitlines()
#Vishal Kotha, 4
import time, math, random, re

arg = open('Eckel55G.txt', 'r').read().splitlines()
gWIDTH = 4
gHEIGHT = 4

def neighbors(puzzle):
  dict = {}
  for i in range(len(puzzle)):
    locations = []
    if i >= gHEIGHT:
      locations.append(i-gHEIGHT)
    if i+gWIDTH < len(puzzle):
      locations.append(i+gHEIGHT)
    if i%gWIDTH != 0:
      locations.append(i-1)
    if (i+1)%gWIDTH != 0:
      locations.append(i+1)
    dict[i] = locations
  return dict

'''
def BFS(start, goal):
  if start == goal:
    return [start]

  parseMe = [(manhattan(start, goal), start)]
  dctSeen = {start: "rootIndicator"}

  neighborsLocations = {}
  neighborsLocations[0] = [1, 4]
  neighborsLocations[1] = [0, 2, 5]
  neighborsLocations[2] = [1, 3, 6]
  neighborsLocations[3] = [2, 7]
  neighborsLocations[4] = [0, 5, 8]
  neighborsLocations[5] = [1, 4, 6, 9]
  neighborsLocations[6] = [2, 5, 7, 10]
  neighborsLocations[7] = [3, 6, 11]
  neighborsLocations[8] = [4, 9, 12]
  neighborsLocations[9] = [5, 8, 10, 13]
  neighborsLocations[10] = [6, 9, 11, 14]
  neighborsLocations[11] = [7, 10, 15]
  neighborsLocations[12] = [8, 13]
  neighborsLocations[13] = [9, 12, 14]
  neighborsLocations[14] = [10, 13, 15]
  neighborsLocations[15] = [11, 14]

  while parseMe:
    parseMe = sorted(parseMe)
    dist, node = parseMe.pop(0)
    location = node.index('_')
    for neighbor in neighborsLocations[location]:
      temp = node
      temp = temp[:temp.index('_')] + temp[neighbor] + temp[temp.index('_') + 1:]
      temp = temp[:neighbor] + '_' + temp[neighbor + 1:]
      if temp not in dctSeen:
        dctSeen[temp] = node
        parseMe.append((manhattan(temp, goal), temp))
        if temp == goal:
          path = []
          while dctSeen[temp] != "rootIndicator":
            prevIndex = dctSeen[temp].index('_')
            index = temp.index('_')
            if prevIndex + 1 == index:
              path.append('R')
            elif prevIndex - 1 == index:
              path.append('L')
            elif prevIndex < index:
              path.append('D')
            else:
              path.append('U')
            temp = dctSeen[temp]
          return path[::-1]
  return []
'''

'''
def BFS(start, goal):
    neighborsLocations = {}
    neighborsLocations[0] = [1, 4]
    neighborsLocations[1] = [0, 2, 5]
    neighborsLocations[2] = [1, 3, 6]
    neighborsLocations[3] = [2, 7]
    neighborsLocations[4] = [0, 5, 8]
    neighborsLocations[5] = [1, 4, 6, 9]
    neighborsLocations[6] = [2, 5, 7, 10]
    neighborsLocations[7] = [3, 6, 11]
    neighborsLocations[8] = [4, 9, 12]
    neighborsLocations[9] = [5, 8, 10, 13]
    neighborsLocations[10] = [6, 9, 11, 14]
    neighborsLocations[11] = [7, 10, 15]
    neighborsLocations[12] = [8, 13]
    neighborsLocations[13] = [9, 12, 14]
    neighborsLocations[14] = [10, 13, 15]
    neighborsLocations[15] = [11, 14]
    parseMe = [start]
    dctSeen = {start : 'rootIndicator'}
    while parseMe:
        node = parseMe.pop(0)
        index = node.index('_')
        for nbr in neighborsLocations[index]:
            temp = node
            temp = temp[:index] + temp[nbr] + temp[index+1:]
            temp = temp[:nbr] + '_' + temp[nbr+1:]
            if temp not in dctSeen:
                dctSeen[temp] = node
                parseMe.append(temp)
                if temp == goal:
                    path = []
                    while dctSeen[temp] != "rootIndicator":
                        prevIndex = dctSeen[temp].index('_')
                        index = temp.index('_')
                        if prevIndex + 1 == index:
                            path.append('R')
                        elif prevIndex - 1 == index:
                            path.append('L')
                        elif prevIndex < index:
                            path.append('D')
                        else:
                            path.append('U')
                        temp = dctSeen[temp]
                    return path[::-1]
'''

def manhattan(start, goal):
  dist = 0
  for i in range(len(start)):
    if start[i] != '_':
      goalIndex = goal.index(start[i])
      dist += (abs(i // 3 - goalIndex // 3) + abs(i%3 - goalIndex%3))
  return dist // 2

def inversionCount(str):
  str = str[:str.index('_')] + str[str.index('_') + 1:]
  goal = sorted(str)
  count = 0
  for i in range(len(str)):
    for j in range(len(str)):
      if (goal.index(str[i]) < goal.index(str[j])) != (i < j):
        count += 1
  return count // 2

def distanceRow(start, goal):
  return abs(start.index('_') // gWIDTH - goal.index('_') // gWIDTH)

def isSolvable(start, goal):
  startInversionCount = inversionCount(start) % 2
  goalInversionCount = inversionCount(goal) % 2
  if gWIDTH % 2 == 1:
    return startInversionCount == goalInversionCount
  else:
    dist = distanceRow(start, goal)
    left = (startInversionCount + dist) % 2
    return left == goalInversionCount

def aStar(root, goal):
    if root == goal:
        return [root]
    indices = {}
    #neighborsLocations = neighbors(root)
    neighborsLocations = {}
    neighborsLocations[0] = [1, 4]
    neighborsLocations[1] = [0, 2, 5]
    neighborsLocations[2] = [1, 3, 6]
    neighborsLocations[3] = [2, 7]
    neighborsLocations[4] = [0, 5, 8]
    neighborsLocations[5] = [1, 4, 6, 9]
    neighborsLocations[6] = [2, 5, 7, 10]
    neighborsLocations[7] = [3, 6, 11]
    neighborsLocations[8] = [4, 9, 12]
    neighborsLocations[9] = [5, 8, 10, 13]
    neighborsLocations[10] = [6, 9, 11, 14]
    neighborsLocations[11] = [7, 10, 15]
    neighborsLocations[12] = [8, 13]
    neighborsLocations[13] = [9, 12, 14]
    neighborsLocations[14] = [10, 13, 15]
    neighborsLocations[15] = [11, 14]
    fringe = {0 : {goal}}
    visited = set()
    paths = {goal : []}
    radius = 7
    for i in range(1, radius+1):
        fringe[i] = set()
    for r in range(radius):
        for puzzle in fringe[r]:
            visited.add(puzzle)
            index = puzzle.index('_')
            for nbr in neighborsLocations[index]:
                copy = paths[puzzle][:]
                temp = ''.join([puzzle[:index], puzzle[nbr], puzzle[index + 1:]])
                temp = ''.join([temp[:nbr] + '_' + temp[nbr + 1:]])
                if temp not in visited:
                    if index-1 == nbr:
                        copy.append('R')
                    elif index+1 == nbr:
                        copy.append('L')
                    elif index < nbr:
                        copy.append('U')
                    elif index > nbr:
                        copy.append('D')
                    if root == temp:
                        return copy[::-1]
                    paths[temp] = copy
                    fringe[r+1].add(temp)
    for i, c in enumerate(goal):
        if c != '_':
            indices[c] = i
    '''
    for pzl in fringe[radius]:
        path1 = paths[pzl][::-1]
        path2 = BFS(pzl, goal)
        print(f"{pzl} {path1} {path2} {path1==path2}")
    '''
    incremental = {}
    for ch in goal:
        if ch != '_':
            goalIndex = indices[ch]
            for index in range(16):
                prevDist = abs(index // gWIDTH - goalIndex // gWIDTH) + abs(index % gWIDTH - goalIndex % gWIDTH)
                for nbr in neighborsLocations[index]:
                    dist = abs(nbr // gWIDTH - goalIndex // gWIDTH) + abs(nbr % gWIDTH - goalIndex % gWIDTH)
                    incremental[(ch, index, nbr)] = dist - prevDist
    openSet = {}
    for i in range(56):
        openSet[i] = []
    startLevel = manhattan(root, goal)
    openSet[startLevel].append((startLevel, root, startLevel))
    parent = {root : 'none'}
    closedSet = {}
    for i in range(startLevel, 56, 2):
        for dist, node, manh in openSet[i]:
            #print(openSet)
            #openSet = sorted(openSet)
            #print(openSet)
            #dist, node = openSet[0]
            #del openSet[0]
            if node in closedSet:
                continue
            else:
                if closedSet:
                    closedSet[node] = closedSet[parent[node]] + 1
                else:
                    closedSet[node] = 0
            loc = node.index('_')
            for nbr in neighborsLocations[loc]:
                print(parent)
                #print(parent)
                temp = ''.join([node[:loc], node[nbr], node[loc + 1:]])
                temp = ''.join([temp[:nbr] + '_' + temp[nbr + 1:]])
                parent[temp] = node
                if temp == goal:
                    path = []
                    while parent[temp] != "none":
                        prevIndex = parent[temp].index('_')
                        print(f"{temp} {parent[temp]}")
                        index = temp.index('_')
                        if prevIndex + 1 == index:
                            path.append('R')
                        elif prevIndex - 1 == index:
                            path.append('L')
                        elif prevIndex < index:
                            path.append('D')
                        else:
                            path.append('U')
                        temp = parent[temp]
                    return path[::-1]
                if temp in closedSet:
                    continue
                #if(len(paths[copy]) == desiredLen):
                    #print(f"{len(paths[copy])} {paths[copy][::-1]} {temp}")
                    #return paths[copy][::-1]
                '''
                if temp in fringe[radius]:
                    copy = temp
                    path = []
                    while parent[temp] != "none":
                        prevIndex = parent[temp].index('_')
                        index = temp.index('_')
                        if prevIndex + 1 == index:
                            path.append('R')
                        elif prevIndex - 1 == index:
                            path.append('L')
                        elif prevIndex < index:
                            path.append('D')
                        else:
                            path.append('U')
                        temp = parent[temp]
                    #if len(paths[copy]) + len(path) == desiredLen:
                    paths[copy].extend(path)
                        #return paths[copy][::-1]
                    if len(ret) == 0:
                        ret = paths[copy][::-1]
                    elif len(ret) > len(paths[copy]):
                        ret = paths[copy][::-1]
                    temp = copy
                '''
                #'''
                change = incremental[(node[nbr], nbr, loc)]
                estimation = closedSet[node] + 1 + manh + change
                openSet[estimation].append((estimation, temp, manh+change))
            #if len(ret) > 0:
                #return ret
            #print(f'{node}" "{openSet}')
            #print(openSet)
            #openSet[level].remove((dist, node))
            #print(openSet)

def rad(goal, radius):
    neighborsLocations = {}
    neighborsLocations[0] = [1, 3]
    neighborsLocations[1] = [0, 2, 4]
    neighborsLocations[2] = [1, 5]
    neighborsLocations[3] = [0, 4, 6]
    neighborsLocations[4] = [1, 3, 5, 7]
    neighborsLocations[5] = [2, 4, 8]
    neighborsLocations[6] = [3, 7]
    neighborsLocations[7] = [4, 6, 8]
    neighborsLocations[8] = [5, 7]
    fringe = {0 : {goal}}
    visited = set()
    paths = {goal : []}
    for i in range(1, radius+1):
        fringe[i] = set()
    for r in range(radius):
        for puzzle in fringe[r]:
            visited.add(puzzle)
            index = puzzle.index('_')
            if r > 0 and manhattan('1_2345678', puzzle) != r:
                print(r)
                print(manhattan('1_234568', puzzle))
                return puzzle
            for nbr in neighborsLocations[index]:
                copy = paths[puzzle][:]
                temp = ''.join([puzzle[:index], puzzle[nbr], puzzle[index + 1:]])
                temp = ''.join([temp[:nbr] + '_' + temp[nbr + 1:]])
                if temp not in visited:
                    if index-1 == nbr:
                        copy.append('R')
                    elif index+1 == nbr:
                        copy.append('L')
                    elif index < nbr:
                        copy.append('U')
                    elif index > nbr:
                        copy.append('D')
                paths[temp] = copy
                fringe[r+1].add(temp)
    return paths

def BFS(start, goal):
  if start == goal:
    return [start]

  parseMe = [(manhattan(start, goal), start)]
  dctSeen = {start: "rootIndicator"}

  neighborsLocations = {}
  neighborsLocations[0] = [1, 3]
  neighborsLocations[1] = [0, 2, 4]
  neighborsLocations[2] = [1, 5]
  neighborsLocations[3] = [0, 4, 6]
  neighborsLocations[4] = [1, 3, 5, 7]
  neighborsLocations[5] = [2, 4, 8]
  neighborsLocations[6] = [3, 7]
  neighborsLocations[7] = [4, 6, 8]
  neighborsLocations[8] = [5, 7]

  while parseMe:
    dist, node = parseMe.pop(0)
    location = node.index('_')
    for neighbor in neighborsLocations[location]:
      temp = node
      temp = temp[:temp.index('_')] + temp[neighbor] + temp[temp.index('_') + 1:]
      temp = temp[:neighbor] + '_' + temp[neighbor + 1:]
      if temp not in dctSeen:
        dctSeen[temp] = node
        parseMe.append((manhattan(temp, goal), temp))
        if temp == goal:
          path = []
          while dctSeen[temp] != "rootIndicator":
            prevIndex = dctSeen[temp].index('_')
            index = temp.index('_')
            if prevIndex + 1 == index:
              path.append('R')
            elif prevIndex - 1 == index:
              path.append('L')
            elif prevIndex < index:
              path.append('D')
            else:
              path.append('U')
            temp = dctSeen[temp]
          return path[::-1]
  return []

'''
goal = arg[0]
for i in range(len(arg)):
    if i == 0:
        print('0: ' + arg[i] + ' solved in 0.0 secs with path G')
    else:
        startTime = time.time()
        if isSolvable(arg[i], goal):
            path = aStar(arg[i], goal)
            print(str(i) + ': ' + arg[i] + ' solved in ' + str(time.time() - startTime)[:4] + ' secs with path ' + ''.join(path))
        else:
            print(str(i) + ': ' + arg[i] + ' solved in ' + str(time.time() - startTime)[:4] + ' secs with path X')
'''

print(rad('1_2345678', 20))
print(manhattan('1_2645738', '1_2345678'))
#for x in range(16):
    #print(str(x) + ': ', [len(puzzle) for puzzle in rad('12_345678', x).values() if len(puzzle) == x])
    #print(str(x) + ': ', sum([1 for puzzle in rad('1_2345678', x).values() if len(puzzle) == x]))
#Vishal Kotha, 4, 2023