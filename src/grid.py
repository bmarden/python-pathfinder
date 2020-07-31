import sys
import pygame
import config

from pygame.locals import *

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
fill = [200, 200, 200]


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def initGrid(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(white)

        self.drawGrid()

    def drawGrid(self):
        """ Initializes grid defined by width and height """
        x = 0
        y = 0

        # Fit max amount of cells into user defined grid dimensions
        w = self.width // 20

        for l in range(w):
            pygame.draw.aaline(self.screen, black, (0, y), (self.width, y))
            pygame.draw.aaline(self.screen, black, (x, 0), (x, self.height))
            x = x + 20
            y = y + 20

    def fillSquare(self, row, col, color):
        # Calculate actual x and y values
        row_actual = row * 20
        col_actual = col * 20
        rec = pygame.Rect(col_actual, row_actual, 19, 19)
        pygame.draw.rect(self.screen, color, rec)
        pygame.display.update(rec)

    def getCell(self, x, y):
        x = x - (x % 20)
        y = y - (y % 20)
        coord = (x, y)
        return coord
