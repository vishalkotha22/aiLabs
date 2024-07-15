import sys; args = sys.argv[1:]
from PIL import Image; #img = Image.open(args[0])
import math, random, re
img = Image.open('regiontest.jpg')
k = 3 #k = int(args[1])
width, height = img.size
pix = img.load()

centers = []
while len(centers) < k:
    adder = pix[int(random.random() * width), int(random.random() * height)]
    if adder not in centers:
        centers.append(adder)
buckets = {}
commonality = {}
for i in range(width):
    for j in range(height):
        if pix[i, j] not in commonality:
            commonality[pix[i, j]] = 0
        commonality[pix[i, j]] += 1
maxCount = max([*commonality.values()])
maxPixel = ()
for k in commonality:
    if commonality[k] == maxCount:
        maxPixel = k
        break

newCenters = centers[:]
generations = 0
storage = {}

while True:
    generations += 1
    cache = {}
    storage.clear()
    buckets.clear()
    for center in newCenters:
        buckets[center] = set()
    for i in range(width):
        for j in range(height):
            closestCenter, closestDist = (), 10000000
            if pix[i, j] in cache:
                buckets[cache[pix[i, j]]].add((i, j))
            else:
                for center in newCenters:
                    dist = (pix[i, j][0] - center[0]) * (pix[i, j][0] - center[0]) + (pix[i, j][1] - center[1]) * (pix[i, j][1] - center[1]) + (pix[i, j][2] - center[2]) * (pix[i, j][2] - center[2])
                    if dist < closestDist:
                        closestCenter = center
                        closestDist = dist
                cache[pix[i, j]] = closestCenter
                buckets[closestCenter].add((i, j))
    tempCenters = []
    comp = []
    breaker = True
    for k in newCenters:
        storage[k] = buckets[k]
        comp.append(len(buckets[k]))
        r, g, b = 0, 0, 0
        for x, y in buckets[k]:
            r += pix[x, y][0]
            g += pix[x, y][1]
            b += pix[x, y][2]
        tempCenters.append((r / len(buckets[k]), g / len(buckets[k]), b / len(buckets[k])))
        buckets[tempCenters[-1]] = buckets[k]
        if tempCenters[-1] != k:
            breaker = False
        del buckets[k]
    newCenters = tempCenters
    if breaker:
        break

for k in storage:
    for coord in storage[k]:
        pix[coord[0], coord[1]] = (int(k[0]), int(k[1]), int(k[2]))

print(f'Size: {width} x {height}')
print('Pixels:', height * width)
print('Distinct Pixel Count:', len(commonality.keys()))
print(f'Most common pixel: {maxPixel} -> {commonality[maxPixel]}')
print('Final means:')
for i, k in enumerate(storage):
    print(f'{i+1}: {k} => {len(storage[k])}')
locs = {}
for k in storage:
    locs[(int(k[0]), int(k[1]), int(k[2]))] = set()
for i in range(width):
    for j in range(height):
        locs[pix[i, j]].add((i, j))
regionCts = [0] * len(storage.keys())
for i, val in enumerate(locs):
    visited = set()
    while len(visited) < len(locs[val]):
        regionCts[i] += 1
        loc = locs[val].difference(visited).pop()
        queue = [loc]
        visited.add(loc)
        for x, y in queue:
            left = x > 0
            right = x < width-1
            top = y > 0
            bottom = y < height-1
            if left and pix[x-1, y] == val and (x-1, y) not in visited:
                queue.append((x-1, y))
                visited.add((x-1, y))
            if left and top and pix[x-1, y-1] == val and (x-1, y-1) not in visited:
                queue.append((x-1, y-1))
                visited.add((x-1, y-1))
            if top and pix[x, y-1] == val and (x, y-1) not in visited:
                queue.append((x, y-1))
                visited.add((x, y-1))
            if top and right and pix[x+1, y-1] == val and ((x+1, y-1)) not in visited:
                queue.append((x+1, y-1))
                visited.add((x+1, y-1))
            if right and pix[x+1, y] == val and ((x+1, y)) not in visited:
                queue.append((x+1, y))
                visited.add((x+1, y))
            if right and bottom and pix[x+1, y+1] == val and ((x+1, y+1)) not in visited:
                queue.append((x+1, y+1))
                visited.add((x+1, y+1))
            if bottom and pix[x, y+1] == val and ((x, y+1)) not in visited:
                queue.append((x, y+1))
                visited.add((x, y+1))
            if bottom and left and pix[x-1, y+1] == val and ((x-1, y+1)) not in visited:
                queue.append((x-1, y+1))
                visited.add((x-1, y+1))
'''
for i, val in enumerate(locs):
    temp = locs[val]
    while temp:
        regionCts[i] += 1
        queue = [temp.pop()]
        for x, y in queue:
            left = x > 0
            right = x < width-1
            top = y > 0
            bottom = y < height-1
            if left and top and pix[x-1, y-1] == val and (x-1, y-1) in temp:
                queue.append((x-1, y-1))
                temp.remove((x-1, y-1))
            if left and pix[x-1, y] == val and (x-1, y) in temp:
                queue.append((x-1, y))
                temp.remove((x-1, y))
            if top and pix[x, y-1] == val and (x, y-1) in temp:
                queue.append((x, y-1))
                temp.remove((x, y-1))
            if right and pix[x+1, y] == val and (x+1, y) in temp:
                queue.append((x+1, y))
                temp.remove((x+1, y))
            if right and bottom and pix[x+1, y+1] == val and (x+1, y+1) in temp:
                queue.append((x+1, y+1))
                temp.remove((x+1, y+1))
            if right and top and pix[x+1, y-1] == val and (x+1, y-1) in temp:
                queue.append((x+1, y-1))
                temp.remove((x+1, y-1))
            if bottom and pix[x, y+1] == val and (x, y+1) in temp:
                queue.append((x, y+1))
                temp.remove((x, y+1))
            if left and bottom and pix[x-1, y+1] == val and (x+1, y+1) in temp:
                queue.append((x-1, y+1))
                temp.remove((x-1, y+1))
'''
print('Region counts:', ', '.join([str(x) for x in regionCts]))

img.save('results.png', 'PNG')
#img.save("kmeans/{}.png".format('2023vkotha'), "PNG")
#Vishal Kotha, 4, 2023