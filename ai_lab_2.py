import sys; args = sys.argv[1:]
#arg = open(args[0], 'r').read().splitlines()
#Vishal Kotha, 4, 2023
import time, math, random, re

start = time.time()

arg = open('words.txt', 'r').read().splitlines()

def pipe(arg, index):
    gap = {}
    for word in arg:
        pipe = word[:index] + word[index+1:]
        if pipe in gap:
            gap[pipe].add(word)
        else:
            gap[pipe] = set()
            gap[pipe].add(word)
    return gap

first = pipe(arg, 0)
second = pipe(arg, 1)
third = pipe(arg, 2)
fourth = pipe(arg, 3)
fifth = pipe(arg, 4)
sixth = pipe(arg, 5)

graph = {}

def addToGraph(graph, pipes):
    for pipe in pipes:
        words = pipes[pipe]
        for word in words:
            if word not in graph:
                graph[word] = set()
            for word1 in words:
                if word1 != word:
                    graph[word].add(word1)

addToGraph(graph, first)
addToGraph(graph, second)
addToGraph(graph, third)
addToGraph(graph, fourth)
addToGraph(graph, fifth)
addToGraph(graph, sixth)

dict = {}

dict[0] = 'Word Count: ' + str(len(arg))

count = 0
for key in graph.keys():
    count += len(graph[key])
dict[1] = 'Edge Count: ' + str(count//2)

maxNum = 0
for key in graph.keys():
    if len(graph[key]) > maxNum:
        maxNum = len(graph[key])
distributionList = [0] * (maxNum+1)
for key in graph.keys():
    distributionList[len(graph[key])] += 1
    if len(graph[key]) == maxNum-1:
        dict[4] = 'Second degree word: ' + key

dict[2] = 'Degree List: ' + ' '.join(str(distributionList)[1:-1].split(', '))

dict[3] = 'Construction Time: ' + str(time.time() - start)[:4] + 's'

if len(args) > 1:
    list = [0] * len(arg)
    visited = set()
    cc = 1

    def dfsIndex(node, index):
        if node not in visited:
            visited.add(node)
            list[index] = cc
            for neighbor in graph[node]:
                dfsIndex(neighbor, arg.index(neighbor))

    for i in range(len(list)):
        if list[i] == 0:
            dfsIndex(arg[i], i)
            cc += 1

    listMax = 0
    for num in list:
        if num > listMax:
            listMax = num
    sizes = []
    diffSizes = set()
    temp = 0
    for i in range(listMax): #for each component
        count = list.count(i) #get the size of the component
        if count > temp:
            temp = count
        sizes.append(count) #add the size of the component to sizes
        diffSizes.add(count)

    dict[5] = 'Connected component size count: ' + str(len(diffSizes)-1)
    dict[6] = 'Largest component size: ' + str(temp)

    k2count = 0
    for key in graph.keys():
        if len(graph[key]) == 1 and len(graph[min(graph[key])]) == 1:
            k2count += 1

    k3count = 0
    for key in graph.keys():
        if len(graph[key]) == 2:
            key1 = min(graph[key])
            key2 = max(graph[key])
            if graph[key1] == set((key, key2)) and graph[key2] == set((key, key1)):
                k3count += 1

    k4count = 0
    for key in graph.keys():
        if len(graph[key]) == 3:
            temp = [elem for elem in graph[key]]
            key1 = temp[0]
            key2 = temp[1]
            key3 = temp[2]
            if graph[key1] == set((key, key2, key3)) and graph[key2] == set((key, key1, key3)) and graph[key3] == set((key, key1, key2)):
                k4count += 1

    dict[7] = 'K2 Count: ' + str(k2count // 2)
    dict[8] = 'K3 Count: ' + str(k3count // 3)
    dict[9] = 'K4 Count: ' + str(k4count // 4)

    dict[10] = 'Neighbors: ' + str(graph[args[1]])

    processing = [args[1]]
    level = {args[1]: 0}

    ptr = 0
    while ptr < len(processing):
        val = processing[ptr]
        for nbr in graph[val]:
            if nbr not in level:
                level[nbr] = level[val] + 1
                processing.append(nbr)
        ptr += 1

    dict[11] = 'Farthest: ' + str(processing[ptr-1])

    parseMe = [args[1]]
    nodesSeen = {args[1] : 'rootIndicator'}
    if list[arg.index(args[1])] == list[arg.index(args[2])]:
        pointer = 0
        while pointer < len(parseMe):
            node = parseMe[pointer]
            for neighbor in graph[node]:
                if neighbor not in nodesSeen:
                    parseMe.append(neighbor)
                    nodesSeen[neighbor] = node
            if args[2] in nodesSeen:
                path = []
                lastNode = args[2]
                while nodesSeen[lastNode] != 'rootIndicator':
                    path.append(lastNode)
                    lastNode = nodesSeen[lastNode]
                path.append(lastNode)
                dict[12] = 'Path: ' + str(path[::-1])
                pointer = len(parseMe)
            pointer += 1

    else:
        dict[12] = 'Path: []'

end = 4
if len(args) > 1:
    end = 13

for i in range(end):
    print(dict[i])

#Vishal Kotha, 4, 2023