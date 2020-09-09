import pygame
import time

#essential to every pygame application
pygame.init()
pygame.font.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
green = (0,128,0)
red = (255, 0, 0)

class SudokuGrid:
    board = [
        [0, 0, 2, 7, 0, 0, 3, 5, 8],
        [7, 0, 0, 5, 8, 0, 9, 1, 0],
        [1, 5, 8, 3, 6, 0, 0, 0, 0],
        [9, 0, 6, 0, 0, 5, 0, 3, 4],
        [0, 4, 0, 6, 9, 0, 5, 0, 1],
        [5, 8, 0, 1, 0, 7, 2, 0, 0],
        [0, 7, 1, 0, 0, 6, 0, 0, 5],
        [3, 6, 9, 0, 5, 8, 0, 4, 0],
        [0, 0, 0, 0, 7, 1, 6, 9, 3]
    ]
    
    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.squares = [[Square(self.board[row][col], row, col, width, height) for col in range(cols)] for row in range(rows)]
        self.width = width
        self.height = height
        self.window = window
        self.model = None
        self.update_model()
    
    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def show_grid(self, solved):
        #grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            distance = round(gap*i)
            if i % 3 == 0:
                thickness = 5
            else:
                thickness = 1
            if solved:
                pygame.draw.line(self.window, green, (0, distance), (self.width, distance), thickness)
                pygame.draw.line(self.window, green, (distance, 0), (distance, self.height), thickness)
            else:
                pygame.draw.line(self.window, black, (0, distance), (self.width, distance), thickness)
                pygame.draw.line(self.window, black, (distance, 0), (distance, self.height), thickness)

        
        #indivdual squares
        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col].set_value(self.model[row][col])
                self.squares[row][col].show_number(self.window)
        
        #instructions
        font = pygame.font.SysFont("dejavusans", 20)
        text = font.render(str("Press SPACE to solve!"), 1, red)
        self.window.blit(text, (round(display_width/4), display_height-30))
    
    def solve_gui(self):
        self.update_model()
        position = nextZero(self.model)

        if position:
            row, col = position
        else:
            return True

        for attempt in range(1,10):
            if isValid(self.model,position,attempt):
                self.model[row][col] = attempt
                self.squares[row][col].set_value(attempt)
                self.squares[row][col].show_change(self.window,True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(250)

                if self.solve_gui():
                    #valid attempt found now keep going
                    return True  
                
                self.model[row][col] = 0   
                self.squares[row][col].set_value(0)
                self.update_model()
                self.squares[row][col].show_change(self.window,False)
                pygame.display.update()
                pygame.time.delay(250)
        #once it exhausts all options and nothing is valid, we need to set it back to zero
        #this triggers backtrack, goes to previous layer of onion and continue the for loop to find next valid value
        return False

class Square:
    def __init__(self,value,row,col,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
    
    def show_number(self, win):
        font = pygame.font.SysFont("dejavusans", 30)
        gap = round(self.width / 9)
        x = self.col * gap
        y = self.row * gap

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (round(gap / 2) - round(text.get_width() / 2)), y + (round(gap / 2) - round(text.get_height() / 2))))

    def show_change(self, win, valid=True):
        font = pygame.font.SysFont("dejavusans", 30)
        gap = round(self.width / 9)
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (round(gap / 2) - round(text.get_width() / 2)), y + (round(gap / 2) - round(text.get_height() / 2))))
        if valid:
            pygame.draw.rect(win, green, (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, red, (x, y, gap, gap), 3)
        
    def set_value(self, val):
        self.value = val

def nextZero(bo):
    for ri in range(len(bo)):
        for ci in range(len(bo[0])):
            if bo[ri][ci] == 0:
                return((ri, ci))
    #board has no more zeros
    return(None)

def getBlock(bo,pos):
    block = []
    row = pos[0] + 1
    col = pos[1] + 1
    if(1 <= col <= 3):
        stack = 1
    elif(4<= col <= 6):
        stack = 2
    else:
        stack = 3
    if(1 <= row <= 3):
        rank = 1
    elif(4<= row <= 6):
        rank = 2
    else:
        rank = 3
    #area becomes end at (rank*3)-1 begin at (rank*3-2)-1
    for row in range(((rank*3-2)-1), (rank*3)):
        for col in range(((stack*3-2)-1), (stack*3)):
            block.append(bo[row][col])
    return(block)
     
def isValid(bo,pos,val):
    #row check
    for ele in bo[pos[0]]:
        if ele == val:
            return False
    
    #col check
    for row in bo:
        if row[pos[1]] == val:
            return False

    #block check
    for ele in getBlock(bo,pos):
        if ele == val:
            return False
    return True

def redrawWindow(win, board,solved):
    win.fill((255,255,255))
    board.show_grid(solved)

def prettyPrintBoard(bo):
    s = [[str(e) for e in row] for row in bo]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def main():
    display_width = 540
    display_height = 600

    #return a pygame surface object (canvas window to use)
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption("Sudoku Solver")
    
    board = SudokuGrid(9,9,display_width,display_height-60,gameDisplay)

    running = True
    solved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    solved = True
                    prettyPrintBoard(board.model)
        if solved:
            redrawWindow(gameDisplay, board, True)    
        else:
            redrawWindow(gameDisplay, board, False)
        pygame.display.update()

if __name__=="__main__": 
    main()
    pygame.quit()
    quit()