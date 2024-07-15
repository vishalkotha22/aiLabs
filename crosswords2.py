import sys; args = sys.argv[1:]
fin = open(args[0], 'r')
import math, random, re, time

global width, height


def main():
    global width, height
    startTime = time.time()
    width, height, blocks, seeds = 8, 8, 32, []
    words = fin.read()
    words = set(re.findall('^\w{3,}$', words, re.MULTILINE))
    height = int(args[1][:args[1].index('x')])
    width = int(args[1][args[1].index('x') + 1:])
    if len(args) >= 2:
        blocks = int(args[2])
        if len(args) > 2:
            seeds = args[3:]
    board = '-' * (width * height)
    for seed in seeds:
        orientation = seed[0]
        seed = seed[1:]
        vertPos = int(seed[0:seed.index('x')])
        rest = seed[seed.index('x') + 1:]
        slicer = re.findall('^\d*', rest)[0]
        horizPos = int(rest[:len(slicer)])
        word = rest[len(slicer):]
        startPos = vertPos * width + horizPos
        if orientation.lower() == 'h':
            board = board[:startPos] + word + board[startPos + len(word):]
        else:
            for r in range(len(word)):
                loc = startPos + r * width
                board = board[:loc] + word[r] + board[loc + 1:]
    for i in range(len(board)):
        if board[i] == '#':
            board = board[:len(board) - 1 - i] + '#' + board[len(board) - i:]
    # adder = set()
    # recur2(board, blocks - board.count('#'), adder)
    # for add in adder:
    # display(add)
    # print()
    # print(len(adder))
    board = recur(board, blocks - board.count('#'))
    #display(board)
    board = bruteForce(board, words)
    display(board)
    print(time.time() - startTime)


