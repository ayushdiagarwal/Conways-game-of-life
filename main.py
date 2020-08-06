# Importing some modules

import pygame as pg
import random
import os


# RULES

# GRID = [1,1,]
#        [1,0,1]
#        [1,1,,]    

# Neighbours of the cell with value 0 are all the cells with value 1 (In just this particular example)

# Any live cell with fewer than two live neighbours dies, as if by underpopulation. --> 1 --> Neighbours < 2 --> 0
# Any live cell with more than three live neighbours dies, as if by overpopulation. --> 1 --> Neighbours > 3 --> 0
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. --> 0 --> Neighbours == 3 --> 1


# Intializing pygame
pg.init()

# window display stuff
DISPLAY_SIDE = 700
DP = pg.display.set_mode((DISPLAY_SIDE, DISPLAY_SIDE))
pg.display.set_caption("Conway's Game Of Life")

# Frame
frame = 100
clock = pg.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)     
GREY = (168, 159, 158)
RED = (255, 0, 0)
BLUE = (50, 119, 168)

# some variables
col_no = 35
yes1 = yes2 = False
start = End = None

class Life:
    # A matrix/grid for the window
    matrix = [[random.randrange(0,2) for _ in range(col_no)] for _ in range(col_no)]	
    # print(matrix)

    def __init__(self):
        # Main pygame loop
        while True:
            # Checking if someone is quiting the game
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            # Filling white color everytime
            DP.fill(WHITE)
            # Running some functions to do stuff
            self.mark_position()
            self.draw_grid()
            self.apply_rules()

            # Updating the pygame window
            clock.tick(frame)
            pg.display.update()

    # the function draws a rect/line
    def draw_rect(self, color, x, y, width, height):
        #surface, color, (x, y, width, height)
        pg.draw.rect(DP, color, (x, y, width, height))

    # drawing the whole grid
    def draw_grid(self):
        col_dis = DISPLAY_SIDE // col_no
        col_dis_cov = DISPLAY_SIDE // col_no
        thick = 1

        for i in range(col_no):
            # Draws Horizontal lines
            self.draw_rect(GREY, 0, col_dis_cov, DISPLAY_SIDE, 0)

            # Draws Vertical Lines
            self.draw_rect(GREY, col_dis_cov, 0, thick, DISPLAY_SIDE)
            col_dis_cov += col_dis

    # getting position of the selected box
    def get_pos(self):
        global yes1, yes2, start, end
        click = pg.mouse.get_pressed()
        mouse = pg.mouse.get_pos()
        # if there is a click
        if click[0] == 1:
            # X axis of the mouse position
            x_pos = mouse[0] // (DISPLAY_SIDE // col_no)
            # Y axis of the mouse position
            y_pos = mouse[1] // (DISPLAY_SIDE // col_no)

            # Getting the starting point
            if yes1 == False:
                for i in self.matrix:
                    if 2 not in i:
                        # if (x_pos, y_pos) != end:
                        yes1 = True
                        start = (x_pos, y_pos)
                        self.matrix[x_pos][y_pos] = 2

            # Getting the ending point
            if yes2 == False:
                for i in self.matrix:
                    if 3 not in i:
                        if (x_pos, y_pos) != start:
                            yes2 = True
                            end = (x_pos, y_pos)
                            self.matrix[x_pos][y_pos] = 3

            # if starting and ending points are given, the getting the obstacles points
            if yes1 == yes2 == True:
                if (x_pos, y_pos) != start:
                    if (x_pos, y_pos) != end:
                        self.matrix[x_pos][y_pos] = 1

        # If right click, it deletes the obstacle
        if click[2] == 1:
            # X axis of the mouse position
            x_pos = mouse[0] // (DISPLAY_SIDE // col_no)
            # Y axis of the mouse position
            y_pos = mouse[1] // (DISPLAY_SIDE // col_no)

            if self.matrix[x_pos][y_pos] == 1:
                self.matrix[x_pos][y_pos] = 0
            

    # Draws the square/box wherever it needs to be drawn
    def mark_position(self):
        rect_side = DISPLAY_SIDE//col_no
        for i in range(col_no):
            for j in range(col_no):
                # black color for the alive cells
                if self.matrix[i][j] == 1:
                    self.draw_rect(BLUE, rect_side*i, rect_side*j, rect_side, rect_side)


    # Function to count neighbouors of each cell
    def count_neighbors(self, grid, x, y):
        sumi = 0

        for i in range(-1,2):
            for j in range(-1, 2):

                # Checking if the neighbour even exists or not 
                if x + i >= 0 and x+i < col_no:
                    if y + j >= 0 and y+j < col_no:
                        sumi += grid[x+i][y+j]

        # subtract this coloumn value
        sumi -= grid[x][y]
        # print(sumi)

        # print(self.sumi)
        return sumi


    def apply_rules(self):

        # 1 --> Neighbours < 2 --> 0
        # 1 --> Neighbours > 3 --> 0
        # 0 --> Neighbours == 3 --> 1

        for i in range(col_no):
            for j in range(col_no):
                neighbors = self.count_neighbors(self.matrix, i, j)
                #print(neighbors)

                if neighbors < 2:
                    self.matrix[i][j] = 0
                elif neighbors > 3:
                    self.matrix[i][j] = 0
                elif neighbors == 3 and self.matrix[i][j] == 0:
                    self.matrix[i][j] = 1



    


# Running the program
Life()
