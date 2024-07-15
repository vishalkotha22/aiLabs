from math import pi , acos , sin , cos , sqrt
import tkinter as tk
import matplotlib.pyplot as plt
import cv2

root = tk.Tk()
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root)
background_image = tk.PhotoImage(file='rrMapBlank.png')
canvas.pack(fill=tk.BOTH, expand=True)
image = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

def convertCoordsToXY(x, y):
   #newX = (782 - (float(x) - 14.686730))
   #newY = (130.35722 + float(y)) * 8.38 + 153.7
   newX = -17.73538656 * float(x) + 1040.646346
   newY = 12.680550096 * float(y) + 1695.1254
   return [newY, newX]

#Miami: (695, 574) vs. (25.789350, -80.206630)
#Seattle: (149, 221) vs. (47.598480, -122.327970)
#Latitude Extrema: 14.686730 vs. 60.846820
#Longitude Extrema: -130.35722 vs. -60.02403
#Dimensions: 1060 by 782
#(774, 692)

def calcd(y1,x1, y2,x2):
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * R

nodeCoords = {}
lats = []
longs = []
for line in open('rrNodes.txt', 'r').read().splitlines():
   key, latitude, longitude = line.split(' ')
   lats.append(float(latitude))
   longs.append(float(longitude))
   nodeCoords[key] = (latitude, longitude)

cityNode = {}
for line in open('rrNodeCity.txt', 'r').read().splitlines():
   node, *city = line.split(' ')
   cityNode[' '.join(city)] = node

edges = {}
for line in open('rrEdges.txt', 'r').read().splitlines():
   loc1, loc2 = line.split(' ')
   if not loc1 in edges:
      edges[loc1] = set()
   edges[loc1].add(loc2)
   if not loc2 in edges:
      edges[loc2] = set()
   edges[loc2].add(loc1)
   #ax, ay = convertCoordsToXY(nodeCoords[loc1][0], nodeCoords[loc1][1])
   #bx, by = convertCoordsToXY(nodeCoords[loc2][0], nodeCoords[loc2][1])
   #canvas.create_line(ax, ay, bx, by, fill='white')

def helper(start, goal):
   return calcd(nodeCoords[start][0], nodeCoords[start][1], nodeCoords[goal][0], nodeCoords[goal][1])

batchSize = 5000

def aStar(start, goal):
   openSet = [(helper(start, goal), start, 'start', 0)]
   closedSet = {}
   counter = 0
   while openSet:
      openSet = sorted(openSet)
      estimate, key, parent, travelled = openSet.pop(0)
      if key == goal:
         path = [key]
         while parent != 'start':
            path.append(parent)
            parent = closedSet[parent]
         root.update()
         return (travelled, path[::-1])
      if key in closedSet:
         canvas.create_arc(endX - 6, endY - 6, endX + 6, endY + 6, fill='red')
         #canvas.create_line(startX1, startY1, endX, endY, fill='red')
         continue
      else:
         coords = nodeCoords[key]
         endX, endY = convertCoordsToXY(coords[0], coords[1])
         #canvas.create_line(startX1, startY1, endX, endY, fill='red')
         canvas.create_arc(endX - 6, endY - 6, endX + 6, endY + 6, fill='red')
         counter += 1
         if counter >= batchSize:
            root.update()
            counter = 0
         closedSet[key] = parent
      coords = nodeCoords[key]
      for edge in edges[key]:
         travelledNew = travelled + helper(key, edge)
         distanceToGo = helper(edge, goal)
         location = nodeCoords[edge]
         endX, endY = convertCoordsToXY(location[0], location[1])
         #canvas.create_line(startX, startY, endX, endY, fill='blue')
         canvas.create_arc(endX-6, endY-6, endX+6, endY+6, fill='blue')
         counter += 1
         if counter >= batchSize:
            root.update()
            counter = 0
         openSet.append((travelledNew + distanceToGo, edge, key, travelledNew))

city1 = cityNode[input('What is the start location?')]
city2 = cityNode[input('What is the destination?')]
distance, path = aStar(city1, city2)
print(distance, len(path))
print(nodeCoords[city1])
print(nodeCoords[city2])
print(path)

for i in range(len(path)-1):
   startX, startY = nodeCoords[path[i]]
   endX, endY = nodeCoords[path[i+1]]
   bx, by = convertCoordsToXY(endX, endY)
   #canvas.create_line(ax, ay, bx, by, fill='green')
   canvas.create_arc(bx-4, by-4, bx+4, by+4, fill='green')
   if i%25 == 0:
      root.update()

print(distance, len(path))

root.wm_geometry('1060x782')
root.mainloop()