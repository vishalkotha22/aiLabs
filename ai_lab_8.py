import sys; args = sys.argv[1:]
import time, math, random, re

global boardWidth, boardHeight

def display(board):
    for r in range(boardHeight):
        print(board[r*boardWidth:(r+1)*boardWidth])
'''
def possibleMoves(board, token):
    possible = set()
    if token == 'x':
        opponent = 'o'
    else:
        opponent = 'x'
    for j in range(len(board)):
        if board[j] == token:
            cDiff = j%boardWidth
            temp = 1
            while temp < cDiff and j-temp >= 0 and board[j-temp] == opponent:
                temp += 1
            if temp > 1 and j-temp >= 0 and board[j-temp] == '.':
                possible.add(j-temp)
            temp = 1
            while cDiff+temp < boardWidth and j+temp < len(board) and board[j+temp] == opponent:
                temp += 1
            if temp > 1 and j+temp < len(board) and board[j+temp] == '.':
                possible.add(j+temp)
            rDiff = j//boardWidth
            temp = 1
            while temp < rDiff and j-temp*boardWidth >= 0 and board[j-temp*boardWidth] == opponent:
                temp += 1
            if temp > 1 and j-temp*boardWidth >= 0 and board[j-temp*boardWidth] == '.':
                possible.add(j-temp*boardWidth)
            temp = 1
            while rDiff+temp < boardHeight and j+temp*boardWidth < len(board) and board[j+temp*boardWidth] == opponent:
                temp += 1
            if temp > 1 and j+temp*boardWidth < len(board) and board[j+temp*boardWidth] == '.':
                possible.add(j+temp*boardWidth)
            temp = 1
            while temp < min(cDiff, rDiff) and j-temp*boardWidth-temp >= 0 and board[j-temp*boardWidth-temp] == opponent:
                temp += 1
            if temp > 1 and j-temp*boardWidth-temp >= 0 and board[j-temp*boardWidth-temp] == '.':
                possible.add(j-temp*boardWidth-temp)
            temp = 1
            while (cDiff+temp < boardWidth and rDiff+temp < boardHeight) and j+temp*boardWidth+temp < len(board) and board[j+temp*boardWidth+temp] == opponent:
                temp += 1
            if temp > 1 and j+temp*boardWidth+temp < len(board) and board[j+temp*boardWidth+temp] == '.':
                possible.add(j+temp*boardWidth+temp)
            temp = 1
            while (temp < cDiff and rDiff+temp < boardHeight) and j + temp * boardWidth - temp < len(board) and board[j + temp * boardWidth - temp] == opponent:
                temp += 1
            if temp > 1 and j + temp * boardWidth - temp < len(board) and board[j + temp * boardWidth - temp] == '.':
                possible.add(j + temp * boardWidth - temp)
            temp = 1
            while (temp+cDiff < boardWidth and temp < rDiff) and j - temp * boardWidth + temp >= 0 and board[j - temp * boardWidth + temp] == opponent:
                temp += 1
            if temp > 1 and j - temp * boardWidth + temp >= 0 and board[j - temp * boardWidth + temp] == '.':
                possible.add(j - temp * boardWidth + temp)
    return possible
'''
def findMoves(board, token):
    possible = set()
    if token == 'x':
        opponent = 'o'
    else:
        opponent = 'x'
    for i, ch in enumerate(board):
        if ch == '.':
            if i%boardWidth > 0:
                temp = 1
                while (i-temp)%boardWidth > 0 and board[i-temp] == opponent:
                    temp += 1
                if temp > 1 and board[i-temp] == token:
                    possible.add(i)
                    continue
            if i%boardWidth < boardWidth-1:
                temp = 1
                while (i+temp)%boardWidth != boardWidth-1 and board[i+temp] == opponent:
                    temp += 1
                if temp > 1 and board[i+temp] == token:
                    possible.add(i)
                    continue
            if i//boardHeight > 0:
                temp = 1
                while i-temp*boardWidth >= boardWidth and board[i-temp*boardWidth] == opponent:
                    temp += 1
                if temp > 1 and board[i-temp*boardWidth] == token:
                    possible.add(i)
                    continue
            if i//boardWidth < boardHeight-1:
                temp = 1
                while i+temp*boardWidth < (boardHeight-1)*boardWidth and board[i+temp*boardWidth] == opponent:
                    temp += 1
                if temp > 1 and board[i+temp*boardWidth] == token:
                    possible.add(i)
                    continue
            if i%boardWidth > 0 and i//boardWidth > 0:
                temp = 1
                while i%boardWidth-temp > 0 and i-temp*boardWidth >= boardWidth and board[i-temp*boardWidth-temp] == opponent:
                    temp += 1
                if temp > 1 and board[i-temp*boardWidth-temp] == token:
                    possible.add(i)
                    continue
            if i%boardWidth < boardWidth-1 and i//boardWidth < boardHeight-1:
                temp = 1
                while (i+temp)%boardWidth < boardWidth-1 and i+temp*boardWidth < (boardHeight-1)*boardWidth and board[i+temp*boardWidth+temp] == opponent:
                    temp += 1
                if temp > 1 and board[i+temp*boardWidth+temp] == token:
                    possible.add(i)
                    continue
            if i%boardWidth > 0 and i//boardWidth < boardHeight-1:
                temp = 1
                while i%boardWidth-temp > 0 and i+temp*boardWidth < (boardHeight-1)*boardWidth and board[i+temp*boardWidth-temp] == opponent:
                    temp += 1
                if temp > 1 and board[i+temp*boardWidth-temp] == token:
                    possible.add(i)
                    continue
            if i%boardWidth < boardWidth-1 and i//boardWidth > 0:
                temp = 1
                while (i+temp)%boardWidth < boardWidth-1 and i-temp*boardWidth >= boardWidth and board[i-temp*boardWidth+temp] == opponent:
                    temp += 1
                if temp > 1 and board[i-temp*boardWidth+temp] == token:
                    possible.add(i)
                    continue
    return possible

