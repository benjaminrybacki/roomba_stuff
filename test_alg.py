#Method that returns path to front end
def getPath(array):
    #Make array globally accessable
    global arr
    arr = array

    #Retrieve size of array
    global ROWS, COLS
    ROWS = len(array)
    COLS = len(array[0])

    #Find origin based on input array
    global ORIGIN_ROW, ORIGIN_COL
    origin = findOrigin()
    ORIGIN_ROW = origin[0]
    ORIGIN_COL = origin[1]

    #Initialize roomba and clean origin
    global roomba_row, roomba_col
    roomba_row = ORIGIN_ROW
    roomba_col = ORIGIN_COL
    clean()

    #Initialize distance-from-origin array with zeros
    global dis_arr
    dis_arr = [[0 for i in range(COLS)] for j in range(ROWS)]
    populateDistanceArray()

    #Initalize path of roomba at origin
    global path
    path = [[ORIGIN_ROW, ORIGIN_COL]]

    #Run algorithm
    algorithm()

    #Show the overall path of the alg
    print(path)
    
#Algorithm to move the roomba until the room is cleaned
def algorithm():
    #Do bestAdjacent - if [-1, -1] is returned, find nearestDirty and go, otherwise if no dirty, go to start position
    for i in range(2*len(arr)*len(arr[0])): #In case of infinite loop, will automatically exit loop after a point
        next_move = bestAdjacent(roomba_row, roomba_col)
        if(next_move != [-1, -1]): #If there are adjacent dirty cells, pick best one and go to it
            moveTo(next_move[0], next_move[1])
        else: #If there are no adjacent dirty cells, scan array for nearest dirty cell
            nearest_dirty = nearestDirty()
            if(nearest_dirty != [-1, -1]): #If a dirty cell exists somewhere in the array, go to it
                path_to_node = goTo(nearest_dirty[0], nearest_dirty[1]) #Find path to dirty cell
                if(path_to_node != [-1, -1]):
                    for move in path_to_node:
                        moveTo(move[0], move[1])
                else:
                    break #If there is an unreachable dirty square, return to origin anyway

            else: #If there are no dirty cells in the array, go to origin
                break

        #Show step by step path of roomba as alg progresses
        printCleaned()

    #Once all the cells are cleaned
    goTo(ORIGIN_ROW, ORIGIN_COL)

#Return the nearest unclean square to the roomba at (roomba_row, roomba_col). Returns [-1, -1] if everything is clean
def nearestDirty():
    #Find all dirty nodes throughout the square
    all_dirty = []

    #Find closest cell and track its radial distance from current cell
    nearest_dirty = [-1, -1]
    dirty_distance = 1000

    #Find all dirty cells remaining
    for row in range(ROWS):
        for col in range(COLS):
            if arr[row][col] == 1:
                all_dirty.append([row, col])

    #For all dirty cells remaining, find the closest radially to the roomba
    for dirty in all_dirty:
        if(max(abs(roomba_row - dirty[0]),abs(roomba_col - dirty[1]))) < dirty_distance:
            dirty_distance = max(abs(roomba_row - dirty[0]),abs(roomba_col - dirty[1]))
            nearest_dirty = [dirty[0], dirty[1]]
        
    #Return closest dirty cell; if there were no dirty cells, returns [-1, -1]
    return nearest_dirty

#Return the path to a square (row,col) if everyting else is clean - can be starting spot or elsewere
def goTo(row, col):
    #Find path to goal node
    go_to_path = Calculate_Path([roomba_row, roomba_col], [row, col])
    
    #Make sequence of moves to go to goal node
    for move in go_to_path:
        moveTo(move[0], move[1])
    
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
    col_range = range(max(0, col-1), min(col+2, COLS))
    row_range = range(max(0, row-1), min(row+2, ROWS))

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
    col_range = range(max(0, col-1), min(col+2, COLS))
    row_range = range(max(0, row-1), min(row+2, ROWS))

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
    col_range = range(max(0, col-1), min(col+2, COLS))
    row_range = range(max(0, row-1), min(row+2, ROWS))

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
    for row in range(ROWS):
        for col in range(COLS):
            if (row == roomba_row) and (col == roomba_col):
                print("X", end=" ")
            elif (row == ORIGIN_ROW) and (col == ORIGIN_COL):
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
    for row in range(ROWS):
        for col in range(COLS):
            dis_arr[row][col] = max(abs(roomba_col - col), abs(roomba_row - row))  #Radial Distance from starting square

