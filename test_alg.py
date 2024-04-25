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
    global roomba_x, roomba_y
    roomba_x = 2
    roomba_y = 2
    clean()

    #Populate Distance Array
    populateDistanceArray()

    #Show Radial Distance Array
    printDistance()

    #Show bool array start
    printCleaned()

    #Move around roomba
    moveRight()
    moveDownRight()

    #Show later cleaned
    printCleaned()

    print(adjacentCells(2, 2))
    print(adjacentCells(0, 0))
    print(adjacentCells(2, 0))

    

    
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

#Return the amount of dirty cells adjacent to a target cell
def dirtyAdjacent(row, col):
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
            if (row == roomba_y) and (col == roomba_x):
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

#Define all movement functionality
def moveRight():
    global roomba_x
    roomba_x += 1
    clean()

def moveLeft():
    global roomba_x
    roomba_x -= 1
    clean()

def moveUp():
    global roomba_y
    roomba_y -= 1
    clean()

def moveDown():
    global roomba_y
    roomba_y += 1
    clean()

def moveUpRight():
    global roomba_x, roomba_y
    roomba_x += 1
    roomba_y -= 1
    clean()

def moveUpLeft():
    global roomba_x, roomba_y
    roomba_x -= 1
    roomba_y -= 1
    clean()

def moveDownRight():
    global roomba_x, roomba_y
    roomba_x += 1
    roomba_y += 1
    clean()

def moveDownLeft():
    global roomba_x, roomba_y
    roomba_x -= 1
    roomba_y += 1
    clean()

#Clean square the roomba is on (switch boolean array from F -> T)
def clean():
    global roomba_x, roomba_y, arr
    arr[roomba_y][roomba_x] = 0

#Populate the initial distance array
def populateDistanceArray():
    global roomba_x, roomba_y, dis_arr
    for row in range(5):
        for col in range(5):
            dis_arr[row][col] = max(abs(roomba_x - col), abs(roomba_y - row))  #Radial Distance from starting square

#Print the radial distance of all cells relative to the starting position
def printDistance():
    for row in range(5):
        for col in range(5):
            print(dis_arr[row][col], end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Run main class
main()