def makeMove(board, token, i):
    if token == 'x':
        opponent = 'o'
    else:
        opponent = 'x'
    if i % boardWidth > 0:
        temp = 1
        while (i - temp) % boardWidth > 0 and board[i - temp] == opponent:
            temp += 1
        if temp > 1 and board[i - temp] == token:
            for j in range(temp):
                board = board[:i-j] + token + board[i-j+1:]
    if i % boardWidth < boardWidth - 1:
        temp = 1
        while (i + temp) % boardWidth != boardWidth - 1 and board[i + temp] == opponent:
            temp += 1
        if temp > 1 and board[i + temp] == token:
            for j in range(temp):
                board = board[:i+j] + token + board[i+j+1:]
    if i // boardHeight > 0:
        temp = 1
        while i - temp * boardWidth >= boardWidth and board[i - temp * boardWidth] == opponent:
            temp += 1
        if temp > 1 and board[i - temp * boardWidth] == token:
            for j in range(temp):
                board = board[:i-j*boardWidth] + token + board[i-j*boardWidth+1:]
    if i // boardWidth < boardHeight - 1:
        temp = 1
        while i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[i + temp * boardWidth] == opponent:
            temp += 1
        if temp > 1 and board[i + temp * boardWidth] == token:
            for j in range(temp):
                board = board[:i+j*boardWidth] + token + board[i+j*boardWidth+1:]
    if i % boardWidth > 0 and i // boardWidth > 0:
        temp = 1
        while i % boardWidth - temp > 0 and i - temp * boardWidth >= boardWidth and board[
            i - temp * boardWidth - temp] == opponent:
            temp += 1
        if temp > 1 and board[i - temp * boardWidth - temp] == token:
            for j in range(temp):
                board = board[:i-j*boardWidth-j] + token + board[i-j*boardWidth-j+1:]
    if i % boardWidth < boardWidth - 1 and i // boardWidth < boardHeight - 1:
        temp = 1
        while (i + temp) % boardWidth < boardWidth - 1 and i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[i + temp * boardWidth + temp] == opponent:
            temp += 1
        if temp > 1 and board[i + temp * boardWidth + temp] == token:
            for j in range(temp):
                board = board[:i+j*boardWidth+j] + token + board[i+j*boardWidth+j+1:]
    if i % boardWidth > 0 and i // boardWidth < boardHeight - 1:
        temp = 1
        while i % boardWidth - temp > 0 and i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[i + temp * boardWidth - temp] == opponent:
            temp += 1
        if temp > 1 and board[i + temp * boardWidth - temp] == token:
            for j in range(temp):
                board = board[:i+j*boardWidth-j] + token + board[i+j*boardWidth-j+1:]
    if i % boardWidth < boardWidth - 1 and i // boardWidth > 0:
        temp = 1
        while (i + temp) % boardWidth < boardWidth - 1 and i - temp * boardWidth >= boardWidth and board[i - temp * boardWidth + temp] == opponent:
            temp += 1
        if temp > 1 and board[i - temp * boardWidth + temp] == token:
            for j in range(temp):
                board = board[:i-j*boardWidth+j] + token + board[i-j*boardWidth+j+1:]
    return board

