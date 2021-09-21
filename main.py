import pygame
from barcode import EAN13
from barcode.writer import ImageWriter
from pygame.locals import *
import random
import os

number = '123456789123'

pygame.init()
CLOCK = pygame.time.Clock()

try:
    os.remove('code.png')
except:
    pass

winHeight = 1200 + 3 #TODO fix this later
winWidth = 800 + 3

WINDOW = pygame.display.set_mode((winHeight, winWidth))
pygame.display.set_caption('Wake up!')

WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLACK = 0, 0, 0
BLUE = 0, 0, 255
stack = []
all_walls = []
class Cell:
    size = 80
    def __init__(self, x, y):
        self.x = x * Cell.size
        self.y = y * Cell.size
        self.current = False
        self.visited = False
        self.neighbors = {'left': None, 'right': None, 'top': None, 'bottom': None} 
        self.possible = []
        self.left = 1
        self.right = 1
        self.bottom = 1
        self.top = 1
        self.rect = pygame.rect.Rect(self.x,self.y, Cell.size, Cell.size)
        self.next_cell = None
        self.xindex = x
        self.yindex = y
  


    def is_current(self):
        if self.current == True:
            return True
        else:
            return False

    def make_current(self):
        self.current = True

    def draw_cell(self, surface):
        if self.current:
            pygame.draw.rect(surface, RED, self.rect)

    def draw_walls(self, surface):
        width = 5
        if self.left != 0:
            self.left = pygame.rect.Rect(self.x, self.y, width, Cell.size)
            pygame.draw.rect(surface, BLACK, pygame.rect.Rect(self.x, self.y, width, Cell.size))
        if self.right != 0:
            self.right = pygame.rect.Rect(self.x + Cell.size, self.y, width, Cell.size)
            pygame.draw.rect(surface, BLACK, pygame.rect.Rect(self.x + Cell.size, self.y, width, Cell.size))
        if self.top != 0:
            self.top = pygame.rect.Rect(self.x, self.y, Cell.size, width)
            pygame.draw.rect(surface, BLACK, pygame.rect.Rect(self.x, self.y, Cell.size, width))
        if self.bottom != 0:
            self.bottom = pygame.rect.Rect(self.x, self.y + Cell.size, Cell.size, width)
            pygame.draw.rect(surface, BLACK, pygame.rect.Rect(self.x, self.y + Cell.size, Cell.size, width))
    
    def collision_test(self, player):
        if self.left != 0:
            if self.left.colliderect(player):
                    return True
  
        if self.right != 0:
            if self.right.colliderect(player):
                    return True
        if self.bottom != 0:
            if self.bottom.colliderect(player):
                    return True

        if self.top != 0:
            if self.top.colliderect(player):
                    return True
        


    def get_neighbors(self):
        if self.y - Cell.size >= 0:
            self.neighbors["top"] = grid[int(self.x/Cell.size)][int(self.y/Cell.size-1)]
        if self.y + Cell.size * 2 <= WINDOW.get_height():
            self.neighbors["bottom"] = grid[int(self.x/Cell.size)][int(self.y/Cell.size+1)]
        if self.x + (Cell.size * 2) <= WINDOW.get_width():
            self.neighbors["right"] = grid[int(self.x/Cell.size+1)][int(self.y/Cell.size)]
        if self.x - Cell.size >= 0:
            self.neighbors["left"] = grid[int(self.x/Cell.size-1)][int(self.y/Cell.size)]

        if self.neighbors["top"] != None:
            if self.neighbors["top"].visited == False:
                self.possible.append(self.neighbors["top"])
        if self.neighbors["left"] != None:
            if self.neighbors["left"].visited == False:
                self.possible.append(self.neighbors["left"])
        if self.neighbors["right"] != None:
            if self.neighbors["right"].visited == False:
                self.possible.append(self.neighbors["right"])
        if self.neighbors["bottom"] != None:
            if self.neighbors["bottom"].visited == False:
                self.possible.append(self.neighbors["bottom"])
        
        if len(self.possible) > 0:
            self.next_cell = self.possible[random.randrange(0, len(self.possible))]
            return self.next_cell
        elif len(self.possible) == 0:
            return False


def break_wall(current, next):
    x = int(current.xindex) - int(next.xindex)
    y = int(current.yindex) - int(next.yindex)
    if x == -1:
        current.right = 0
        next.left = 0
    if x == 1:
        current.left = 0
        next.right = 0
    if y == -1:
        current.bottom = 0
        next.top = 0
    if y == 1:
        current.top = 0
        next.bottom = 0
    
   
    
def player_rect(x, y):
    playerRect = pygame.rect.Rect(x, y, 20, 30)
    pygame.draw.rect(WINDOW, GREEN, playerRect)
    return playerRect

def end_rect(x, y):
    end_rect = pygame.rect.Rect(x, y, 20, 30)
    pygame.draw.rect(WINDOW, RED, end_rect)
    return end_rect

grid = []
for x in range(WINDOW.get_width()//Cell.size):
    grid.append([])
    for y in range(WINDOW.get_height()//Cell.size):
        grid[x].append(Cell(x,y))

current = grid[0][0]
next = 0

player_momentum = [0,0]
player_pos = [10, 10]
end_pos = random.choice([[1160, 760], [1160, 30]])
moving_up = False
moving_left = False
moving_down = False
moving_right = False

running = True
count = 0

def collision_test(entity, walls):
    collisions = []
    for wall in walls:
        if entity.colliderect(wall):
            collisions.append(wall)
        print("COLLIDED")
    return collisions


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_w:
                moving_up = True
            if event.key == K_s:
                moving_down = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
        if event.type == KEYUP:
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_d:
                moving_right = False

    WINDOW.fill(WHITE)

    current.visited = True
    current.make_current()

    for col in grid:
        for cell in col:
            cell.draw_walls(WINDOW)

    next = current.get_neighbors()


    if next != False:
        current.possible = []
        stack.append(current)
        break_wall(current, next)
        current.current = False
        current = next
    
    elif len(stack) > 0:
        current.current = False
        current = stack.pop()    

    elif next == False: # START GAME HERE
        current.current = False

        player = player_rect(player_pos[0], player_pos[1])
        end = end_rect(end_pos[0], end_pos[1])


        if player.colliderect(end):
            my_code = EAN13(number, writer=ImageWriter())
            my_code.save("code")
            BARCODE = pygame.image.load("code.png")
            WINDOW.fill(WHITE)
            WINDOW.blit(BARCODE, (396,76))
        for col in grid:
            for cell in col:
                if cell.collision_test(player):
                    player_pos = [10, 10]
       
        if moving_right:
            player_momentum[0] = 3
            player_pos[0] += 3
        if moving_left:
            player_momentum[0] = -3
            player_pos[0] += -3
        if moving_down:
            player_momentum[1] = 3
            player_pos[1] += 3
        if moving_up:
            player_momentum[1] = -3
            player_pos[1] -= 3
        if moving_right == False:
            if moving_left == False:
                if moving_down == False:
                    if moving_up == False:
                        player_momentum[0] = 0
                        player_momentum[1] = 0

  

                    
        



        
        
        

  

    
    
    CLOCK.tick(60)
    pygame.display.flip()


pygame.quit()

