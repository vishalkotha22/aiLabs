import sys; args = sys.argv[1:]
#Vishal Kotha, 4, 2023
LIMIT_AB = 14; DEPTH_AB = 4
#Percents: 78 80 78 79 79 80 82 83 81 84 83 84 84 85
#Times: 0.748 0.722 0.755 0.730 0.762 0.826 0.915 1.318 2.297 5.011 11.88 52.89 168.7 256.8
#114.2 89%, 14.79 80%, 14.98 69%

import time, math, random, re

def display(board):
 for r in range(boardHeight):
     print(board[r * boardWidth:(r + 1) * boardWidth])

foundPossibles = {}

def findMoves(board, token):
 global foundPossibles
 possible = set()
 if token == 'x':
     opponent = 'o'
 else:
     opponent = 'x'
 if (board, token) in foundPossibles:
     return foundPossibles[(board, token)]
 else:
     for i, ch in enumerate(board):
         if ch == '.':
             if i % boardWidth > 0:
                 temp = 1
                 while (i - temp) % boardWidth > 0 and board[i - temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i - temp] == token:
                     possible.add(i)
                     continue
             if i % boardWidth < boardWidth - 1:
                 temp = 1
                 while (i + temp) % boardWidth != boardWidth - 1 and board[i + temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i + temp] == token:
                     possible.add(i)
                     continue
             if i >= 8:
                 temp = 1
                 while i - temp * boardWidth >= boardWidth and board[i - temp * boardWidth] == opponent:
                     temp += 1
                 if temp > 1 and board[i - temp * boardWidth] == token:
                     possible.add(i)
                     continue
             if i < 56:
                 temp = 1
                 while i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[
                     i + temp * boardWidth] == opponent:
                     temp += 1
                 if temp > 1 and board[i + temp * boardWidth] == token:
                     possible.add(i)
                     continue
             if i % boardWidth > 0 and i >= 8:
                 temp = 1
                 while i % boardWidth - temp > 0 and i - temp * boardWidth >= boardWidth and board[
                     i - temp * boardWidth - temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i - temp * boardWidth - temp] == token:
                     possible.add(i)
                     continue
             if i % boardWidth < boardWidth - 1 and i < 56:
                 temp = 1
                 while (i + temp) % boardWidth < boardWidth - 1 and i + temp * boardWidth < (
                         boardHeight - 1) * boardWidth and board[i + temp * boardWidth + temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i + temp * boardWidth + temp] == token:
                     possible.add(i)
                     continue
             if i % boardWidth > 0 and i < 56:
                 temp = 1
                 while i % boardWidth - temp > 0 and i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[
                     i + temp * boardWidth - temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i + temp * boardWidth - temp] == token:
                     possible.add(i)
                     continue
             if i % boardWidth < boardWidth - 1 and i >= 8:
                 temp = 1
                 while (i + temp) % boardWidth < boardWidth - 1 and i - temp * boardWidth >= boardWidth and board[
                     i - temp * boardWidth + temp] == opponent:
                     temp += 1
                 if temp > 1 and board[i - temp * boardWidth + temp] == token:
                     possible.add(i)
                     continue
     foundPossibles[(board, token)] = possible
     return possible

movesMadeBefore = {}

