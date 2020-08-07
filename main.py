# Importing some modules

import pygame as pg
import random
import time

# Intializing pygame
pg.init()

# some variables
col_no = 35 # 70
into = 18
# window display stuff
DISPLAY_SIDE = col_no*into
DP = pg.display.set_mode((DISPLAY_SIDE, DISPLAY_SIDE+50))
pg.display.set_caption("Conway's Game Of Life")

# Frame
frame = 100
clock = pg.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (3, 252, 173)
BLACK = (0,0,0)     
GREY = (168, 159, 158)
RED = (255, 0, 0)
BLUE = (50, 119, 168)
DARK = (106, 95, 115)




class Life:
    # A matrix/grid for the window
    matrix = [[0 for _ in range(col_no)] for _ in range(col_no)]
    end = time.time()
    end2 = time.time()
    started = False
    generation = 0

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
            if self.started == False:
                self.get_pos()
            self.mark_position()
            self.draw_grid()

            # Checking for space key
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                start = time.time()
                if start - self.end>0.05:
                    self.apply_rules()
                    self.add_and_remove()
                self.end = time.time()

            # Checking for "S" key
            if self.started == True:
                start2 = time.time()
                if start2 - self.end2 > 0.009:
                    old = self.matrix
                    self.apply_rules()
                    self.add_and_remove()
                self.end2 = time.time()

            if keys[pg.K_s]:
                self.started = True

            # Checking for "C" key
            if keys[pg.K_c]:
                self.started = False

            # Checking for "R" key --> Reset
            if keys[pg.K_r]:
                self.started = False
                self.matrix = [[0 for _ in range(col_no)] for _ in range(col_no)]
                self.generation = 0

            # Printing generation

            self.print_stuff(40, f"Generation: {self.generation}", DARK, DISPLAY_SIDE//2-70, DISPLAY_SIDE+15)

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
        col_dis_cov = 0
        thick = 1

        for _ in range(col_no+1):
            # Draws Horizontal lines
            self.draw_rect(GREY, 0, col_dis_cov, DISPLAY_SIDE, 0)

            # Draws Vertical Lines
            self.draw_rect(GREY, col_dis_cov, 0, thick, DISPLAY_SIDE)
            col_dis_cov += col_dis


    # getting position of the selected box
    def get_pos(self):
        click = pg.mouse.get_pressed()
        mouse = pg.mouse.get_pos()
        # if there is a click
        if click[0] == 1:
            # X axis of the mouse position
            x_pos = mouse[0] // (DISPLAY_SIDE // col_no)
            # Y axis of the mouse position
            y_pos = mouse[1] // (DISPLAY_SIDE // col_no)
            self.matrix[x_pos][y_pos] = 1

            #print(x_pos, y_pos)


        # If right click, it deletes the cell
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

    # function for printing stuff
    def print_stuff(self, font_size, text, color, x, y):
        self.font = pg.font.Font(None, font_size)
        self.text_render = self.font.render(text, 1, color)
        DP.blit(self.text_render, (x, y))


    # Function to count neighbouors of each cell
    def count_neighbors(self, grid, x, y):
        global into, col_no
        sumi = 0

        for i in range(-1,2):
            for j in range(-1, 2):

                # Checking if the neighbour even exists or not 
                if x + i >= 0 and x+i < col_no:
                    if y + j >= 0 and y+j < col_no:
                        sumi += grid[x+i][y+j]


        # subtract this cell value
        sumi -= grid[x][y]
        return sumi


    def apply_rules(self):

        # RULES
        # 1 --> Neighbours < 2 --> 0
        # 1 --> Neighbours > 3 --> 0
        # 0 --> Neighbours == 3 --> 1

        self.to_remove = []
        self.to_add = []

        for i in range(col_no):
            for j in range(col_no):
                neighbors = self.count_neighbors(self.matrix, i, j)

                # Basically the rules

                if neighbors < 2:
                    self.to_remove.append([i,j])
                elif neighbors > 3:
                    self.to_remove.append([i,j])
                elif neighbors == 3 and self.matrix[i][j] == 0:
                    #self.matrix[i][j] = 1
                    self.to_add.append([i,j])

    # Implementing the rules
    def add_and_remove(self):
        for i in range(len(self.to_remove)):
            x,y = self.to_remove[i]
            self.matrix[x][y] = 0
        for i in range(len(self.to_add)):
            x,y = self.to_add[i]
            self.matrix[x][y] = 1
        self.generation += 1

# Running the program
Life()