# SIT 215 ASSIGNMENT 1

# HERE I AM IMPORTING THE LIBRARIES REQUIRED FOR MY PROJECT
import matplotlib.pyplot as plt
import time
import numpy as np
import pygame


# THE FOLLOWING METHOD OPENS AND READS THE MAZE (MAZE.TXT)
def read_maze(maze):
    with open(maze, 'r') as maze_opened:
        maze = [list(line.strip()) for line in maze_opened]

    # CREATING TWO VARIABLES START AND END AND INITIALIZING TO NONE
    start, end = None, None

    # USING THE ENUMERATE FUNCTION TO RUN THROUGH THE MAZE AND FIND THE INDEX OF THE REQUIRED ELEMENTS (START AND END)
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            # HERE WE ARE SEARCHING FOR 'S' WITHIN THE MAZE AND SETTING THIS AS THE STARTING POINT
            if cell == 'S':
                starting_point = (row_index, col_index)
            # HERE WE ARE SEARCHING FOR 'E' WITHIN THE MAZE AND SETTING THIS AS THE END POINT
            elif cell == 'E':
                ending_point = (row_index, col_index)

    return maze, starting_point, ending_point

# HERE WE ARE CALLING ON THE READ_MAZE FUNCTION USING THE MAZE.TXT FILE AND RETURNS THE VALUES OF MAZE, STARTING POINT AND ENDING POINT
maze, starting_point, ending_point = read_maze("maze.txt")

# THIS FUNCTION USES A DEPTH-FIRST ALGORITM TO FIND A PATH FROM THE STARTING POINT TO THE ENDING POINT IN THE MAZE I CREATED.
# IT TAKES THE VARIABLES CREATED IN THE 'read_maze' FUNCTION
def dfs(maze, starting_point, ending_point):
    
    passed = set()      # INITIALIZE PASSED WITH AN EMPTY SET (set() function)
    search_state = [(starting_point, [])]  # INITIALIZE THE SEARCH_STATE LIST (DATASTRUCTURE) CONTAINING TWO ELEMENTS USED TO KEEP TRACK OF THE CURRENT POSITION IN THE MAZE AND THE PATH TAKEN

    # SEE NOTES BESIDES INSTRUCTIONS WITHIN THIS LOOP
    while search_state:
        position, path = search_state.pop() # THE LAST ELEMENT WITHIN SEARCH_STATE IS POPPED AND POSITION AND PATH ARE BOTH EXTRACTED
        if position == ending_point:        # IF POSITION IS EQUAL TO ENDING_POINT, IT HAS COMPLETED THE SEARCH AND RETURNS PATH TAKEN PLUS CURRENT POSITION
            return path + [position]
        if position in passed:              # IF CURRENT POSITION HAS ALREADY BEEN PASSED THE LOOP WILL MOVE ONTO THE NEXT ITERATION, THIS ENSURES NO CYCLES
            continue

        passed.add(position)                # IF THE CURRENT POSITION HAS NOT BEEN VISITED, IT IS NOW ADDED TO THE PASSED SET

        row, col = position                 # HERE WE ARE 'UNPACKING' POSITION AND ASSIGNING TO ROW AND COL

        # PLEASE TAKE NOTE THAT THIS ENABLES SEARCH UP, DOWN, LEFT AND RIGHT AS PER THE ASSIGNMENT REQUIREMENTS
        for horizontal, vertical in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            if (
                0 <= horizontal < len(maze) and 
                0 <= vertical < len(maze[0]) and 
                maze[horizontal][vertical] != '#' and 
                (horizontal, vertical)  not in passed
            ):
                search_state.append(((horizontal, vertical), path + [position]))

    return None

# HERE WE CREATE A VARIABLE 'PATH' WITH THE 
path = dfs(maze, starting_point, ending_point)

