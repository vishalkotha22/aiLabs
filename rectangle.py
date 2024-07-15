import sys; args = sys.argv[1:]
#rect = args[1]
global width, height

def vert(rect):
    cols = []
    for i in range(width):
        col = []
        for j in range(height):
            col.append(rect[j*width+i])
        cols.append(col)
    cols = cols[::-1]
    build = ''
    for i in range(height):
        for j in range(width):
            build += cols[j][i]
    return build

def horiz(rect):
    rows = []
    for i in range(height):
        rows.append(rect[i*width:(i+1)*width])
    if len(rows)%2 == 0:
        start = len(rows) // 2
        reorder = []
        for j in range(len(rows)-1, start, -1):
            reorder.append(rows[j])
        for j in range(start, -1, -1):
            reorder.append(rows[j])
        build = ''
        for r in reorder:
            build += ''.join(r)
        return build
    else:
        start = (len(rows) // 2) + 1
        end = (len(rows) // 2) - 1
        reorder = []
        for i in range(len(rows)-1, len(rows)//2, -1):
            reorder.append(rows[i])
        for j in range(len(rows)//2, -1, -1):
            reorder.append(rows[j])
        build = ''
        for r in reorder:
            build += ''.join(r)
        return build

def mainDiagonal(rect):
    rows = []
    for i in range(height):
        rows.append(rect[i * width:(i + 1) * width])
    build = ''
    for i in range(width):
        for r in rows:
            build += r[i]
    return build

def backDiagonal(rect):
    return horiz(vert(mainDiagonal(rect)))

def rotate90(puzzle, width, height):
    rows = []
    for h in range(height):
        rows.append(puzzle[h*width:h*width + width])
    rows = rows[::-1]
    newPuzzle = ''
    for w in range(width):
        for row in rows:
            newPuzzle += row[w]
    return newPuzzle

def rotate180(puzzle):
    return rotate90(rotate90(puzzle, width, height), height, width)

def rotate270(pzl):
    return rotate180(rotate90(pzl, width, height))

rect = args[0]
if len(args) > 1:
    width = int(args[1])
    height = len(rect) // width
else:
    width, height = -1, -1
    if int(len(rect)**0.5) == len(rect)**0.5:
        min = int(len(rect)**0.5)
    else:
        min = int(len(rect)**0.5)+1
    for i in range(min, len(rect)):
        if len(rect)%i == 0:
            width = i
            break
    height = len(rect) // width

'''
def recur(adder, transformations, pzl):
    adder.append(pzl)
    if len(transformations) == 4:
        return
    else:
        for t in transformations:
            temp = transformations[:]
            temp.remove(t)
            cop = pzl[:]
            if t == 1:
                cop = rotate90(cop, width, height)
            elif t == 2:
                cop = rotate180(cop)
            elif t == 3:
                cop = rotate270(cop)
            elif t == 4:
                cop = vert(cop)
            elif t == 5:
                cop = horiz(cop)
            elif t == 6:
                cop = mainDiagonal(cop)
            elif t == 7:
                cop = backDiagonal(cop)
            recur(adder, temp, cop)
'''

unique = set()
unique.add(rect)
unique.add(vert(rect))
unique.add(horiz(rect))
unique.add(mainDiagonal(rect))
unique.add(backDiagonal(rect))
unique.add(rotate90(rect, width, height))
unique.add(rotate180(rect))
unique.add(rotate270(rect))

print(width, height)

for u in {*unique}:
    print(u)

#Vishal Kotha, 4, 2023