# -*- coding: UTF-8 -*-

import random

class Board():
    """
    A 2048 board
    """

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    GOAL = 2048
    SIZE = 4

    def __init__(self):
        self.cells = [[0]*Board.SIZE for i in xrange(Board.SIZE)]
        self.addTile(2)
        self.addTile(2)
        self.__won = False

    def won(self):
        return self.__won

    def canMove(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in xrange(0, Board.SIZE-1):
            for x in xrange(0, Board.SIZE-1):
                c = self.getCell(x, y)
                if c == self.getCell(x+1, y) or c == self.getCell(x, y+1):
                    return True

        return False

    def filled(self):
        return len(self.getEmptyCells()) == 0

    def addTile(self, value=None, choices=[2, 4]):
        """
        add a random tile in an empty cell
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCell(self, x, y):
        return self.cells[y][x]

    def getCellStr(self, x, y):
        c = self.getCell(x, y)
        if c == 0:
            return '   .'
        return '%4d' % c

    def setCell(self, x, y, v):
        self.cells[y][x] = v

    def getLine(self, y):
        return [self.getCell(i, y) for i in xrange(0, Board.SIZE)]

    def getCol(self, x):
        return [self.getCell(x, i) for i in xrange(0, Board.SIZE)]

    def setLine(self, y, l):
        for i in xrange(0, Board.SIZE):
            self.setCell(i, y, l[i])

    def setCol(self, x, l):
        for i in xrange(0, Board.SIZE):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """
        return [x, y] for each cell
        """
        return [[x, y] for x in xrange(Board.SIZE)
                           for y in xrange(Board.SIZE) if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction
        """
        if (d == Board.LEFT or d == Board.UP):
            rg = xrange(0, Board.SIZE-1)
        else:
            rg = xrange(Board.SIZE-2, -1, -1)

        for i in rg:
            if line[i] == line[i+1]:
                v = line[i]*2
                if v == Board.GOAL:
                    self.won = True

                line[i] = v
                line[i+1] = 0

        return line

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (Board.SIZE - len(nl))
        return [0] * (Board.SIZE - len(nl)) + nl

    def move(self, d, add_tile=True):
        if d == Board.LEFT or d == Board.RIGHT:
            chg, get = self.setLine, self.getLine
        else:
            chg, get = self.setCol, self.getCol

        for i in xrange(0, Board.SIZE):
            line = self.__moveLineOrCol(get(i), d)
            collapsed = self.__collapseLineOrCol(line, d)
            chg(i, self.__moveLineOrCol(collapsed, d))

        if add_tile:
            self.addTile()

    def __str__(self):
        s = "\n".join([' '.join(
                    [self.getCellStr(x, y) for x in xrange(Board.SIZE)])
                        for y in xrange(Board.SIZE)])
        return s