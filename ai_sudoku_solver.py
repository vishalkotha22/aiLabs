import sys, math, time
global start, fixing, hardcode, count, sideLength, width, height, symbols, constraintSets, rows, cols, subblocks, count

class SudokuPuzzleReader:
    def __init__(self, filename):
        self.file = filename

    def read_puzzles(self):
        pzls = open(self.file, 'r').read().splitlines()
        solver = SudokuSolver(pzls)
        solver.solvePuzzles()

class SudokuBoard:
    def __init__(self, ind):
        self.loc = ind

    # given a number from 0 to the length of the puzzle - 1, return the row it's in
    def findRow(self):
        startRow = self.loc // sideLength * sideLength
        temp = set()
        for r in range(startRow, startRow + sideLength):
            temp.add(r)
        return temp

    # given a number from 0 to the length of the puzzle - 1, return the column it's in
    def findCol(self):
        col = self.loc % sideLength
        temp = set()
        for r in range(sideLength):
            temp.add(r * sideLength + col)
        return temp

    # given a number from 0 to the length of the puzzle - 1, return the subblock in
    def findSubBlock(self):
        # calculate the lower and upper bounds for both x and y of the subblock
        diff = self.loc % sideLength
        subBlockLowerX = diff // width * width
        subBlockHigherX = subBlockLowerX + width
        row = self.loc // sideLength
        subBlockLowerY = row // height * height
        subBlockHigherY = subBlockLowerY + height

        temp = set()
        for r in range(subBlockLowerY, subBlockHigherY):
            for c in range(subBlockLowerX, subBlockHigherX):
                temp.add(r * sideLength + c)
        return temp

    # given an index from 0 to the length of the board minus one, it returns the indices of the constraint set.
    # the constraint set is all the indices in the row, column, and the sub block.
    def findNeighbors(self):
        startRow = self.loc // sideLength * sideLength
        temp = {r for r in range(startRow, startRow + sideLength)}
        col = self.loc % sideLength
        for r in range(sideLength):
            temp.add(r * sideLength + col)
        diff = self.loc % sideLength
        subBlockLowerX = diff // width * width
        subBlockHigherX = subBlockLowerX + width
        row = self.loc // sideLength
        subBlockLowerY = row // height * height
        subBlockHigherY = subBlockLowerY + height
        for r in range(subBlockLowerY, subBlockHigherY):
            for c in range(subBlockLowerX, subBlockHigherX):
                temp.add(r * sideLength + c)
        return [*temp]

class SudokuSolver:
    def __init__(self, pzls):
        self.puzzles = pzls

    def solvePuzzles(self):
        global sideLength, rows, cols, subblocks, width, height, symbols, constraintSets
        pzls = self.puzzles
        startTime = time.time()
        pzl = pzls[0]
        sideLength = math.isqrt(len(pzl))
        width = [i for i in range(1, math.isqrt(len(pzl)) + 1) if len(pzl) % i == 0][-1]
        height = len(pzl) // width
        symbols = []
        for n in range(1, sideLength + 1):
            symbols.append(str(n))
        constraintSets = [0] * len(pzl)
        board = SudokuBoard(0)
        for i in range(len(constraintSets)):
            board = SudokuBoard(i)
            constraintSets[i] = board.findNeighbors()
        # calculate the indices for each row, column, and sub block
        rows = [0] * len(pzl)
        cols = [0] * len(pzl)
        subblocks = [0] * len(pzl)
        for i in range(len(pzl)):
            board = SudokuBoard(i)
            rows[i] = board.findRow()
            cols[i] = board.findCol()
            subblocks[i] = board.findSubBlock()
        count = 0
        for index, pzl in enumerate(pzls):
            start = time.time()
            pzlCleaner = PuzzleCleaner(pzl)
            cleanedPzl, helped = pzlCleaner.fillInHiddenSingles()
            pzlSolver = PuzzleSolver(cleanedPzl)
            ans = pzlSolver.solvePuzzle()
            # print things like the solved board and the time it took to solve it
            print(' ' * len(str(index + 1)), ans, str(time.time() - start)[:4])

class PuzzleCleaner:
    def __init__(self, pzl):
        self.puzzle = pzl

    def fillInHiddenSingles(self):
        helped = 0
        pzl = self.puzzle
        for val in range(len(pzl)):
            sym, pos = self.isHiddenSingle(val)
            if pos > -1:
                pzl = pzl[:pos] + sym + pzl[pos + 1:]
                helped += 1
        return pzl, helped

    # return the symbol to put if the location is a hidden single; otherwuse, return -1
    def isHiddenSingle(self, loc):
        pzl = self.puzzle

        # calculate the row, column, aud subblock variables
        row = loc // sideLength
        diff = loc % sideLength
        subBlockLowerX = diff // width * width
        subBlockLowerY = row // height * height

        # get the symbols and locations of the other two columns in the stack
        if diff % width == 0:
            col1 = {pzl[i] for i in cols[loc + 1]}
            col1i = {*cols[loc + 1]}
            col2 = {pzl[i] for i in cols[loc + 2]}
            col2i = {*cols[loc + 2]}
        elif diff % width == 1:
            col1 = {pzl[i] for i in cols[loc - 1]}
            col1i = {*cols[loc - 1]}
            col2 = {pzl[i] for i in cols[loc + 1]}
            col2i = {*cols[loc + 1]}
        else:
            col1 = {pzl[i] for i in cols[loc - 2]}
            col1i = {*cols[loc - 2]}
            col2 = {pzl[i] for i in cols[loc - 1]}
            col2i = {*cols[loc - 1]}

        # get the symbols and locations of the other two rows in the band
        if row % height == 0:
            row1 = {pzl[i] for i in rows[loc + sideLength]}
            row1i = {*rows[loc + sideLength]}
            row2 = {pzl[i] for i in rows[loc + 2 * sideLength]}
            row2i = {*rows[loc + 2 * sideLength]}
        elif row % height == 1:
            row1 = {pzl[i] for i in rows[loc - sideLength]}
            row1i = {*rows[loc - sideLength]}
            row2 = {pzl[i] for i in rows[loc + sideLength]}
            row2i = {*rows[loc + sideLength]}
        else:
            row1 = {pzl[i] for i in rows[loc - sideLength]}
            row1i = {*rows[loc - sideLength]}
            row2 = {pzl[i] for i in rows[loc - 2 * sideLength]}
            row2i = {*rows[loc - 2 * sideLength]}

        # remove all the row1 values if the symbol is already in row1 (repeat for row2, col1, and col2). this way, we can
        # detect hidden singles.
        sub = {i for i in subblocks[loc] if pzl[i] == '.'}
        for sym in ({*symbols} - {pzl[i] for i in constraintSets[loc] if pzl[i] in symbols}):
            subblock = sub.copy()
            if sym in row1:
                subblock = subblock - row1i
            if sym in row2:
                subblock = subblock - row2i
            if sym in col1:
                subblock = subblock - col1i
            if sym in col2:
                subblock = subblock - col2i
            if len(subblock) == 1:
                return (sym, subblock.pop())

        # no hidden singles were found, so return -1 and -1
        return -1, -1

