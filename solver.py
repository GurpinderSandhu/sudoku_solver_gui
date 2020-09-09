# use 1-9 in each row, column and block once and only once
# use backtracking algorithim, find all possible solutions given constraints
# as soon as one approach is illegal, backtrack and try another solution until 
# it works
# identify position by (ri, ci) row index, column index

def printBoard(bo): 
    for i in range(9): 
        for j in range(9): 
            print(bo[i][j], end= " ")
        print("\n")
        
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
    #print(block)
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

def solver(bo):

    position = nextZero(bo)

    if position:
        row, col = position
    else:
        return True

    for attempt in range(1,10):
        if isValid(bo,position,attempt):
            bo[row][col] = attempt

            if solver(bo):
                #valid attempt found now keep going by calling solver(bo)
                #print(bo)
                return True     
            bo[row][col] = 0
    #once it exhausts all options and nothing is valid, we need to set it back to zero
    #this triggers backtrack, goes to previous layer of onion and goes to line 86 and continue the for loop
    return False

def main():
    board = [[3, 0, 6, 5, 0, 8, 4, 0, 0], 
         [5, 2, 0, 0, 0, 0, 0, 0, 0], 
         [0, 8, 7, 0, 0, 0, 0, 3, 1], 
         [0, 0, 3, 0, 1, 0, 0, 8, 0], 
         [9, 0, 0, 8, 6, 3, 0, 0, 5], 
         [0, 5, 0, 0, 9, 0, 6, 0, 0], 
         [1, 3, 0, 0, 0, 0, 2, 5, 0], 
         [0, 0, 0, 0, 0, 0, 0, 7, 4], 
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    if solver(board):
        printBoard(board)
    else:
        print("no solution")


if __name__=="__main__": 
    main()