def makeMove(board, token, i):
 global movesMadeBefore
 key = (board, token, i)
 if key in movesMadeBefore:
     return movesMadeBefore[key]
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
             board = board[:i - j] + token + board[i - j + 1:]
 if i % boardWidth < boardWidth - 1:
     temp = 1
     while (i + temp) % boardWidth != boardWidth - 1 and board[i + temp] == opponent:
         temp += 1
     if temp > 1 and board[i + temp] == token:
         for j in range(temp):
             board = board[:i + j] + token + board[i + j + 1:]
 if i // boardHeight > 0:
     temp = 1
     while i - temp * boardWidth >= boardWidth and board[i - temp * boardWidth] == opponent:
         temp += 1
     if temp > 1 and board[i - temp * boardWidth] == token:
         for j in range(temp):
             board = board[:i - j * boardWidth] + token + board[i - j * boardWidth + 1:]
 if i // boardWidth < boardHeight - 1:
     temp = 1
     while i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[i + temp * boardWidth] == opponent:
         temp += 1
     if temp > 1 and board[i + temp * boardWidth] == token:
         for j in range(temp):
             board = board[:i + j * boardWidth] + token + board[i + j * boardWidth + 1:]
 if i % boardWidth > 0 and i // boardWidth > 0:
     temp = 1
     while i % boardWidth - temp > 0 and i - temp * boardWidth >= boardWidth and board[
         i - temp * boardWidth - temp] == opponent:
         temp += 1
     if temp > 1 and board[i - temp * boardWidth - temp] == token:
         for j in range(temp):
             board = board[:i - j * boardWidth - j] + token + board[i - j * boardWidth - j + 1:]
 if i % boardWidth < boardWidth - 1 and i // boardWidth < boardHeight - 1:
     temp = 1
     while (i + temp) % boardWidth < boardWidth - 1 and i + temp * boardWidth < (boardHeight - 1) * boardWidth and \
             board[i + temp * boardWidth + temp] == opponent:
         temp += 1
     if temp > 1 and board[i + temp * boardWidth + temp] == token:
         for j in range(temp):
             board = board[:i + j * boardWidth + j] + token + board[i + j * boardWidth + j + 1:]
 if i % boardWidth > 0 and i // boardWidth < boardHeight - 1:
     temp = 1
     while i % boardWidth - temp > 0 and i + temp * boardWidth < (boardHeight - 1) * boardWidth and board[
         i + temp * boardWidth - temp] == opponent:
         temp += 1
     if temp > 1 and board[i + temp * boardWidth - temp] == token:
         for j in range(temp):
             board = board[:i + j * boardWidth - j] + token + board[i + j * boardWidth - j + 1:]
 if i % boardWidth < boardWidth - 1 and i // boardWidth > 0:
     temp = 1
     while (i + temp) % boardWidth < boardWidth - 1 and i - temp * boardWidth >= boardWidth and board[
         i - temp * boardWidth + temp] == opponent:
         temp += 1
     if temp > 1 and board[i - temp * boardWidth + temp] == token:
         for j in range(temp):
             board = board[:i - j * boardWidth + j] + token + board[i - j * boardWidth + j + 1:]
 movesMadeBefore[key] = board
 return board

global digits
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def filterMoves(moves):
 filtered = []
 for i, ch in enumerate(moves):
     if ch[0] not in digits and ch[0] != '-':
         ch = ch.lower()
         cols = ord(ch[0]) - ord('a')
         rows = (int(ch[1]) - 1) * boardWidth
         filtered.append(rows + cols)
     elif ch[0] != '-':
         filtered.append(int(ch))
 return filtered

neighbors = {0: [1, 9, 8], 1: [0, 2, 8, 10, 9], 2: [1, 3, 9, 11, 10], 3: [2, 4, 10, 12, 11], 4: [3, 5, 11, 13, 12], 5: [4, 6, 12, 14, 13], 6: [5, 7, 13, 15, 14], 7: [6, 14, 15], 8: [9, 1, 17, 0, 16], 9: [8, 10, 0, 16, 2, 18, 1, 17], 10: [9, 11, 1, 17, 3, 19, 2, 18], 11: [10, 12, 2, 18, 4, 20, 3, 19], 12: [11, 13, 3, 19, 5, 21, 4, 20], 13: [12, 14, 4, 20, 6, 22, 5, 21], 14: [13, 15, 5, 21, 7, 23, 6, 22], 15: [14, 6, 22, 7, 23], 16: [17, 9, 25, 8, 24], 17: [16, 18, 8, 24, 10, 26, 9, 25], 18: [17, 19, 9, 25, 11, 27, 10, 26], 19: [18, 20, 10, 26, 12, 28, 11, 27], 20: [19, 21, 11, 27, 13, 29, 12, 28], 21: [20, 22, 12, 28, 14, 30, 13, 29], 22: [21, 23, 13, 29, 15, 31, 14, 30], 23: [22, 14, 30, 15, 31], 24: [25, 17, 33, 16, 32], 25: [24, 26, 16, 32, 18, 34, 17, 33], 26: [25, 27, 17, 33, 19, 35, 18, 34], 27: [26, 28, 18, 34, 20, 36, 19, 35], 28: [27, 29, 19, 35, 21, 37, 20, 36], 29: [28, 30, 20, 36, 22, 38, 21, 37], 30: [29, 31, 21, 37, 23, 39, 22, 38], 31: [30, 22, 38, 23, 39], 32: [33, 25, 41, 24, 40], 33: [32, 34, 24, 40, 26, 42, 25, 41], 34: [33, 35, 25, 41, 27, 43, 26, 42], 35: [34, 36, 26, 42, 28, 44, 27, 43], 36: [35, 37, 27, 43, 29, 45, 28, 44], 37: [36, 38, 28, 44, 30, 46, 29, 45], 38: [37, 39, 29, 45, 31, 47, 30, 46], 39: [38, 30, 46, 31, 47], 40: [41, 33, 49, 32, 48], 41: [40, 42, 32, 48, 34, 50, 33, 49], 42: [41, 43, 33, 49, 35, 51, 34, 50], 43: [42, 44, 34, 50, 36, 52, 35, 51], 44: [43, 45, 35, 51, 37, 53, 36, 52], 45: [44, 46, 36, 52, 38, 54, 37, 53], 46: [45, 47, 37, 53, 39, 55, 38, 54], 47: [46, 38, 54, 39, 55], 48: [49, 41, 57, 40, 56], 49: [48, 50, 40, 56, 42, 58, 41, 57], 50: [49, 51, 41, 57, 43, 59, 42, 58], 51: [50, 52, 42, 58, 44, 60, 43, 59], 52: [51, 53, 43, 59, 45, 61, 44, 60], 53: [52, 54, 44, 60, 46, 62, 45, 61], 54: [53, 55, 45, 61, 47, 63, 46, 62], 55: [54, 46, 62, 47, 63], 56: [57, 49, 48], 57: [56, 58, 48, 50, 49], 58: [57, 59, 49, 51, 50], 59: [58, 60, 50, 52, 51], 60: [59, 61, 51, 53, 52], 61: [60, 62, 52, 54, 53], 62: [61, 63, 53, 55, 54], 63: [62, 54, 55]}
boardWidth, boardHeight = 8, 8
corners = {0, 7, 56, 63}
close = {1: 0, 6: 7, 8: 0, 9: 0, 14: 7, 15: 7, 48: 56, 49: 56,  54: 63,  55: 63,  57: 56, 62: 63}
revClose = {0 : [1, 8, 9], 7 : [6, 14, 15], 56 : [48, 49, 57], 63 : [54, 55, 62]}
csquares = {1: 0,  6: 7,  8: 0,  15: 7,  48: 56,  55: 63,  57: 56,    62: 63}