# THE FOLLOWING FUNCTION SERVES AS THE VISUALIZATION FOR THE MAZE AND THE SORTING, USING THE VARIABLES OF MAZE, PATH, BLOCK_SIZE AND DELAY
# WE FIRST CREATE VARIABLES FOR WIDTH AND HEIGHT, AS INITIALIZE THEM BY USING 'len(maze[0])' TO CALCULATE THE LENGTH OF THE FIRST ROW (WIDTH) 
# AND 'len(maze)' TO CALCULATE THE NUMBER OF ROWS (HEIGHT).
def visualize(maze, path, block_size=25, delay=0.5):
    
    width = len(maze[0]) * block_size
    height = len(maze) * block_size
    
    pygame.init()   # INITIALIZE PYGAME LIBRARY
    screen = pygame.display.set_mode((width, height))                   # SET WINDOW SIZE
    pygame.display.set_caption("Visualization of Maze Being Solved")    # SET WINDOW CAPTION/NAME

    # ASSIGNING COLOUR VALUES TO EACH VALUE/ASSET WITHIN THE MAZE (RGB) & MAKING BACKGROUND WHITE (MADE IT LOOK MUCH NICER)
    boarder_colour = (64, 64, 64)
    path_colour = (55, 255, 0)
    ending_colour = (140, 50, 55)
    npc_colour = (55, 50, 140)
    screen.fill((255, 255, 255))
    
    # THIS LOOP ITERATES THROUGH EACH INDEX WITHIN THE PATH LIST USING VARIBLE 'i' AND ASSIGNING THE CURRENT INDEX TO THE VARIABLE POSITION
    for i in range(len(path)):
        position = path[i]
    
        # TERMINATES THE PROGRAM AND ALLOWS THE USER TO CLOSE THE WINDOW IN THE MIDDLE OF THE PROGRAM RUNNING
        # WITHOUT THIS, I FOUND THAT THE PROGRAM CRASHED WHEN I TRIED TO CLOSE THE WINDOW DURING OPERATION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        # IN THE FOLLOWING LOOP ITERATES THROUGH THE ROWS OF MAZE USING 'enumerate()' FUNCTION TO KEEP TRACK OF ROW INDEX
        for row_index, row in enumerate(maze):
            # IN THE FOLLOWING LOOP ITERATES THROUGH THE CELLS OF ROW USING 'enumerate()' FUNCTION TO KEEP TRACK OF COLUMN INDEX
            # WE THEN USE THE 'pygame.Rect()' FUNCTION TO CREATE A REPRESENTATION OF THE MAZE (VISUALISE), I HAVE CREATED A VARIABLE CALLED 'block_size' THAT CAN BE ADJUSTED 
            # WITHIN THE IF STATEMENTS I SET THE ARGUMENTS FOR WHERE THE COLOURS BELONG.
            for col_index, cell in enumerate(row):
                area = pygame.Rect(col_index * block_size, row_index * block_size, block_size, block_size)
                if cell == '#':
                    pygame.draw.rect(screen, boarder_colour, area)
                elif (row_index, col_index) == position:
                    pygame.draw.rect(screen, npc_colour, area)
                elif (row_index, col_index) in path[:i]:
                    pygame.draw.rect(screen, path_colour, area)
                elif cell == 'E':
                    pygame.draw.rect(screen, ending_colour, area)

        # UPDATE THE SCREEN WITH UPDATED VISUALIZATION
        pygame.display.flip()
        # ADD DELAY BETWEEN EACH FRAME (VARIABLE USED IS 'delay')
        time.sleep(delay)

    # KEEPS THE WINDOW (VISUALIZATION) OPEN EVEN WHEN THE MAZE HAS BEEN COMPLETED, THE USER CLOSES THE WINDOW WHEN READY
    # WITHOUT THIS, THE WINDOW AUTOMATICALLY CLOSED WHEN THE MAZE WAS COMPLETED
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
   

# HERE WE ARE CALLING ON THE FUNCTIONS TO WORK THROUGH THE MAZE 
def main():
    maze, starting_point, ending_point = read_maze("maze.txt")
    path = dfs(maze, starting_point, ending_point)
    visualize(maze, path)

if __name__ == "__main__":
    main()