class PuzzleSolver:
    def __init__(self, puzzle):
        self.pzl = puzzle

    # return a dictionary that has the index as the key and a tuple as the value. the tuple stores the following numbers:
    # (the number of possible symbols, the set of possible symbols, and the index). this is used to pick dots optimally.
    def findBest(self, pzl):
        locs = [i for i, ch in enumerate(pzl) if ch == '.']
        ret = {}
        for loc in locs:
            ret[loc] = (len((s := ({*symbols} - {pzl[i] for i in constraintSets[loc] if pzl[i] in symbols}))), s, loc)
        return ret

    # an improved version of the find best method. if there's a hidden single (there's only one possibility for a square by the
    # rules of sudoku even though there's technically more than one symbol it could be). it finds the best dot to try and fill
    # in values for (it uses recursive backtracking).
    def findBest2(self, pzl, loc):
        # if there's a hidden single, there's only one possibility for some square by the rules of sudoku. just fill it in and
        # continue with the recursive backtracking.
        one, two = isHiddenSingle(pzl, loc)
        if two > -1:
            return (1, one, {two})

        # create a dictionary of all possible locations for each symbol
        helper = {}
        for i in constraintSets[loc]:
            for sym in test(pzl, i):
                if pzl[i] == '.':
                    if sym in helper:
                        helper[sym].add(i)
                    else:
                        helper[sym] = set()
                        helper[sym].add(i)

        # return the symbol with the fewest possible locations
        minV, minS, minP = 100, 1, {}
        for sym in helper:
            v = helper[sym]
            if len(v) < minV:
                minV = len(v)
                minS = sym
                minP = v
        return (minV, minS, minP)

    # a brute force method to recursively backtrack and solve a sudoku puzzle.
    def bruteForce(self, pzl, possible):
        # count the number of times a number is tried
        # if there's no possibilities, return it
        if len(possible) == 0: return pzl

        # choose the dot with the fewest possibilities (significant speed up from choosing dots randomly)
        minVal, minSet, minPos = 100, {}, -1
        for key in possible:
            v, s, k = possible[key]
            if len(s) < minVal:
                minVal = len(s)
                minSet = s
                minPos = k
            if len(s) == 1:  # if there's only one possibility, that's the minimum so we don't need to keep exploring
                break

        # find the constraint set and remove the location from the set of dots that still need to be filled. we only look at the
        # constraint set (row, column, sub block), since those are the only indices that will be affected by the placement of a
        # symbol at some location.
        constraintSet = constraintSets[minPos]
        del possible[minPos]
        subset = {k for k in possible if possible[k][2] in constraintSet}

        # try all the possible numbers at the location. we update the possibilities set by removing the symbol as a possibility
        # for any other index in the constraint set. however, if it doesn't result in a solved board, we incrementally update the
        # possibilities for each index in the constraint set. this means that if the symbol was removed as a possibility for any
        # other index, since it failed, we read it as a possibility for all the othre indices. doing this incremental repair is
        # much faster than making a copy of the index to possible symbols dictionary each time.
        for num in minSet:
            subPzl = ''.join([pzl[:minPos], num, pzl[minPos + 1:]])  # add the symbol
            tofix = []
            for k in subset:  # for everything in the constraint set, if it has num as a possibility, remove it
                tv, ts, tk = possible[k]
                if num in ts:
                    possible[k] = (len(ts) - 1, ts - {num}, tk)
                    tofix.append((k, tv, ts, tk))  # store the tuple in tofix if we have to repair it afterwards
            bf = self.bruteForce(subPzl, possible)
            if bf:
                return bf  # if it resulted in a solved board, return it
            for tup in tofix:  # it failed so repair the set of possibilities
                k, tv, ts, tk = tup
                possible[k] = (tv, ts, tk)

        possible[minPos] = (minVal, minSet, minPos)  # this position failed so readd to the set of possibilities
        return ''

    def solvePuzzle(self):
        return self.bruteForce(self.pzl, self.findBest(self.pzl))

puzzleSolver = SudokuPuzzleReader('puzzles.txt')
puzzleSolver.read_puzzles()