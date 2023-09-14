import pygame
import random
from settings import *

#0 -> begin, 1 -> left, 2 -> right, 3 -> bottom, 4 -> goBackWithoutDraw
shapes = [
    [[0, 2, 2, 2], [0, 3, 3, 3]], 
    [[0, 2, 3, 1]],
    [[0, 3, 1, 4, 3], [0, 3, 1, 4, 2], [0, 3, 2, 4, 3], [0, 2, 3, 4, 2]],
    [[0, 3, 3, 1], [0, 3, 2, 2], [0, 2, 4, 3, 3], [0, 2, 2, 3]],
    [[0, 3, 3, 2], [0, 1, 1, 3], [0, 2, 3, 3], [0, 3, 1, 1]],
    [[0, 2, 3, 2], [0, 3, 2, 3], [0, 1, 3, 1], [0, 3, 1, 3]]
]

blockSize = 40

class Shape:
    def __init__(self, screen):
        self.screen = screen
        self.type = random.randint(0, len(shapes) - 1)
        self.rotation = random.randint(0, len(shapes[self.type]) - 1)
        self.color_pos = random.randint(1, len(BLOCK_COLOURS) - 1)
        self.color = BLOCK_COLOURS[self.color_pos]
        self.positionInTheGrid = [] # list of position (i, j) of cells occupied by the block
        self.shape = shapes[self.type][self.rotation]
        # print(self.type, self.rotation)
        # print(shapes[self.type][self.rotation])

    def draw(self, x, y):
        self.positionInTheGrid.clear()
        screen = self.screen
        color = self.color
        self.shape = shapes[self.type][self.rotation]
        
        # draw first block of the shape
        rect = pygame.Rect(x, y, blockSize, blockSize)
        pygame.draw.rect(screen, color, rect)

        self.positionInTheGrid.append(((y - 25) // 40, (x - 50) // 40))
        
        # record the position in the screen (in px)
        sx = x        # minimum x of the shape
        dx = x + blockSize   # maximum x of the shape
        curY = y      # maximum y of the shape

        # store the previous position in the screen (in px)
        previousSx = 0 
        previousDx = 0
        previousY = 0

        # store the verse of drawing (0 = none, 1 = left, 2 = right)
        verse = 0

        for i in range(1, len(self.shape)):
            # print(i)
            # print(self.shape[i])
            
            if self.shape[i] == 1:
                rect = pygame.Rect(sx - 40, curY, blockSize, blockSize)
                previousSx = sx
                sx -= blockSize
                verse = 1
                self.positionInTheGrid.append((curY // 40, (sx - 50) // 40))
            elif self.shape[i] == 2:
                rect = pygame.Rect(dx, curY, blockSize, blockSize)
                previousDx = dx
                dx += blockSize
                verse = 2
                self.positionInTheGrid.append((curY // 40, (dx - 50 - blockSize) // 40))
            elif self.shape[i] == 3:
                if verse <= 1: 
                    rect = pygame.Rect(sx, curY + blockSize, blockSize, blockSize)
                    self.positionInTheGrid.append(((curY + blockSize) // 40, (sx - 50) // 40))
                elif verse == 2: 
                    rect = pygame.Rect(dx - blockSize, curY + blockSize, blockSize, blockSize)
                    sx += 40
                    self.positionInTheGrid.append(((curY + blockSize) // 40, (dx - blockSize - 50) // 40))
                previousY = curY
                curY += blockSize
            elif self.shape[i] == 4:
                verse = 0
                if self.shape[i - 1] == 1: sx = previousSx
                elif self.shape[i - 1] == 2: dx = previousDx
                elif self.shape[i - 1] == 3: curY = previousY
                continue

            # print(self.positionInTheGrid)
            pygame.draw.rect(screen, color, rect)

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(shapes[self.type]) 
