#Main class to test code
def main():

    #Primary array: -1 -> wall, 0 -> clean, 1 -> unclean
    global arr
    arr = [[1 for i in range(5)] for j in range(5)]

    #Initialize room size for cell checking
    global RIGHT_BOUND, BOTTOM_BOUND
    RIGHT_BOUND = len(arr[0])
    BOTTOM_BOUND = len(arr)
    
    #Initialize roomba position and clean initial square
    global roomba_row, roomba_col, start_row, start_col
    roomba_row, start_row = 2, 2
    roomba_col, start_col = 2, 2
    clean()

    #Initialize distance-from-origin array with zeros
    global dis_arr
    dis_arr = [[0 for i in range(5)] for j in range(5)]
    populateDistanceArray()

    #Initalize path of roomba
    global path
    path = []
    #testPath = [[3,2],[4,2]]

    #Show array start
    printCleaned()

    #Run algorithm
    algorithm(start_row, start_col)

    #Move roomba along path
    #for move in testPath:
        #moveTo(move[0], move[1])

    #Show cleaned after movement
    #printCleaned()

    print(path)
    
#Algorithm to move the roomba until the room is cleaned
def algorithm(start_row, start_col):
    #Do bestAdjacent - if [-1, -1] is returned, find nearestDirty and go, otherwise if no dirty, go to start position
    for i in range(23):
        next_move = bestAdjacent(roomba_row, roomba_col)
        if(next_move != [-1, -1]): #If there are adjacent dirty cells, pick best one and go to it
            moveTo(next_move[0], next_move[1])
        else: #If there are no adjacent dirty cells, scan array for nearest dirty cell
            nearest_dirty = nearestDirty()
            if(nearest_dirty != [-1, -1]): #If a dirty cell exists somewhere in the array, go to it
                goTo(nearest_dirty[0], nearest_dirty[1])
            else: #If there are no dirty cells in the array, go to origin
                goTo(start_row, start_col)
        printCleaned()


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
    #Find all adjacent dirty cells
    options = adjacentDirty(row, col)

    #If their are no dirty neighbors, return [-1, -1]
    if len(options) == 0:
        return[-1, -1]

    #Initalize best node at 9 dirty edges
    min_dirty_edges = 9

    #Initalize variable to hold next move
    best_adjacent = []

    #Iterate through options to find best move
    for option in options:
        dirty_edges = adjacentDirtyCount(option[0], option[1])
        if (dirty_edges < min_dirty_edges):
            #If option is better, reset max dirty edges value and store next move
            min_dirty_edges = dirty_edges
            best_adjacent = option
        elif (dirty_edges == min_dirty_edges):
            #If equal adjacent dirty edges, take choice farther from origin
            if( dis_arr[option[0]][option[1]] > dis_arr[best_adjacent[0]][best_adjacent[1]] ):
                best_adjacent = option
            


    #Return the best option as a single path
    return best_adjacent
    
#Return a list of lists of all adjacent cells to the cell at [row, col]
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

#Return a list of lists of all adjacent and dirty cells to the cell at [row, col]
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

#Return the amount of dirty cells adjacent to the cell at [row, col]
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
            elif (row == start_row) and (col == start_col):
                print("O",end=" ")
            else:
                if(arr[row][col] == 1):
                    print("D", end=" ")
                elif(arr[row][col] == 0):
                    print("C", end=" ")
                else:
                    print("W", end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Move functionality - move to (row, col) and add path to global path
def moveTo(row, col):
    global roomba_row, roomba_col, path
    roomba_row = row
    roomba_col = col
    clean()
    path.append([row, col])

#Clean square the roomba is on (set cell value to 0)
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
            if (arr[row][col] == -1):
                print("X", end=" ")
            else:
                print(dis_arr[row][col], end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Run main class
main()