#Print the radial distance of all cells relative to the starting position
def printDistance():
    for row in range(ROWS):
        for col in range(COLS):
            if (arr[row][col] == -1):
                print("X", end=" ")
            else:
                print(dis_arr[row][col], end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

#Find roomba when array is first initialized
def findOrigin():
    #Iterate through neighboring cells
    for r in range(ROWS):
        for c in range(COLS):
            #If value is roomba value, that is origin
            if arr[r][c] == 2:
                return [r, c]
    
    return [-1, -1]

#John's code
# Define Class for Tree Structure
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) tuple to represent the position on the grid
        self.parent = parent
        self.children = []
        self.dist_to_end_pos = 2 ** 8
        self.dist_traveled = 0
        self.total_cost = 0

    def add_child(self, position):     
        child = Node(position, self)
        self.children.append(child)
        return child

def Calculate_Path(start_pos, end_pos):
    #
    # Description:
    # This function creates a tree structure from the 
    # array and uses A* search to find the best path from the starting 
    # position to the end position
    #
    # Parameters:
    #
    # start_pos - This parameter is a node that represents the starting 
    #             position in the array
    #
    # end_pos - This parameter is a node that represents end position 
    #           in the array
    #
    # arrRows - This parameter represents the # of rows in the array 
    #   
    # arrCols - This parameter represents the # of columns in the array
    #
    # Limitations:
    # Will return the starting node if the goal node is not found
    

    #Initialize data structures
    root = Node(start_pos)
    open_list = [root]
    closed_list = []
    openedNodes = 0
    # While Loop to process nodes
    while len(open_list) > 0:
        
        # Sort open by closest nodes
        open_list.sort(key=lambda node: node.total_cost)

        # Process new node
        current_node = open_list.pop(0) 
        openedNodes = openedNodes + 1 
        closed_list.append(current_node)

        # Find possible adjacent cells
        adj = adjacentCells(current_node.position[0], current_node.position[1])

        # Loop through adjacent cells
        for new_pos in adj:

            # Find & return path if goal position found
            if new_pos == end_pos:          
                # Create new child and then find path
                child = current_node.add_child(new_pos)
                child.parent = current_node
                path = path_to_parent(child)
                return path  

            # Determine if node has been previously processed
            previousNode, node_in_list = node_already_seen(new_pos, open_list, closed_list)

            #Create and add child to open list             
            if node_in_list == "Node not seen":

                    # Create new child
                    child = current_node.add_child(new_pos)
                    child.parent = current_node
                    
                    # Calculate Cost for A* search
                    child.dist_to_end_pos = distance_to_end_pos(new_pos, end_pos)
                    child.dist_traveled = child.parent.dist_traveled + 1
                    child.total_cost = child.dist_to_end_pos + child.dist_traveled

                    # Add child to open list
                    open_list.append(child)

            # Conditionally change cost and move to open
            if node_in_list == "open" or node_in_list == "closed":  
                
                # Compute new cost
                previousNode.dist_traveled = min( current_node.dist_traveled + 1, previousNode.dist_traveled)
                previous_total_cost = previousNode.total_cost
                previousNode.total_cost = previousNode.dist_to_end_pos + previousNode.dist_traveled

                # Move node back to open
                if node_in_list == "closed" and previousNode.total_cost < previous_total_cost :
                    open_list.append(previousNode)


    #Return original position if goal is not found
    return root.position

def path_to_parent(current_node):
    #
    # Description
    # This function finds a path from the current node (end position)
    # to the root node (start position)
    #
    # Parameters:
    #
    # currentNode - This parameter is node that represents the end 
    #               position in the tree
    #
    # Limitations: None

    #Initialize path
    reverse_path = []
    path = []

    #Add node to path until root node is reached - opposite order of travel
    while current_node:
        reverse_path.append(current_node.position)
        current_node = current_node.parent

    #The actual path is the reverse of the 
    path = reverse_path[::-1]

    #The first element is a duplicate
    path.pop(0)

    #Return path from current node desired node
    return path

def distance_to_end_pos(current_pos, end_pos):
    #
    # Description
    # This function calculates the distance between the current 
    # position and the end position.
    #
    # Parameters:
    #
    # current_pos - This parameter is current position in the array
    #
    # end_pos - This parameter is the final position in the array
    #
    # Limitations: None

    distance = max(abs(current_pos[0] - end_pos[0]), abs(current_pos[1] - end_pos[1]))

    return distance

def node_already_seen(new_pos, open_list, closed_list):
    #
    # Description
    # This function determines if the position is in the open
    # or closed list and returns the node/list to for cost/list 
    # updates
    #
    # Parameters:
    #
    # new_pos: This is the position in the array that is being checked
    #
    # open_list: This is the list of nodes that are currently open
    #
    # closed_list: This is the list of nodes that have been closed
    #
    # Limitations: None
    
    for node in closed_list:
        if new_pos == node.position:
            return node, "closed"


    for node in open_list:
        if new_pos == node.position:
            return node, "open"
          
    return None, "Node not seen"

testArray = [[1, 1, 1], [1, 2, 1], [1, 1, 1]]
getPath(testArray)

