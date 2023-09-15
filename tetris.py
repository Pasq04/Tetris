import pygame
from pygame.locals import *
from shape import *
from settings import *

pygame.font.init()

# global variables
running = True
clock = pygame.time.Clock()
score = 0
record = 0

# fonts
DEFEAT_FONT = pygame.font.SysFont("Arial", 100)
SCORE_FONT = pygame.font.SysFont("Arial", 40)
RECORD_FONT = pygame.font.SysFont("Arial", 40)

# matrix ROWS x COLUMNS that define the grid
ROWS = 20
COLUMNS = 12
grid_matrix = [] # 0 -> the cell i,j is empty, c -> the cell i,j is occupied by a block of colour BLOCK_COLOURS[c]

# screen definition
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# utils function
def drawGrid():
    for x in range(50, GRID_WIDTH + 50, blockSize):
        for y in range(25, GRID_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, GRID_GREY, rect, 1)

def drawOldBlocks():
    for i in range(ROWS):
        for j in range(COLUMNS):
            #print(grid_matrix)
            if grid_matrix[i][j] != 0:
                rect =  pygame.Rect(50 + j * blocksize, 25 + i * blocksize, blocksize, blocksize)
                # print("drawing coordinates: " + str((rect.x, rect.y)))
                pygame.draw.rect(screen, BLOCK_COLOURS[grid_matrix[i][j]], rect)
        
def draw(block_x, block_y):
    global record
    
    screen.fill(BACKGROUND_BLACK)
    drawGrid()
    drawOldBlocks()
    deleteCompleteRows()

    with open("record.txt") as f:
        record = int(f.readline())

    score_text = SCORE_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    record_text = RECORD_FONT.render("Record: " + str(record), 1, (255, 255, 255))
    screen.blit(score_text, (GRID_WIDTH + 70, 30))
    screen.blit(record_text, ((GRID_WIDTH + 70, 80)))

    # print("coordinates: " + str((block_x, block_y)))
    block.draw(block_x, block_y)

    pygame.display.update()

def initializeMatrix():
    grid_matrix.clear()
    for i in range(ROWS):
        sub = []
        
        for j in range(COLUMNS):
            sub.append(0)
        
        grid_matrix.append(sub)

