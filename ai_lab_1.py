import sys; args = sys.argv[1:]
#Vishal Kotha, 4
import time, math, random, re

start = time.time()

def dimensions(puzzle):
  width = [i for i in range(1, int(1 + math.sqrt(len(puzzle)) - math.sqrt(len(puzzle)) % 1)) if len(puzzle) % i == 0][-1]
  height = len(puzzle) // width
  return [width, height]

params = dimensions(args[0])
gWIDTH = params[0]
gHEIGHT = params[1]

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

adjacent = neighbors(args[0])

def BFS(start, goal):
  if start == goal:
      return [start]

  parseMe = [start]
  dctSeen = {start : "rootIndicator"}

  while parseMe:
    node = parseMe.pop(0)
    location = node.index('_')
    for neighbor in adjacent[location]:
      temp = node
      temp = temp[:temp.index('_')] + temp[neighbor] + temp[temp.index('_')+1:]
      temp = temp[:neighbor] + '_' + temp[neighbor+1:]
      if temp not in dctSeen:
        parseMe.append(temp)
        dctSeen[temp] = node
        if temp == goal:
          path = [goal]
          while dctSeen[temp] != "rootIndicator":
            path.append(dctSeen[temp])
            temp = dctSeen[temp]
          path.append(start)
          return path[::-1]

  return []

solution = ''.join([''.join(sorted(''.join(args[0].split('_')))), '_'])

path = []
if len(args) == 1:
  path = BFS(args[0], solution)
  if len(path) > 1 and path[0] == path[1]:
    path.pop(0)
else:
  path = BFS(args[0], args[1])
  if len(path) > 1 and path[0] == path[1]:
    path.pop(0)

def display(path):
  for i in range(num := len(path) // 5):
    for j in range(gHEIGHT):
      list = []
      for k in range(5):
        square = path[i*5+k]
        list.append(square[j*gWIDTH:(j+1)*gWIDTH])
      print(' '.join(list))
    print()

  for j in range(gHEIGHT):
    list = []
    for k in range(len(path)-5*num):
      square = path[num * 5 + k]
      list.append(square[j * gWIDTH:(j + 1) * gWIDTH])
    print(' '.join(list))

if path:
  display(path)
else:
  display([args[0]])

print('Steps: ' + str(len(path)-1))

print('Time: ' + str(time.time() - start)[:4] + 's')