def snapshot(board, token):
  locs = findMoves(board, token)
  for loc in locs:
      board = board[:loc] + '*' + board[loc + 1:]
  display(board)
  print('')
  for loc in locs:
      board = board[:loc] + '.' + board[loc + 1:]
  xs = board.count('x')
  os = board.count('o')
  print(board, str(xs) + '/' + str(os))
  print('Possible moves for', token + ':', str(locs)[1:-1])

def isStable(board, i, token):
 if token == 'x':
     opponent = 'o'
 else:
     opponent = 'x'
 horizontal = (i % boardWidth == 0) or (i % boardWidth == boardWidth - 1)
 temp = i
 while temp % boardWidth > 0 and board[temp] == token:
     temp -= 1
 if board[temp] == token and temp % boardWidth == 0:
     horizontal = True
 temp = i
 while temp % boardWidth < boardWidth - 1 and board[temp] == token:
     temp += 1
 if board[temp] == token and temp % boardWidth == boardWidth - 1:
     horizontal = True
 vertical = (i // boardWidth == 0 or i // boardWidth == boardHeight - 1)
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
 mainDiagonal = (
             i % boardWidth == 0 or i // boardWidth == 0 or i % boardWidth == boardWidth - 1 or i // boardWidth == boardHeight - 1)
 otherDiagonal = mainDiagonal
 temp = i
 while temp % boardWidth > 0 and temp // boardWidth > 0 and board[temp] == token:
     temp = temp - boardWidth - 1
 if board[temp] == token and (temp % boardWidth == 0 or temp // boardWidth == 0):
     mainDiagonal = True
 temp = i
 while temp % boardWidth < boardWidth - 1 and temp // boardWidth < boardHeight - 1 and board[temp] == token:
     temp = temp + boardWidth + 1
 if board[temp] == token and (temp % boardWidth == boardWidth - 1 or temp // boardWidth == boardHeight - 1):
     mainDiagonal = True
 temp = i
 while temp % boardWidth < boardWidth - 1 and temp // boardWidth > 0 and board[temp] == token:
     temp = temp + 1 - boardWidth
 if board[temp] == token and (temp // boardWidth == 0 and temp % boardWidth == boardWidth - 1):
     otherDiagonal = True
 while temp % boardWidth > 0 and temp // boardWidth < boardHeight - 1 and board[temp] == token:
     temp = temp - 1 + boardWidth
 if board[temp] == token and (temp % boardWidth == 0 or temp // boardWidth == boardHeight - 1):
     otherDiagonal = True
 if (otherDiagonal and mainDiagonal and horizontal and vertical):
     return True
 left = (i % boardWidth == 0 or board[i - 1] == opponent)
 right = (i % boardWidth == boardWidth - 1 or board[i + 1] == opponent)
 top = (i // boardWidth == 0 or board[i - boardWidth] == opponent)
 bottom = (i // boardWidth == boardHeight - 1 or board[i + boardWidth] == opponent)
 topLeft = (i // boardWidth == 0 or i % boardWidth == 0 or board[i - boardWidth - 1] == opponent)
 bottomRight = (i // boardWidth == boardHeight - 1 or i % boardWidth == boardWidth - 1 or board[
     i + boardWidth + 1] == opponent)
 topRight = (i % boardWidth == boardHeight - 1 or i // boardWidth == 0 or board[i - boardWidth + 1] == opponent)
 bottomLeft = (i // boardWidth == boardHeight - 1 or i % boardWidth == 0 or board[i + boardWidth - 1] == opponent)
 return (left and right and top and bottom and topLeft and bottomRight and topRight and bottomLeft)

def quickMove(board, token, override, tournament):
 locs = findMoves(board, token)
 for loc in locs:
     board = board[:loc] + '*' + board[loc + 1:]
 #display(board)
 #print('')
 for loc in locs:
     board = board[:loc] + '.' + board[loc + 1:]
 xs = board.count('x')
 os = board.count('o')
 #print(board, str(xs) + '/' + str(os))
 if board.count('.') > LIMIT_AB or override:
     #print('Possible moves for', token + ':', str(locs)[1:-1])
     # initial = -1
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
             if loc in csquares and board[close[loc]] == token:
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
             comp = {p for p in findMoves(tempBoard, opponent) if
                     p not in corners or (p in close and tempBoard[close[p]] == opponent) #or isStable(
                         #makeMove(board, opponent, p), p, opponent)
                    }
             if len(comp) < minMoves:
                 bestPos = loc
                 minMoves = len(comp)
         if bestPos == -1 and locs:
             bestPos = random.choice([*locs])
     if not tournament:
         print('My preferred move is', bestPos)
     return bestPos
 else:
     #print('Possible moves for', token + ':', str(locs)[1:-1])
     maxScore, sequence = alphabeta(board, token, -64, 64, [])
     maxScore *= -1
     if not tournament:
         print('My move is', sequence[0])
         print('Score:', maxScore, ', Move List:', sequence[::-1])
     return sequence

def playGame(board, token):
 script = []
 while board.count('.') > 0 and (len(findMoves(board, 'x')) > 0 or len(findMoves(board, 'o')) > 0):
     if token == 'x':
         move = quickMove(board, 'x', False, True)
         if type(move) != list:
             script.append(move)
             if move > -1:
                 board = makeMove(board, 'x', move)
         else:
             if move:
                 script.append(move[0])
                 if move[0] > -1:
                     board = makeMove(board, 'x', move[0])
             else:
                 script.append(-1)
         ePsbl = [*findMoves(board, 'o')]
         if ePsbl:
             choice = random.choice(ePsbl)
             board = makeMove(board, 'o', choice)
             script.append(choice)
         else:
             script.append(-1)
     else:
         ePsbl = [*findMoves(board, 'x')]
         if ePsbl:
             choice = random.choice(ePsbl)
             script.append(choice)
             board = makeMove(board, 'x', choice)
         else:
             script.append(-1)
         move = quickMove(board, 'o', False, True)
         if type(move) != list:
             script.append(move)
             if move > -1:
                 board = makeMove(board, 'o', move)
         else:
             if move:
                 script.append(move[0])
                 if move[0] > -1:
                     board = makeMove(board, 'o', move[0])
             else:
                 script.append(-1)
 conv = ''
 for mv in script:
     if mv >= 0 and mv < 10:
         conv += '_'
         conv += str(mv)
     else:
         conv += str(mv)
 while conv[-2:] == '-1':
    conv = conv[:-2]
 return (board, conv)

def quickMove2(board, token, tournament):
# locs = findMoves(board, token)
# for loc in locs:
# board = board[:loc] + '*' + board[loc + 1:]
# display(board)
# print('')
# for loc in locs:
# board = board[:loc] + '.' + board[loc + 1:]
# xs = board.count('x')
# os = board.count('o')
# print(board, str(xs) + '/' + str(os))
# print('Possible moves for', token + ':', str(locs)[1:-1])
# initial = -1
# print('Possible moves for', token + ':', str(locs)[1:-1])
 startTime = time.time()
 maxScore, sequence = midgameAB(board, token, -64, 64, [], 0, board, token, startTime)
 oSeq = sequence[:]
 maxScore *= -1
 if not tournament:
     print('My move is', sequence[0])
     print('Score:', maxScore, ', Move List:', sequence[::-1])
 return oSeq

alphaBetaBefore = {}
midgameBefore = {}

'''
def heuristic(board, token):
   opponent = 'xo'.replace(token, '')
   psbls = findMoves(board, token)
   ePsbls = findMoves(board, opponent)
   difference = 1 * (board.count(token) - board.count(opponent)) / (board.count(token) + board.count(opponent))
   actualMobility = 0
   if len(psbls) + len(ePsbls) > 0:
       actualMobility = 100 * (len(psbls) - len(ePsbls)) / (len(psbls) + len(ePsbls))
   psblMobilityMe, psblMobilityEnemy = 0, 0
   myFrontiers, theirFrontiers = 0, 0
   for i, tok in enumerate(board):
       if tok == '.':
           validMe, validEnemy = False, False
           for nbr in neighbors[i]:
               if board[nbr] == token:
                   validMe = True
               if board[nbr] == opponent:
                   validEnemy = True
           if validMe:
               psblMobilityMe += 1
           if validEnemy:
               psblMobilityEnemy += 1
       else:
           vMe, vEnemy = False, False
           for nbr in neighbors[i]:
               if board[nbr] == '.':
                   if tok == token:
                       vMe = True
                   else:
                       vEnemy = True
           if vMe:
               myFrontiers += 1
           if vEnemy:
               theirFrontiers += 1
   #possibleMobility = 0
   #if psblMobilityMe + psblMobilityEnemy > 0:
       #possibleMobility = 75 * (psblMobilityMe - psblMobilityEnemy) / (psblMobilityMe + psblMobilityEnemy)
   frontierEval = 0
   if myFrontiers + theirFrontiers > 0:
       frontierEval = -50 * (myFrontiers - theirFrontiers) / (myFrontiers + theirFrontiers)
   me, them = 0, 0
   for corner in corners:
       if board[corner] == token:
           me += 1
       if board[corner] == opponent:
           them += 1
   cornerEval = 0
   if me > 0 or them > 0:
       cornerEval = 1000 * (me - them) / (me + them)
   mcEval, tcEval = 0, 0
   for loc in close:
       if board[loc] == token:
           if board[close[loc]] == opponent:
               tcEval += 1
           if board[close[loc]] == token:
               mcEval += 1
           #if board[close[loc]] == '.':
               #tcEval += 0.5
       if board[loc] == opponent:
           if board[close[loc]] == token:
               tcEval += 1
           if board[close[loc]] == opponent:
               mcEval += 1
           #if board[close[loc]] == '.':
               #tcEval += 0.5
   awkwardEval = 0
   if tcEval + mcEval > 0:
       awkwardEval = 250 * (mcEval - tcEval) / (mcEval + tcEval)
   return -1*(difference + actualMobility + frontierEval + cornerEval + awkwardEval)
'''
weights = [
    200, -100, 100, 50, 50, 100, -100, 200,
    -100, -200, -50, -50, -50, -50, -200, -100,
    100, -50, 100, 0, 0, 100, -50, 100,
    50, -50, 0, 0, 0, 0, -50, 50,
    50, -50, 0, 0, 0, 0, -50, 50,
    100, -50, 100, 0, 0, 100, -50, 100,
    -100, -200, -50, -50, -50, -50, -200, -100,
    200, -100, 100, 50, 50, 100, -100, 200]

def heuristic(board, token):
    '''
    staticWeights = weights[:]
    for corner in corners:
        if board[corner] == '.':
            for loc in revClose[corner]:
                staticWeights[loc] = 0
        elif board[corner] == token:
            for loc in revClose[corner]:
                staticWeights[loc] *= -1
    '''
    opponent = 'xo'.replace(token, '')
    myMoves = findMoves(board, token)
    oppMoves = findMoves(board, opponent)
    mobility = 0
    if len(myMoves) > 0 or len(oppMoves) > 0:
        mobility = (len(myMoves) - len(oppMoves)) / (len(myMoves) + len(oppMoves))
    pMobM, pMobE = 0, 0
    mS, eS = 0, 0
    wImpact = 0
    for i in range(len(board)):
        if board[i] == token:
            #wImpact += staticWeights[i]
            if isStable(board, i, token):
                mS += 1
        elif board[i] == opponent:
            #wImpact -= staticWeights[i]
            if isStable(board, i, opponent):
                eS += 1
        vMe, vE = False, False
        for nbr in neighbors[i]:
            if board[nbr] == '.':
                if board[i] == token:
                    vE = True
                    break
                if board[i] == opponent:
                    vMe = True
                    break
        if vMe:
            pMobM += 1
        if vE:
            pMobE += 1
    possibleMobility = 0
    if pMobM > 0 or pMobE > 0:
        possibleMobility = (pMobM - pMobE) / (pMobM + pMobE)
    mC, eC = 0, 0
    for corner in corners:
        if board[corner] == token:
            mC += 1
        if board[corner] == opponent:
            eC += 1
    cornerEval = 0
    if mC > 0 or eC > 0:
        cornerEval = (mC - eC) / (mC + eC)
    stableEval = 0
    if mS > 0 or eS > 0:
        stableEval = (mS - eS) / (mS + eS)
    xs, os = board.count('x'), board.count('o')
    squaresRemaining = 64 - xs - os
    if squaresRemaining%2 == 0:
        if token == 'x':
            parity = 1
        else:
            parity = -1
    else:
        if token == 'x':
            parity = -1
        else:
            parity = 1
    discDiff = (board.count(token) - board.count(opponent)) / (xs + os)
    if xs + os < 15:
        return -1*(40*mobility+10000*stableEval)
    else:
        return -1*(40*mobility+10*possibleMobility+5*parity+10000*stableEval)

def negamax(board, token, mvs):
  opponent = 'xo'.replace(token, '')
  if '.' not in board:
      return (-1*(board.count(token) - board.count(opponent)), mvs)
  possibilities = findMoves(board, token)
  if len(possibilities) == 0:
      other = findMoves(board, opponent)
      if len(other) == 0:
          return (-1*(board.count(token) - board.count(opponent)), mvs)
      else:
          temp = mvs[:]
          temp.append(-1)
          tup = negamax(board, opponent, temp)
          tup = (tup[0] * -1, tup[1])
          return tup
  maxScore, mvsSeq = -100, []
  for move in possibilities:
      newBoard = makeMove(board, token, move)
      temp = mvs[:]
      temp.append(move)
      score, seq = negamax(newBoard, opponent, temp)
      if maxScore < score:
          maxScore = score
          mvsSeq = seq
  return (-1 * maxScore, mvsSeq)

def alphabeta(board, token, alpha, beta, mvs):
 global alphaBetaBefore
 key = (board, token, alpha, beta)
 if key in alphaBetaBefore:
     tup = alphaBetaBefore[key]
     temp = mvs[:]
     temp.extend(tup[1])
     return (tup[0], temp)
 opponent = 'xo'.replace(token, '')
 if '.' not in board:
     return (board.count(opponent) - board.count(token), mvs)
 possibilities = findMoves(board, token)
 if len(possibilities) == 0:
     other = findMoves(board, opponent)
     if len(other) == 0:
         return (board.count(opponent) - board.count(token), mvs)
     else:
         temp = mvs[:]
         temp.append(-1)
         tup = alphabeta(board, opponent, -beta, -alpha, temp)
         tup = (tup[0] * -1, tup[1])
         return tup
 reorder = []
 for loc in possibilities:
     if loc in corners:
         reorder.append(loc)
 for loc in possibilities:
     if loc not in reorder and loc in close and board[close[loc]] == token:
         reorder.append(loc)
 storage = {}
 for loc in possibilities:
     tempBoard = makeMove(board, token, loc)
     storage[loc] = tempBoard
     if loc not in reorder and isStable(tempBoard, loc, token):
         reorder.append(loc)
 cop = possibilities.copy()
 for loc in possibilities:
     if loc in corners or loc in close or loc in reorder:
         cop.remove(loc)
 reaver = {}
 for loc in cop:
     tempBoard = makeMove(board, token, loc)
     comp = {p for p in findMoves(tempBoard, opponent) if
             (p not in corners or p in close and tempBoard[close[p]] == opponent) #or isStable(
                 #makeMove(board, 'xo'.replace(token, ''), p), p, token)
            }
     if len(comp) in reaver:
         reaver[len(comp)].append(loc)
     else:
         reaver[len(comp)] = []
         reaver[len(comp)].append(loc)
 for k in sorted([*reaver.keys()]):
     reorder.extend(reaver[k])
 for loc in possibilities:
     if loc not in reorder:
         reorder.append(loc)
 maxScore, mvsSeq = -65, []
 for move in reorder:
     newBoard = makeMove(board, token, move)
     temp = mvs[:]
     temp.append(move)
     score, seq = alphabeta(newBoard, opponent, -beta, -alpha, temp)
     if maxScore < score:
         maxScore = score
         mvsSeq = seq
     if maxScore > alpha:
         alpha = maxScore
     if alpha >= beta:
         break
 alphaBetaBefore[key] = (-1 * maxScore, mvsSeq[len(mvs):])
 return (-1 * maxScore, mvsSeq)

def midgameAB(board, token, alpha, beta, mvs, depth, oBoard, oToken, startTime):
 global midgameBefore, DEPTH_AB
 '''
 if time.time() - startTime >= 0.45 or depth == DEPTH_AB:
     move = quickMove(oBoard, oToken, True, True)
     board = makeMove(oBoard, oToken, move)
     return (board.count(oToken) - board.count('xo'.replace(oToken, '')), [move])
 '''
 key = (board, token, alpha, beta)
 if key in midgameBefore:
     tup = midgameBefore[key]
     temp = mvs[:]
     temp.extend(tup[1])
     return (tup[0], temp)
 opponent = 'xo'.replace(token, '')
 if depth == DEPTH_AB or '.' not in board:
     return (heuristic(board, token), mvs)
 possibilities = findMoves(board, token)
 if len(possibilities) == 0:
     other = findMoves(board, opponent)
     if len(other) == 0:
         return (heuristic(board, token), mvs)
     else:
         temp = mvs[:]
         temp.append(-1)
         tup = midgameAB(board, opponent, -beta, -alpha, temp, depth+1, oBoard, oToken, startTime)
         tup = (tup[0] * -1, tup[1])
         return tup
 reorder = []
 for loc in possibilities:
     if loc in corners:
         reorder.append(loc)
 for loc in possibilities:
     if loc not in reorder and loc in close and board[close[loc]] == token:
         reorder.append(loc)
 cop = possibilities.copy()
 for loc in possibilities:
     if loc in corners or loc in close or loc in reorder:
         cop.remove(loc)
 reaver = {}
 for loc in cop:
     tempBoard = makeMove(board, token, loc)
     comp = {p for p in findMoves(tempBoard, opponent) if
             (p not in corners or p in close and tempBoard[close[p]] == opponent) #or isStable(
                 #makeMove(board, 'xo'.replace(token, ''), p), p, token)
            }
     if len(comp) in reaver:
         reaver[len(comp)].append(loc)
     else:
         reaver[len(comp)] = []
         reaver[len(comp)].append(loc)
 for k in sorted([*reaver.keys()]):
     reorder.extend(reaver[k])
 for loc in possibilities:
     if loc not in reorder:
         reorder.append(loc)
 '''
 reaver = {}
 for move in possibilities:
     numPsbls = len(findMoves(makeMove(board, token, move), opponent))
     if numPsbls in reaver:
         reaver[numPsbls].append(move)
     else:
         reaver[numPsbls] = [move]
 for k in sorted([*reaver.keys()]):
     reorder.extend(reaver[k])
 '''
 maxScore, mvsSeq = -1*float('inf'), []
 for move in reorder:
     newBoard = makeMove(board, token, move)
     temp = mvs[:]
     temp.append(move)
     score, seq = midgameAB(newBoard, opponent, -beta, -alpha, temp, depth+1, board, token, startTime)
     if maxScore < score:
         maxScore = score
         mvsSeq = seq
     if maxScore > alpha:
         alpha = maxScore
     if alpha >= beta:
         break
 #midgameBefore[key] = (-1 * maxScore, mvsSeq[len(mvs):])
 return (-1 * maxScore, mvsSeq)

def playGame2(board, token):
 script = []
 while board.count('.') > 0 and (len(findMoves(board, 'x')) > 0 or len(findMoves(board, 'o')) > 0):
     if token == 'x':
         if board.count('.') > LIMIT_AB:
            move = quickMove2(board, 'x', True)
         else:
            move = quickMove(board, 'x', False, True)
         if type(move) != list:
             script.append(move)
             if move > -1:
                 board = makeMove(board, 'x', move)
         else:
             if move:
                 script.append(move[0])
                 if move[0] > -1:
                     board = makeMove(board, 'x', move[0])
             else:
                 script.append(-1)
         #ePsbl = [*findMoves(board, 'o')]
         ePsbl = quickMove(board, 'o', False, True)
         #if ePsbl:
         #if ePsbl > -1:
             #choice = random.choice(ePsbl)
             #board = makeMove(board, 'o', choice)
             #script.append(choice)
             #board = makeMove(board, 'o', ePsbl)
             #script.append(ePsbl)
         #else:
             #script.append(-1)
         if type(ePsbl) != list:
             script.append(ePsbl)
             if ePsbl > -1:
                 board = makeMove(board, 'o', ePsbl)
         else:
             if ePsbl:
                 script.append(ePsbl[0])
                 if ePsbl[0] > -1:
                     board = makeMove(board, 'o', ePsbl[0])
             else:
                 script.append(-1)
     else:
         #ePsbl = [*findMoves(board, 'x')]
         ePsbl = quickMove(board, 'x', False, True)
         #if ePsbl:
         #if ePsbl > -1:
             #choice = random.choice(ePsbl)
             #script.append(choice)
             #board = makeMove(board, 'x', choice)
             #script.append(ePsbl)
             #board = makeMove(board, 'x', ePsbl)
         #else:
             #script.append(-1)
         if type(ePsbl) != list:
             script.append(ePsbl)
             if ePsbl > -1:
                 board = makeMove(board, 'x', ePsbl)
         else:
             if ePsbl:
                 script.append(ePsbl[0])
                 if ePsbl[0] > -1:
                     board = makeMove(board, 'x', ePsbl[0])
             else:
                 script.append(-1)
         if board.count('.') > LIMIT_AB:
            move = quickMove2(board, 'o', True)
         else:
            move = quickMove(board, 'o', False, True)
         if type(move) != list:
             script.append(move)
             if move > -1:
                 board = makeMove(board, 'o', move)
         else:
             if move:
                 script.append(move[0])
                 if move[0] > -1:
                     board = makeMove(board, 'o', move[0])
             else:
                 script.append(-1)
 conv = ''
 for mv in script:
     if mv >= 0 and mv < 10:
         conv += '_'
         conv += str(mv)
     else:
         conv += str(mv)
 while conv[-2:] == '-1':
    conv = conv[:-2]
 return (board, conv)

class Strategy:
    # implement all the required methods on your own
    logging = True
    def best_strategy(self, board, player, best_move, running, time_limit):
        time.sleep(1)
        if running.value:
            DEPTH_AB = 5
            startTime = time.time()
            best_move.value = quickMove(board, player, True, True)
            if board.count('.') <= LIMIT_AB:
                mvs = quickMove(board, player, False, True)
                best_move.value = mvs[0]
            else:
                while time.time() - startTime < time_limit / 2:
                    mvs = quickMove2(board, player, True)
                    best_move.value = mvs[0]
                    DEPTH_AB += 1

def main():
 while '' in args:
     args.remove(args.index(''))
 while ' ' in args:
     args.remove(args.index(' '))
 if len(args) == 0:
     startTime = time.time()
     myTokens, totalTokens = 0, 0
     simulation = {}
     for iter in range(100):
         token = 'x'
         enemy = 'o'
         if iter%2 == 1:
             token = 'o'
             enemy = 'x'
         board = '...........................ox......xo...........................'
         after, moveScript = playGame2(board, token)
         myTokens += after.count(token)
         totalTokens = totalTokens + after.count('x') + after.count('o')
         if iter%10 == 0:
             print()
         diff = after.count(token) - after.count(enemy)
         simulation[moveScript] = (diff, iter, token)
         print(diff, end=' ')
         DEPTH_AB = 4
     print()
     print(f'My tokens: {myTokens}; Total tokens: {totalTokens}')
     percent = str(myTokens * 100 / totalTokens)[:4]
     print(f'Score: {percent}%')
     print('NM/AB LIMIT:', LIMIT_AB)
     scores = [v[0] for v in simulation.values()]
     absMin = min(scores)
     scores.remove(absMin)
     min2 = min(scores)
     moveScript1, moveScript2 = '', ''
     g1, g2 = -1, -1
     g1t, g2t = 'x', 'x'
     for k in simulation:
         v = simulation[k]
         if len(moveScript1) > 0 and len(moveScript2) > 0:
             break
         if v[0] == absMin:
             moveScript1 = k
             g1 = v[1]
             g1t = v[2]
         if v[0] == min2:
             moveScript2 = k
             g2 = v[1]
             g2t = v[2]
     print(f'Game {g1} as {g1t} => {absMin}:')
     print(moveScript1)
     print(f'Game {g2} as {g2t} => {min2}:')
     print(moveScript2)
     print('Elapsed Time:', str(time.time()-startTime)[:5]+'s')
     moves = []
     board = '...........................ox......xo...........................'
     token = 'x'
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
                 if type(moves) == list and len(moves[0]) > 2:
                     moves = moves[0]
                     temp = []
                     for i in range(0, len(moves), 2):
                         move = moves[i:i + 2]
                         if '_' in move:
                             temp.append(move[1])
                         else:
                             temp.append(moves[i:i + 2])
                     moves = temp
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
     if type(moves) == list and len(moves[0]) > 2:
         moves = moves[0]
         temp = []
         for i in range(0, len(moves), 2):
             move = moves[i:i+2]
             if '_' in move:
                 temp.append(move[1])
             else:
                 temp.append(moves[i:i+2])
         moves = temp
 if len(args) > 0:
     snapshot(board, token)
 moves = filterMoves(moves)
 if moves:
     if token == 'x':
         init = 'xo'
     else:
         init = 'ox'
     for i, move in enumerate(moves):
         board = makeMove(board, init[i%2], move)
         token = init[i%2]
         print()
         print(token, 'plays to', move)
         print()
         snapshot(board, token)
     if (board.count('x') + board.count('o')) % 2 == 1:
         token = 'o'
     else:
         token = 'x'
 if len(findMoves(board, token)) == 0:
     token = 'xo'[token == 'x']
 if len(args) > 0:
     quickMove(board, token, True, False)
 if board.count('.') > LIMIT_AB:
     quickMove2(board, token, False)
 else:
     quickMove(board, token, False, False)

if __name__ == '__main__':
 main()

# Vishal Kotha, 4, 2023