global digits
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def isStable(board, i, token):
    if token == 'x':
        opponent = 'o'
    else:
        opponent = 'x'
    horizontal = (i%boardWidth == 0) or (i%boardWidth == boardWidth-1)
    temp = i
    while temp%boardWidth > 0 and board[temp] == token:
        temp -= 1
    if board[temp] == token and temp%boardWidth == 0:
        horizontal = True
    temp = i
    while temp%boardWidth < boardWidth-1 and board[temp] == token:
        temp += 1
    if board[temp] == token and temp%boardWidth == boardWidth-1:
        horizontal = True
    vertical = (i // boardWidth == 0 or i // boardWidth == boardHeight-1)
    temp = i
    while temp - boardWidth >= boardWidth and board[temp] == token:
        temp -= boardWidth
    if board[temp] == token and temp < boardWidth:
        vertical = True
    temp = i
    while temp < (boardHeight - 1) * boardWidth and board[temp] == token:
        temp += boardWidth
    if board[temp] == token and temp >= (boardHeight - 1) * boardWidth:
        vertical = True
    mainDiagonal = (i%boardWidth == 0 or i//boardWidth == 0 or i%boardWidth == boardWidth-1 or i//boardWidth == boardHeight-1)
    otherDiagonal = mainDiagonal
    temp = i
    while temp%boardWidth > 0 and temp//boardWidth > 0 and board[temp] == token:
        temp = temp - boardWidth - 1
    if board[temp] == token and (temp%boardWidth == 0 or temp//boardWidth == 0):
        mainDiagonal = True
    temp = i
    while temp%boardWidth < boardWidth-1 and temp//boardWidth < boardHeight-1 and board[temp] == token:
        temp = temp + boardWidth + 1
    if board[temp] == token and (temp%boardWidth == boardWidth-1 or temp//boardWidth == boardHeight-1):
        mainDiagonal = True
    temp = i
    while temp%boardWidth < boardWidth-1 and temp//boardWidth > 0 and board[temp] == token:
        temp = temp + 1 - boardWidth
    if board[temp] == token and (temp//boardWidth == 0 and temp%boardWidth == boardWidth-1):
        otherDiagonal = True
    while temp%boardWidth > 0 and temp//boardWidth < boardHeight-1 and board[temp] == token:
        temp = temp - 1 + boardWidth
    if board[temp] == token and (temp%boardWidth == 0 or temp//boardWidth == boardHeight-1):
        otherDiagonal = True
    if (otherDiagonal and mainDiagonal and horizontal and vertical):
        return True
    left = (i%boardWidth == 0 or board[i-1] == opponent)
    right = (i%boardWidth == boardWidth-1 or board[i+1] == opponent)
    top = (i//boardWidth == 0 or board[i-boardWidth] == opponent)
    bottom = (i//boardWidth == boardHeight-1 or board[i+boardWidth] == opponent)
    topLeft = (i//boardWidth == 0 or i%boardWidth == 0 or board[i-boardWidth-1] == opponent)
    bottomRight = (i//boardWidth == boardHeight-1 or i%boardWidth == boardWidth-1 or board[i+boardWidth+1] == opponent)
    topRight = (i%boardWidth == boardHeight-1 or i//boardWidth == 0 or board[i-boardWidth+1] == opponent)
    bottomLeft = (i//boardWidth == boardHeight-1 or i%boardWidth == 0 or board[i+boardWidth-1] == opponent)
    return (left and right and top and bottom and topLeft and bottomRight and topRight and bottomLeft)

def filterMoves(moves):
    filtered = []
    for i, ch in enumerate(moves):
        if ch[0] not in digits and ch[0] != '-':
            ch = ch.lower()
            cols = ord(ch[0]) - ord('a')
            rows = (int(ch[1])-1) * boardWidth
            filtered.append(rows+cols)
        elif ch[0] != '-':
            filtered.append(int(ch))
    return filtered

boardWidth = 8
boardHeight = 8
corners = {0, 7, 56, 63}
close = {1 : 0,
         6 : 7,
         8 : 0,
         9 : 0,
         14 : 7,
         15 : 7,
         48 : 56,
         49 : 56,
         54 : 63,
         55 : 63,
         57 : 56,
         62 : 63}
csquares = {1 : 0,
            6 : 7,
            8 : 0,
            15 : 7,
            48 : 56,
            55 : 63,
            57 : 56,
            62 : 63}

'''
def quickMove(board, token):
    locs = findMoves(board, token)
    for loc in locs:
        board = board[:loc] + '*' + board[loc+1:]
    display(board)
    print('')
    for loc in locs:
        board = board[:loc] + '.' + board[loc+1:]
    xs = board.count('x')
    os = board.count('o')
    print(board, str(xs)+'/'+str(os))
    if locs:
        print('Possible moves for', token+':', str(locs)[1:-1])
        initial = -1
        bestPos = -1
        if token == 'x':
            opponent = 'o'
        else:
            opponent = 'x'
        for loc in locs:
            locs2 = []
            tempBoard = makeMove(board, token, loc)
            locs2 = findMoves(tempBoard, opponent)
            if len(locs2) == 0:
                heuristic2 = tempBoard.count(token)
                if heuristic2 > initial:
                    initial = heuristic2
                    bestPos = loc
            else:
                for loc2 in locs2:
                    temp2Board = makeMove(tempBoard, opponent, loc2)
                    heuristic3 = temp2Board.count(token)
                    if heuristic3 > initial:
                        initial = heuristic3
                        bestPos = loc
        print(bestPos)
        return bestPos
    else:
        print('No moves possible')
        return 'No moves possible'
'''
'''
def quickMove(board, token):
    locs = findMoves(board, token)
    for loc in locs:
        board = board[:loc] + '*' + board[loc+1:]
    display(board)
    print('')
    for loc in locs:
        board = board[:loc] + '.' + board[loc+1:]
    xs = board.count('x')
    os = board.count('o')
    print(board, str(xs)+'/'+str(os))
    if locs:
        print('Possible moves for', token+':', str(locs)[1:-1])
        #initial = -1
        bestPos = -1
        if token == 'x':
            opponent = 'o'
        else:
            opponent = 'x'
        for loc in locs:
            if loc in corners:
                bestPos = loc
                break
        for loc in locs:
            if bestPos == -1 and loc in close and board[close[loc]] == token:
                bestPos = loc
                break
        if bestPos == -1:
            cop = locs.copy()
            for loc in locs:
                if loc in corners or loc in close:
                    cop.remove(loc)
            minMoves = 100
            for loc in cop:
                tempBoard = makeMove(board, token, loc)
                comp = findMoves(tempBoard, opponent)
                if len(comp) < minMoves:
                    bestPos = loc
                    minMoves = len(comp)
            if bestPos == -1:
                bestPos = locs.pop()
        print(bestPos)
        return bestPos
    else:
        print('No moves possible')
        return 'No moves possible'
'''

def quickMove(board, token):
    locs = findMoves(board, token)
    for loc in locs:
        board = board[:loc] + '*' + board[loc+1:]
    display(board)
    print('')
    for loc in locs:
        board = board[:loc] + '.' + board[loc+1:]
    xs = board.count('x')
    os = board.count('o')
    print(board, str(xs)+'/'+str(os))
    if board.count('.') > 10:
        print('Possible moves for', token+':', str(locs)[1:-1])
        #initial = -1
        bestPos = -1
        if token == 'x':
            opponent = 'o'
        else:
            opponent = 'x'
        for loc in locs:
            if loc in corners:
                bestPos = loc
                break
        if bestPos == -1:
            for loc in locs:
                if loc in close and board[close[loc]] == token:
                    bestPos = loc
                    break
        if bestPos == -1:
            for loc in locs:
                tempBoard = makeMove(board, token, loc)
                if isStable(tempBoard, loc, token):
                    bestPos = loc
                    break
        if bestPos == -1:
            cop = locs.copy()
            for loc in locs:
                if loc in corners or loc in close:
                    cop.remove(loc)
            minMoves = 100
            for loc in cop:
                tempBoard = makeMove(board, token, loc)
                comp = {p for p in findMoves(tempBoard, opponent) if p not in corners or (p in close and tempBoard[close[p]] == opponent) or isStable(makeMove(board, opponent, p), p, opponent)}
                if len(comp) < minMoves:
                    bestPos = loc
                    minMoves = len(comp)
            if bestPos == -1:
                bestPos = locs.pop()
        print(bestPos)
        return bestPos
    else:
        print('Possible moves for', token + ':', str(locs)[1:-1])
        minScore, moveList = negamax(board, token, [])
        print('Min Score:', minScore, moveList)
        return moveList

def negamax(board, token, mvs):
    opponent = 'xo'.replace(token, '')
    if '.' not in board:
        return (board.count(token) - board.count(opponent), -1)
    possibilities = findMoves(board, token)
    if len(possibilities) == 0:
        if len(findMoves(board, opponent)) == 0:
            return (board.count(token) - board.count(opponent), -1)
        token = 'xo'.replace(token, '')
        return negamax(board, token, mvs+[-1])
    storage = {}
    #display(board)
    #print(findMoves(board, token))
    for mv in findMoves(board, token):
        seq = mvs[:]
        seq.append(mv)
        newBoard = makeMove(board, token, mv)
        #display(newBoard)
        storage[mv] = negamax(newBoard, opponent, seq)
    maxHeur = max([v[0] for v in storage.values()])
    for k in storage:
        if storage[k][0] == maxHeur:
            return (maxHeur, mvs+[k])

def main():
    while '' in args:
        args.remove(args.index(''))
    while ' ' in args:
        args.remove(args.index(' '))
    if len(args) == 0:
        board = '...........................ox......xo...........................'
        token = 'x'
        moves = []
    elif len(args[0]) == 64:
        board = args[0].lower()
        if len(args) == 1:
            token = 'x'
            if (board.count('x') + board.count('o')) % 2 == 1 or len(possibleMoves(board, token)) == 0:
                token = 'o'
            moves = []
        else:
            if args[1].lower() == 'x' or args[1].lower() == 'o':
                token = args[1].lower()
                if len(args) == 2:
                    moves = []
                else:
                    moves = args[2:]
            else:
                token = 'x'
                if (board.count('x') + board.count('o')) % 2 == 1 or len(possibleMoves(board, token)) == 0:
                    token = 'o'
                moves = args[1:]
    elif args[0].lower() == 'x' or args[0].lower() == 'o':
        board = '...........................ox......xo...........................'
        token = args[0].lower()
        if len(args) == 1:
            moves = []
        else:
            moves = args[1:]
    else:
        board = '...........................ox......xo...........................'
        token = 'x'
        moves = args
    moves = filterMoves(moves)
    quickMove(board, token)
    #negamax(board, token, [])

if __name__ == '__main__':
    main()

#Vishal Kotha, 4, 2023