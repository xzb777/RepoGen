import pygame
import sys
import time


CELL_SIZE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
BLUE = (0,0,255) # speed of the animation
directions = ['up', 'right', 'down', 'left']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 2],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]





class Robot:
    def __init__(self, initial_pos=[1,1], initial_dir='up', delay=0):
        pygame.init()
        self.window = pygame.display.set_mode((len(maze[0])*CELL_SIZE, len(maze)*CELL_SIZE))
        self.pos = initial_pos
        self.dir = initial_dir
        self.delay = delay

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_forward(self):
        ahead = self.get_front_cell()
        if ahead == 1:
            return
        elif ahead == 2:
            pygame.quit()
            quit() 
        if self.dir == 'up':
            self.pos[1] -= 1
        elif self.dir == 'right':
            self.pos[0] += 1
        elif self.dir == 'down':
            self.pos[1] += 1
        elif self.dir == 'left':
            self.pos[0] -= 1

    def turn_left(self):
        self.dir = directions[(directions.index(self.dir) - 1) % 4]

    def turn_right(self):
        self.dir = directions[(directions.index(self.dir) + 1) % 4]

    def move(self, instruction):
        """this function takes the cpu output and moves the robot accordingly"""
        self.event_check()
        if instruction == [0,0,0,0,0,0,1,1]:
            self.move_forward()
        elif instruction == [0,0,0,0,0,0,0,1]:
            self.turn_left()
        elif instruction == [0,0,0,0,0,0,1,0]:
            self.turn_right()
        draw(self)



    def get_front_cell(self):
        if self.dir == 'up':
            return maze[self.pos[1]-1][self.pos[0]]
        elif self.dir == 'right':
            return maze[self.pos[1]][self.pos[0]+1]
        elif self.dir == 'down':
            return maze[self.pos[1]+1][self.pos[0]]
        elif self.dir == 'left':
            return maze[self.pos[1]][self.pos[0]-1]
        
    def get_front_cell_bit(self):
        """This functions reads the front cell and passes it to the cpu input"""
        front = self.get_front_cell()
        #convert to byte
        if front == 0:
            return [0,0,0,0,0,0,0,0]
        elif front == 1:
            return [0,0,0,0,0,0,0,1]
        elif front == 2:
            pygame.quit()
            sys.exit('Robot reached the end of the maze!') 



def draw(robot):
    window = robot.window
    """Pass in a robot object and draw the maze and robot"""
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:  # wall
                pygame.draw.rect(window, BLACK, rect)
            elif maze[y][x] == 2:  # end
                pygame.draw.rect(window, BLUE, rect)
            else:  # path
                pygame.draw.rect(window, WHITE, rect)


    # Draw the square ahead of the robot
    if robot.dir == 'up' and robot.pos[1] > 0:
        rect = pygame.Rect(robot.pos[0]*CELL_SIZE, (robot.pos[1]-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'right' and robot.pos[0] < len(maze[0]) - 1:
        rect = pygame.Rect((robot.pos[0]+1)*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'down' and robot.pos[1] < len(maze) - 1:
        rect = pygame.Rect(robot.pos[0]*CELL_SIZE, (robot.pos[1]+1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'left' and robot.pos[0] > 0:
        rect = pygame.Rect((robot.pos[0]-1)*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, GREEN, rect)
    # Draw the robot
    rect = pygame.Rect(robot.pos[0]*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, RED, rect)
    pygame.display.update()
    time.sleep(robot.delay)



