#Import Libraries
import test_alg

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

def Calculate_Path(start_pos, end_pos, arrRows, arrCols):
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
        adj = test_alg.adjacentCells(current_node.position[0], current_node.position[1])

        # Loop through adjacent cells
        for new_pos in adj:

            # Ensure only positions in array are returned
            if new_pos[0] > arrRows or new_pos[1] > arrCols:
                continue

            # Find & return path if goal position found
            if new_pos == end_pos:          
                path = path_to_parent(current_node)
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
    path = []

    #Add node to path until root node is reached
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent

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

# Testing
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [4,4], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [0,4], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [3,2], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [2,2], end_pos = [5,2], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