def get_temp_block_position(shape, x, y):
    grid_position = []

    # draw the first block of shape
    grid_position.append(((y - 25) // 40, (x - 50) // 40))
        
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

    for i in range(1, len(shape)):
            # print(i)
            # print(shape[i])
            
            if shape[i] == 1:
                previousSx = sx
                sx -= blockSize
                verse = 1
                grid_position.append((curY // 40, (sx - 50) // 40))
            elif shape[i] == 2:
                previousDx = dx
                dx += blockSize
                verse = 2
                grid_position.append((curY // 40, (dx - 50 - blockSize) // 40))
            elif shape[i] == 3:
                if verse <= 1: 
                    grid_position.append(((curY + blockSize) // 40, (sx - 50) // 40))
                elif verse == 2: 
                    sx += 40
                    grid_position.append(((curY + blockSize) // 40, (dx - blockSize - 50) // 40))
                previousY = curY
                curY += blockSize
            elif shape[i] == 4:
                verse = 0
                if shape[i - 1] == 1: sx = previousSx
                elif shape[i - 1] == 2: dx = previousDx
                elif shape[i - 1] == 3: curY = previousY
                continue

    return grid_position

def validRotation(block, x, y):
    next_shape = shapes[block.type][(block.rotation + 1) % len(shapes[block.type])]
    tmp_block_position = get_temp_block_position(next_shape, x, y)
    
    for i in range(len(tmp_block_position)):
        if tmp_block_position[i][0] < 0 or tmp_block_position[i][0] >= ROWS - 1 or tmp_block_position[i][1] < 0 or tmp_block_position[i][1] > COLUMNS - 1:
            return False
        if grid_matrix[tmp_block_position[i][0]][tmp_block_position[i][1]] != 0:
            return False
        
    return True

def validMovmentDown():
    for i in range(len(block_positions)):
        if block_positions[i][0] >= ROWS - 1: 
            return False
        if grid_matrix[block_positions[i][0] + 1][block_positions[i][1]] != 0 or block_positions[i][0] + 1 >= ROWS:    
            return False
        
    return True

def validMovementLeft():
    for i in range(len(block_positions)):
        if block_positions[i][1] - 1 < 0:
            return False
        elif grid_matrix[block_positions[i][0]][block_positions[i][1] - 1] != 0:    
            return False

    return True

def validMovementRight():
    for i in range(len(block_positions)):
        if block_positions[i][1] + 1 >= COLUMNS:
            return False
        elif grid_matrix[block_positions[i][0]][block_positions[i][1] + 1] != 0:    
            return False

    return True

def clearRow(i):
    for j in range(len(grid_matrix[i])):
        grid_matrix[i][j] = 0

def shiftRows():
    for i in range(len(grid_matrix) - 1, 1, -1):
        to_swap = True

        for j in range(len(grid_matrix[i])):
            if grid_matrix[i][j] != 0:
                to_swap = False
                break

        if to_swap:
            tmp_row = grid_matrix[i]
            grid_matrix[i] = grid_matrix[i - 1]
            grid_matrix[i - 1] = tmp_row

def deleteCompleteRows():
    global score
    for i in range(len(grid_matrix)):
        to_clear = True
        
        for j in range(len(grid_matrix[i])):
            if grid_matrix[i][j] == 0:
                to_clear = False
                break
        
        if to_clear:
            score += SCORE_ROW_COMPLETE
            clearRow(i)

    shiftRows()

def checkDefeat(shape, x, y):
    #SE NON POSSO DISEGNARE IL BLOCCO, IL GIOCATORE HA PERSO!!!
    tmp_block_position = get_temp_block_position(shape, x, y)

    for i in range(len(tmp_block_position)):
        if tmp_block_position[i][0] < 0 or tmp_block_position[i][0] >= ROWS - 1 or tmp_block_position[i][1] < 0 or tmp_block_position[i][1] > COLUMNS - 1:
            return True
        if grid_matrix[tmp_block_position[i][0]][tmp_block_position[i][1]] != 0:
            return True
        
    return False

def defeat():
    global score
    defeat_text = DEFEAT_FONT.render("GAME OVER!", 1, (255, 255, 255))
    screen.blit(defeat_text, (WIDTH // 2 - defeat_text.get_width() // 2, HEIGHT // 2 - defeat_text.get_height() // 2))
    
    if score > record:
        f = open("record.txt").close() # delete all the content
        f = open("record.txt", "w")
        f.write(str(score))

    score = 0
    pygame.display.update()
    pygame.time.delay(5000)

initializeMatrix()

next_block = True
block_x = block_y = 0
while running:
    clock.tick(FPS)

    if next_block:
        block_x = 50 + random.randint(3, 7) * 40
        block_y = 25
        block = Shape(screen)
        next_block = False
        if not checkDefeat(block.shape, block_x, block_y):
            draw(block_x, block_y)
            pygame.time.delay(500)
            continue
        else:
            defeat()
            initializeMatrix()
            next_block = True
            continue

    block_positions = block.positionInTheGrid
    block_moved = False # it records if the block has been moved by the user (left or right)

    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                if validRotation(block, block_x, block_y):
                    block.rotate()
                    block_moved = True
            if event.key == K_LEFT and not block_moved:
                if validMovementLeft():
                    block_x -= blocksize
                    block_moved = True
            if event.key == K_RIGHT and not block_moved:
                if validMovementRight():
                    block_x += blocksize
                    block_moved = True

    if not block_moved:
        # move down
        if validMovmentDown():  
            block_y += blocksize
        else:
            for i in range(len(block_positions)):
                grid_matrix[block_positions[i][0]][block_positions[i][1]] = block.color_pos
            score += SCORE_BLOCK_POSITIONED
            next_block = True
    
    draw(block_x, block_y)

    pygame.time.delay(300)
    
pygame.quit()