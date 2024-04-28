#Import Libraries
import test_alg

# Define Class for Tree Structure
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) tuple to represent the position on the grid
        self.parent = parent
        self.children = []

    def add_child(self, position):     
        child = Node(position, self)
        self.children.append(child)
        return child

def Calculate_Path(start_pos, end_pos, arrRows, arrCols):
    #
    # Description:
    # This function creates and processes a tree structure from the 
    # array to find the path from the starting position to the end 
    # position
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
    open = [root]
    closed_pos = []
      
    # While Loop to process nodes
    while len(open) > 0:
        
        # Process new node
        current_node = open.pop(0)
        closed_pos.append(current_node.position)

        # Find possible adjacent cells
        adj = test_alg.adjacentCells(current_node.position[0], current_node.position[1])

        # Loop through adjacent cells
        for new_pos in adj:

            # Ensure only positions in array are returned
            if new_pos[0] > arrRows or new_pos[1] > arrCols:
                continue
            
            # Add child if it hasn't been processed yet
            if new_pos not in closed_pos and \
                all(new_pos != node.position for node in open):

                # Find & return path if goal position found
                if new_pos == end_pos:          
                    path = path_to_parent(current_node)
                    return path  

                # Otherwise, create and add child to open list
                else:
                    child = current_node.add_child(new_pos)
                    child.parent = current_node
                    open.append(child)
    
    #Return original position if goal is not found
    return root.position

def path_to_parent(currentNode):
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
    while currentNode:
        path.append(currentNode.position)
        currentNode = currentNode.parent

    #Return path from current node desired node
    return path


# Testing
start_position = [0, 0]
end_position = [4,4]
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [4,4], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [0,4], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [0,0], end_pos = [3,2], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
path_to_node = Calculate_Path(start_pos = [2,2], end_pos = [5,2], arrRows=5, arrCols=5)
print("path_to_node: " + str(path_to_node))
