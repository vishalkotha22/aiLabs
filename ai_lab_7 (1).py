import sys; args = sys.argv[1:]
#Vishal Kotha, 4
import time, math, random, re
#blocks = ' '.join(args)
blocks = input('What are the blocks?')
global boardWidth, boardHeight, fix, count

def display(board):
    for i in range(boardHeight):
        for c in range(boardWidth):
            print(board[i*boardWidth+c], end='')
        print()

def findCandidates(board, optim):
    locs = {}
    for area, rows, cols in optim:
        candidates = {j for j in range(len(board)) if board[j] == '.' and j % boardWidth + cols <= boardWidth and j // boardWidth + rows <= boardHeight}
        locs[(rows, cols)] = candidates
        temp = rows
        rows = cols
        cols = temp
        candidates = {j for j in range(len(board)) if board[j] == '.' and j % boardWidth + cols <= boardWidth and j // boardWidth + rows <= boardHeight}
        locs[(rows, cols)] = candidates
    return locs
'''
def bruteForce(board, opt, storage, candidates):
    #if time.time() - startTime > 2:
        #return ('', {})
    global count
    count += 1
    if len(opt) == 0:
        return (board, storage)
    sym = fix[len(opt)-1]
    area, rows, cols = max(opt)
    opt.remove((area, rows, cols))
    for candidate in candidates[(rows, cols)]:
        cand = candidates.copy()
        boardCopy = board.copy()
        passes = True
        w = candidate // boardWidth
        d = candidate % boardWidth
        indices = set()
        for r in range(w, w + rows):
            for c in range(d, d + cols):
                index = r * boardWidth + c
                # print(candidate, r, c, index)
                if boardCopy[index] != '.':
                    passes = False
                    break
                else:
                    boardCopy[index] = sym
                    indices.add(index)
            if passes == False:
                break
        if passes:
            for can in cand:
                cand[can] = cand[can] - indices
            storage[sym] = (rows, cols)
            # display(boardCopy)
            # print()
            bf = bruteForce(boardCopy, optim, storage, cand)
            if bf[0]:
                return bf
            del storage[sym]
    temp = rows
    rows = cols
    cols = temp
    for candidate in candidates[(rows, cols)]:
        cand = candidates.copy()
        boardCopy = board.copy()
        passes = True
        indices = set()
        w = candidate // boardWidth
        d = candidate % boardWidth
        for r in range(w, w + rows):
            for c in range(d, d + cols):
                index = r * boardWidth + c
                if boardCopy[index] != '.':
                    passes = False
                    break
                else:
                    boardCopy[index] = sym
                    indices.add(index)
            if passes == False:
                break
        if passes:
            storage[sym] = (rows, cols)
            for can in cand:
                cand[can] = cand[can] - indices
            # display(boardCopy)
            # print()
            bf = bruteForce(boardCopy, optim, storage, cand)
            if bf[0]:
                return bf
            del storage[sym]
    opt.append((area, rows, cols))
    return ('', {})
'''
'''
def bruteForce(board, opt, storage):
    #if time.time() - startTime > 2:
        #return ('', {})
    global count
    count += 1
    if len(opt) == 0:
        return (board, storage)
    sym = fix[len(opt)-1]
    area, rows, cols = max(opt)
    opt.remove((area, rows, cols))
    candidates = {j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight}
    if candidates:
        for candidate in candidates:
            boardCopy = board.copy()
            passes = True
            w = candidate // boardWidth
            d = candidate % boardWidth
            for r in range(w, w + rows):
                for c in range(d, d + cols):
                    index = r * boardWidth + c
                    #print(candidate, r, c, index)
                    if boardCopy[index] != '.':
                        passes = False
                        break
                    else:
                        boardCopy[index] = sym
                if passes == False:
                    break
            if passes:
                storage[sym] = (rows, cols)
                #display(boardCopy)
                #print()
                bf = bruteForce(boardCopy, optim, storage)
                if bf[0]:
                    return bf
                del storage[sym]
    temp = rows
    rows = cols
    cols = temp
    candidates = {j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight}
    if candidates:
        for candidate in candidates:
            boardCopy = board.copy()
            passes = True
            w = candidate // boardWidth
            d = candidate % boardWidth
            for r in range(w, w + rows):
                for c in range(d, d + cols):
                    index = r * boardWidth + c
                    if boardCopy[index] != '.':
                        passes = False
                        break
                    else:
                        boardCopy[index] = sym
                if passes == False:
                    break
            if passes:
                storage[sym] = (rows, cols)
                #display(boardCopy)
                #print()
                bf = bruteForce(boardCopy, optim, storage)
                if bf[0]:
                    return bf
                del storage[sym]
    opt.append((area, rows, cols))
    return ('', {})
'''

def visualize(occupied):
    board = {}
    for i in range(boardWidth*boardHeight):
        board[i] = '.'
    for i, occupy in enumerate(occupied):
        tlx, tly, brx, bry = occupy
        for r in range(tly, bry+1):
            for c in range(tlx, brx+1):
                board[r*boardWidth+c] = fix[i]
    #display(''.join([*board.values()]))
    return ''.join([*board.values()])
'''
def bruteForce(board, opt, storage, occupied):
    #if time.time() - startTime > 2:
        #return ('', {})
    global count
    count += 1
    if len(opt) == 0:
        return (board, storage, occupied)
    #working = visualize(occupied)
    area, rows, cols = max(opt)
    #print('before', findCandidates(working, opt)[(rows, cols)])
    opt.remove((area, rows, cols))
    candidates = []
    for j in range(boardWidth*boardHeight):
        #print('testing', j)
        if j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight:
            passes = True
            for occupy in occupied:
                tlx, tly, blx, bly = occupy
                if j % boardWidth + cols <= tlx or j % boardWidth > blx or j // boardWidth > bly or j // boardWidth + rows <= tly:
                    #print(j, 'passed')
                    continue
                else:
                    passes = False
                    break
            if passes:
                candidates.append(j)
    #print('after', candidates)
    if candidates:
        for candidate in candidates:
            occupying = occupied.copy()
            tlx = candidate%boardWidth
            tly = candidate // boardWidth
            blx = tlx + cols - 1
            bly = tly + rows - 1
            occupying.append((tlx, tly, blx, bly))
            storage[(tlx, tly, blx, bly)] = (rows, cols)
            # display(boardCopy)
            # print()
            bf = bruteForce(board, opt, storage, occupying)
            if bf[0]:
                return bf
            del storage[(tlx, tly, blx, bly)]
    temp = rows
    rows = cols
    cols = temp
    candidates = []
    for j in range(boardWidth*boardHeight):
        if j % boardWidth + cols <= boardWidth and j // boardWidth + rows <= boardHeight:
            passes = True
            for occupy in occupied:
                tlx, tly, blx, bly = occupy
                #print('testing', j)
                if j % boardWidth + cols <= tlx or j % boardWidth > blx or j // boardWidth > bly or j // boardWidth + rows <= tly:
                    #print(j, 'passed')
                    continue
                else:
                    passes = False
                    break
            if passes:
                candidates.append(j)
    if candidates:
        for candidate in candidates:
            occupying = occupied.copy()
            tlx = candidate % boardWidth
            tly = candidate // boardWidth
            blx = tlx + cols - 1
            bly = tly + rows - 1
            occupying.append((tlx, tly, blx, bly))
            storage[(tlx, tly, blx, bly)] = (rows, cols)
            # display(boardCopy)
            # print()
            bf = bruteForce(board, opt, storage, occupying)
            if bf[0]:
                return bf
            del storage[(tlx, tly, blx, bly)]
    opt.append((area, rows, cols))
    return ('', {}, [])
'''

def bruteForce(board, optim, storage):
    #if time.time() - startTime > 2:
        #return ('', {})
    global count
    count += 1
    if len(optim) == 0:
        return (board, storage)
    sym = fix[len(optim)-1]
    for area, rows, cols in optim:
        opt = optim.copy()
        opt.remove((area, rows, cols))
        #candidates = {j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight}
        display(board)
        if storage:
            candidates = [j for j in board if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight if (j%boardWidth>0 and board[j-1] != '.') or (j//boardWidth > 0 and board[j-boardWidth] != '.')]
        else:
            candidates = [j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight]
        #print(rows, cols, candidates)
        #display(board)
        print(rows, cols, candidates)
        if candidates:
            for candidate in candidates:
                boardCopy = board.copy()
                passes = True
                w = candidate // boardWidth
                d = candidate % boardWidth
                for r in range(w, w + rows):
                    for c in range(d, d + cols):
                        index = r * boardWidth + c
                        #print(candidate, r, c, index)
                        if boardCopy[index] != '.':
                            passes = False
                            break
                        else:
                            boardCopy[index] = sym
                    if passes == False:
                        break
                if passes:
                    storage[sym] = (rows, cols)
                    #display(boardCopy)
                    #print()
                    bf = bruteForce(boardCopy, opt, storage)
                    if bf[0]:
                        return bf
                    del storage[sym]
        temp = rows
        rows = cols
        cols = temp
        #candidates = [j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight]
        candidates = []
        if storage:
            candidates = [j for j in board if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight if (j%boardWidth>0 and board[j-1] != '.') or (j//boardWidth > 0 and board[j-boardWidth] != '.')]
        else:
            candidates = [j for j in range(len(board)) if board[j] == '.' and j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight]
        #display(board)
        print(rows, cols, candidates)
        if candidates:
            for candidate in candidates:
                boardCopy = board.copy()
                passes = True
                w = candidate // boardWidth
                d = candidate % boardWidth
                for r in range(w, w + rows):
                    for c in range(d, d + cols):
                        index = r * boardWidth + c
                        if boardCopy[index] != '.':
                            passes = False
                            break
                        else:
                            boardCopy[index] = sym
                    if passes == False:
                        break
                if passes:
                    storage[sym] = (rows, cols)
                    #display(boardCopy)
                    #print()
                    bf = bruteForce(boardCopy, opt, storage)
                    if bf[0]:
                        return bf
                    del storage[sym]
    return ('', {})

blockSizes = re.findall('\d+', blocks)
boardWidth = int(blockSizes[1])
boardHeight = int(blockSizes[0])
count = 0
blockSizes = blockSizes[2:]
rectRows = [int(blockSizes[i]) for i in range(len(blockSizes)) if i%2 == 0]
rectCols = [int(blockSizes[i]) for i in range(len(blockSizes)) if i%2 == 1]
optim = []
for i in range(len(rectRows)):
    optim.append((rectRows[i]*rectCols[i], rectRows[i], rectCols[i]))
optim.sort(reverse=True)
board = {}
for i in range(boardWidth*boardHeight):
    board[i] = '.'
fix = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
startTime = time.time()
solvedPzl, decomp = bruteForce(board, optim, {})
print(time.time() - startTime)
#solvedPzl = visualize(occupied)
build = {}
why = []
'''
for tup in occupied:
    tlx, tly, brx, bry = tup
    w = brx-tlx+1
    h = bry-tly+1
    why.append((tlx, tly))
    build[(tlx, tly)] = (tlx, tly, brx, bry)
'''
#display(solvedPzl)
#print(occupied)
#print(solvedPzl)
#print(occupied)
#visualize(occupied)
#display(''.join([*solvedPzl.values()]))
if solvedPzl:
    display(solvedPzl)
    print('Decomposition:', end=' ')
    symbols = set()
    for k in solvedPzl:
        ch = solvedPzl[k]
        if ch in decomp:
            if ch not in symbols:
                tup = decomp[ch]
                print(tup[0], tup[1], end=' ')
                symbols.add(ch)
        else:
            print('1 1', end=' ')
    #print(count, time.time())
else:
    print('No solution')

'''
import sys; args = sys.argv[1:]
#Vishal Kotha, 4
import time, math, random, re
blocks = ' '.join(args)
#blocks = input('What are the blocks?')
global boardWidth, boardHeight, startTime

def display(board):
    for i in range(boardHeight):
        print(board[i*boardWidth:(i+1)*boardWidth])

def bruteForce(board, rectRows, rectCols, storage):
    if time.time() - startTime > 10:
        return ('', {})
    if len(rectRows) == 0:
        return (board, storage)
    sym = str(len(rectRows)-1)
    for i in range(len(rectRows)):
        rows = rectRows[i]
        cols = rectCols[i]
        decomp = storage.copy()
        rowsCopy = rectRows.copy()
        colsCopy = rectCols.copy()
        del rowsCopy[i]
        del colsCopy[i]
        candidates = []
        for j in range(len(board)):
            if board[j] == '.':
                if j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight:
                    candidates.append(j)
        if candidates:
            for candidate in candidates:
                boardCopy = board[:]
                passes = True
                for r in range(candidate // boardWidth, candidate // boardWidth + rows):
                    for c in range(candidate % boardWidth, candidate % boardWidth + cols):
                        index = r * boardWidth + c
                        if boardCopy[index] != '.':
                            passes = False
                        else:
                            boardCopy = boardCopy[:index] + sym + boardCopy[index+1:]
                if passes:
                    decomp[sym] = (rows, cols)
                    bf = bruteForce(boardCopy, rowsCopy, colsCopy, decomp)
                    if bf:
                        return bf
        temp = rows
        rows = cols
        cols = temp
        candidates = []
        decomp = storage.copy()
        for j in range(len(board)):
            if board[j] == '.':
                if j%boardWidth+cols <= boardWidth and j//boardWidth+rows <= boardHeight:
                    candidates.append(j)
        if candidates:
            for candidate in candidates:
                boardCopy = board[:]
                passes = True
                for r in range(candidate // boardWidth, candidate // boardWidth + rows):
                    for c in range(candidate % boardWidth, candidate % boardWidth + cols):
                        index = r * boardWidth + c
                        if boardCopy[index] != '.':
                            passes = False
                        else:
                            boardCopy = boardCopy[:index] + sym + boardCopy[index+1:]
                if passes:
                    decomp[sym] = (rows, cols)
                    bf = bruteForce(boardCopy, rowsCopy, colsCopy, decomp)
                    if bf:
                        return bf
        else:
            continue
    return ''

blockSizes = re.findall('\d+', blocks)
boardWidth = int(blockSizes[1])
boardHeight = int(blockSizes[0])
blockSizes = blockSizes[2:]
rectRows = [int(blockSizes[i]) for i in range(len(blockSizes)) if i%2 == 0]
rectCols = [int(blockSizes[i]) for i in range(len(blockSizes)) if i%2 == 1]
board = '.' * (boardWidth * boardHeight)
startTime = time.time()
solvedPzl, decomp = bruteForce(board, rectRows, rectCols, {})
#display(solvedPzl)
if solvedPzl:
    print('Decomposition:', end=' ')
    symbols = set()
    for ch in solvedPzl:
        if ch in decomp:
            if ch not in symbols:
                tup = decomp[ch]
                print(tup[0], tup[1], end=' ')
                symbols.add(ch)
        else:
            print('1 1', end=' ')
else:
    print('No solution')

#Vishal Kotha, 4, 2023
'''

#Vishal Kotha, 4, 2023