def display(board):
    for r in range(len(board) // width):
        print(board[r * width:(r + 1) * width])


def isSymmetric(board):
    tempBoard = board[:]
    for i, c in enumerate(board):
        if c != '-' and c != '#':
            tempBoard = tempBoard[:i] + '-' + tempBoard[i + 1:]
    if tempBoard[::-1] != tempBoard:
        return False
    return True


def isHorizVert(board):
    for i in range(len(board)):
        if board[i] != '#':
            vertical = False
            if i // width > 0 and i // width < height - 1:
                if board[i - width] != '#' and board[i + width] != '#':
                    vertical = True
            if i // width < height - 2:
                if board[i + width] != '#' and board[i + width * 2] != '#':
                    vertical = True
            if i // width > 1:
                if board[i - width] != '#' and board[i - width * 2] != '#':
                    vertical = True
            horizontal = False
            if i % width > 0 and i % width < width - 1:
                if board[i - 1] != '#' and board[i + 1] != '#':
                    horizontal = True
            if i % width > 1:
                if board[i - 2] != '#' and board[i - 1] != '#':
                    horizontal = True
            if i % width < width - 2:
                if board[i + 1] != '#' and board[i + 2] != '#':
                    horizontal = True
            if vertical == False or horizontal == False:
                return [False, i]
    return [True]


def findAllHorizontalPos(board):
    indices = set()
    for i, c in enumerate(board):
        if i % width == 0 and board[i] != '#':
            indices.add(i)
        elif board[i - 1] == '#':
            indices.add(i)
    templates = {}
    for idx in indices:
        build = ''
        temp = idx
        while temp % width < width - 1 and board[temp] != '#':
            build += board[temp]
            temp += 1
        if temp % width == width - 1 and board[temp] != '#':
            build += board[temp]
        templates[idx] = build
    return templates

def bruteForce(board, words):
    templates = findAllHorizontalPos(board)
    wordsPlaced = set()
    for idx in templates:
        fill = templates[idx].replace('-', '.').lower()
        for word in words:
            if word not in wordsPlaced and re.match('^'+fill+'$', word):
                wordsPlaced.add(word)
                board = board[:idx] + word + board[idx+len(word):]
                break
    return board

def recur(board, needed):
    if board != '#' * (width * height) and isConnected(board, set(), board.index('-')) != (
            len(board) - board.count('#')):
        if needed == 0:
            return 'FALSE'
        temp = set()
        for i in range(len(board)):
            if board[i] == '-':
                temp.add(i)
        ccs = []
        while len(temp) > 0:
            ret = set()
            getConnectedComponent(board, ret, temp.pop())
            temp = temp.difference(ret)
            ccs.append(ret)
        for cc in ccs:
            if len(cc) <= needed:
                tempBoard = board[:]
                for c in cc:
                    tempBoard = tempBoard[:c] + '#' + tempBoard[c + 1:]
                res = recur(tempBoard, needed - len(cc))
                if res != 'FALSE':
                    return res
        return 'FALSE'
    tup = isHorizVert(board)
    if tup[0] == False:
        if needed == 0:
            return 'FALSE'
        if board[tup[1]] == '-':
            board = board[:tup[1]] + '#' + board[tup[1] + 1:]
            if needed - 1 == 0 and board == '#' * (width * height):
                return board
            result = 'FALSE'
            if width % 2 == 1 and height % 2 == 1 and tup[1] == len(board) // 2:
                result = recur(board, needed - 1)
            elif board[len(board) - 1 - tup[1]] == '-':
                board = board[:len(board) - 1 - tup[1]] + '#' + board[len(board) - tup[1]:]
                result = recur(board, needed - 2)
            return result
    else:
        if needed == 0:
            if isSymmetric(board):
                return board
            return 'FALSE'
        for i in range(len(board)):
            if board[i] == '-' and board[len(board) - i - 1] == '-':
                tempBoard = board[:i] + '#' + board[i + 1:]
                result = 'FALSE'
                if width % 2 == 1 and height % 2 == 1 and i == len(board) // 2:
                    result = recur(tempBoard, needed - 1)
                elif needed > 1:
                    tempBoard = tempBoard[:len(board) - 1 - i] + '#' + tempBoard[len(board) - i:]
                    result = recur(tempBoard, needed - 2)
                if result != 'FALSE':
                    return result
    return 'FALSE'


def recur2(board, needed, adder):
    if board != '#' * (width * height) and isConnected(board, set(), board.index('-')) != (
            len(board) - board.count('#')):
        if needed == 0:
            return
        temp = set()
        for i in range(len(board)):
            if board[i] == '-':
                temp.add(i)
        ccs = []
        while len(temp) > 0:
            ret = set()
            getConnectedComponent(board, ret, temp.pop())
            temp = temp.difference(ret)
            ccs.append(ret)
        for cc in ccs:
            if len(cc) <= needed:
                tempBoard = board[:]
                for c in cc:
                    tempBoard = tempBoard[:c] + '#' + tempBoard[c + 1:]
                recur2(tempBoard, needed - len(cc), adder)
    tup = isHorizVert(board)
    if tup[0] == False:
        if needed == 0:
            return
        if board[tup[1]] == '-' and needed > 0:
            board = board[:tup[1]] + '#' + board[tup[1] + 1:]
            if needed == 1 and board == '#' * (width * height):
                adder.add(board)
                return
            if width % 2 == 1 and height % 2 == 1 and tup[1] == len(board) // 2:
                recur2(board, needed - 1, adder)
            elif board[len(board) - 1 - tup[1]] == '-':
                board = board[:len(board) - 1 - tup[1]] + '#' + board[len(board) - tup[1]:]
                recur2(board, needed - 2, adder)
    else:
        if needed == 0:
            if isSymmetric(board):
                adder.add(board)
            return
        for i in range(len(board)):
            if board[i] == '-' and board[len(board) - i - 1] == '-' and needed > 0:
                tempBoard = board[:i] + '#' + board[i + 1:]
                if width % 2 == 1 and height % 2 == 1 and i == len(board) // 2:
                    recur2(tempBoard, needed - 1, adder)
                elif needed > 1:
                    tempBoard = tempBoard[:len(board) - 1 - i] + '#' + tempBoard[len(board) - i:]
                    recur2(tempBoard, needed - 2, adder)
        return


def isConnected(board, visited, i):
    if board.index('-') == -1:
        return -1
    if i in visited:
        return 0
    visited.add(i)
    if board[i] == '#':
        return 0
    count = 1
    if i % width > 0:
        count += isConnected(board, visited, i - 1)
    if i % width < width - 1:
        count += isConnected(board, visited, i + 1)
    if i >= width:
        count += isConnected(board, visited, i - width)
    if i < (height - 1) * width:
        count += isConnected(board, visited, i + width)
    return count


def getConnectedComponent(board, comp, i):
    if i in comp:
        return
    if board[i] != '-':
        return
    comp.add(i)
    if i % width > 0:
        getConnectedComponent(board, comp, i - 1)
    if i % width < width - 1:
        getConnectedComponent(board, comp, i + 1)
    if i >= width:
        getConnectedComponent(board, comp, i - width)
    if i < (height - 1) * width:
        getConnectedComponent(board, comp, i + width)


if __name__ == '__main__':
    main()
    # incremental set repair: use distance to block as a heuristic, and it can be incrementally updated since only 1 or 2 blocks
    #                        are added at a time

# Vishal Kotha, 4, 2023