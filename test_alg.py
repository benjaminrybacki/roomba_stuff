#Main class to test code
def main():

    #Initialize Empty array with zeros
    global dis_arr
    dis_arr = [[0 for i in range(5)] for j in range(5)]

    #Primary array: -1 -> wall, 0 -> clean, 1 -> unclean
    global arr
    arr = [[1 for i in range(5)] for j in range(5)]

    #Initialize roomba size for cell checking
    global RIGHT_BOUND, BOTTOM_BOUND
    RIGHT_BOUND = len(arr[0])
    BOTTOM_BOUND = len(arr)
    
    #Initialize roomba position and clean initial square
    global roomba_row, roomba_col, start_row, start_col
    roomba_row, start_row = 2, 2
    roomba_col, start_col = 2, 2
    
    clean()

    #Populate Distance Array
    populateDistanceArray()

    #Show Radial Distance Array
    printDistance()

    #Show bool array start
    printCleaned()

    #Test path
    path = [[2,3],[2,4],[3,4],[3,3],[3,2],[4,2],[4,3],[4,4]]

    #Move roomba along path
    for move in path:
        moveTo(move[0], move[1])

    #Show cleaned after movement
    printCleaned()

    print(bestAdjacent(3,3))

    
#TODO
def branch(start_row, start_col):
    print("x")
    #Do bestAdjacent - if [-1, -1] is returned, find nearestDirty and go, otherwise if no dirty, go to start position

#TODO
#Return the nearest unclean square to the roomba at (roomba_row, roomba_col). Returns [-1, -1] if everything is clean
def nearestDirty():
    print("to dirty square")
    #Will be difficult to account for walls if it get stuck in a room

#TODO
#Return the path to a square (row,col) if everyting else is clean - can be starting spot or elsewere
def goTo(row, col):
    #Figure out how to avoid walls
    print("go to (row,col)")
    
#Return the best adjacent node to the current node at (row, col), if none, returns [-1, -1]
def bestAdjacent(row, col):
    #Find all adjacent cells
    options = adjacentDirty(row, col)

    #If their are no dirty neighbors, return [-1, -1]
    if len(options) == 0:
        return[-1, -1]

    #Initalize best node at 9 dirty edges
    min_dirty_edges = 9

    #Initalize empty list of next move
    best_adjacent = []

    for option in options:
        dirty_edges = adjacentDirtyCount(option[0], option[1])
        if (dirty_edges < min_dirty_edges):
            #If option is better, reset max dirty edges value and store next move
            min_dirty_edges = dirty_edges
            best_adjacent = option

    #Return the best option as a single path
    return best_adjacent
    
#Return a list of lists of all adjacent cells to the roomba
def adjacentCells(row, col):
    #List of available cells to return
    available = []

    #Range of neighboring cells to consider
    col_range = range(max(0, col-1), min(col+2, RIGHT_BOUND))
    row_range = range(max(0, row-1), min(row+2, BOTTOM_BOUND))

    #Find all adjacent notes that are not walls
    for r in row_range:
        for c in col_range:
            #exclude current cell
            if r != row or c != col:
                if (arr[r][c] != -1):
                    available.append([r, c])

    return available

#Return a list of lists of all adjacent and dirty cells to the roomba
def adjacentDirty(row, col):
    #List of dirty cells to return
    dirty = []

    #Range of neighboring cells to consider
    col_range = range(max(0, col-1), min(col+2, RIGHT_BOUND))
    row_range = range(max(0, row-1), min(row+2, BOTTOM_BOUND))

    #Find all adjacent notes that are dirty
    for r in row_range:
        for c in col_range:
            #exclude current cell
            if r != row or c != col:
                if (arr[r][c] == 1):
                    dirty.append([r, c])

    return dirty

#Return the amount of dirty cells adjacent to a target cell
def adjacentDirtyCount(row, col):
    #Range of neighboring cells to consider
    col_range = range(max(0, col-1), min(col+2, RIGHT_BOUND))
    row_range = range(max(0, row-1), min(row+2, BOTTOM_BOUND))

    #Initialize count of unclean adjacent squares
    dirty_count = 0

    #Iterate through neighboring cells
    for r in row_range:
        for c in col_range:
            #exclude current cell
            if r != row or c != col:
                if (arr[r][c] == 1):
                    dirty_count += 1
    
    return dirty_count

#Print the boolean array of clean/dirty squares
def printCleaned():
    for row in range(5):
        for col in range(5):
            if (row == roomba_row) and (col == roomba_col):
                print("X", end=" ")
            else:
                if(arr[row][col] == 1):
                    print("D", end=" ")
                elif(arr[row][col] == 0):
                    print("C", end=" ")
                else:
                    print("W", end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Move functionality - move to (row, col)
def moveTo(row, col):
    global roomba_row, roomba_col
    roomba_row = row
    roomba_col = col
    clean()

#Clean square the roomba is on (switch boolean array from F -> T)
def clean():
    global roomba_col, roomba_row, arr
    arr[roomba_row][roomba_col] = 0

#Populate the initial distance array
def populateDistanceArray():
    global roomba_col, roomba_row, dis_arr
    for row in range(5):
        for col in range(5):
            dis_arr[row][col] = max(abs(roomba_col - col), abs(roomba_row - row))  #Radial Distance from starting square

#Print the radial distance of all cells relative to the starting position
def printDistance():
    for row in range(5):
        for col in range(5):
            print(dis_arr[row][col], end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Run main class
main()
