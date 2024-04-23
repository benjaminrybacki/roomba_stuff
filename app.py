from flask import Flask, render_template, request, make_response
import time

app = Flask(__name__)

path = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def path():
  # get the grid from the post request
  json_grid = request.get_json()
  print(json_grid)
  # parse the grid out of the json
  grid = json_grid['grid']
  # calculate the path
  global path
  path = calculate_path(grid)
  return {"path": path}, 200

# function to calculate path
def calculate_path(grid):
  path = []
  # TODO: Chance algorithm here
  # for testing, simulate time delay
  time.sleep(3)
  # for testing, return fake path
  return [[4,4], [4,3], [4,2], [4,1], [4,0],
           [3,0], [2,0], [1,0], [0,0], [0, 1],
             [1,1], [2,1], [3,1], [3,2], [3,1],
               [2,1], [1,1], [1,2], [1,3], [0,3],
                 [0,4], [1,4], [2,4], [2, 3], [2,4], [3,4], [4,4]]
  # return path

@app.route('/path', methods=['GET'])
def get_path():
  # return the path as a json
  return {'path': path}

if __name__ == '__main__':
  app.run()

"""
#Main class to test code
def main():

    # Initialize Empty array with zeros
    global boolArr, disArr
    boolArr = [[False for i in range(5)] for j in range(5)]
    disArr = [[0 for i in range(5)] for j in range(5)]
    
    #Initialize roomba position and clean initial square
    global roombaX, roombaY
    roombaX = 2
    roombaY = 2
    Clean()

    #Populate Distance Array
    PopulateDistanceArray()

    #Show Manhattan Distance Array
    printDistance()

    #Show bool array start
    printCleaned()

    #Move roomba
    MoveRight()
    MoveDownRight()
    MoveLeft()

    #Show new roomba position
    printCleaned()


def printCleaned():
    for row in range(5):
        for col in range(5):
            if (row == roombaY) and (col == roombaX):
                print("X", end=" ")
            else:
                if(boolArr[row][col]):
                    print("T", end=" ")
                else:
                    print("F", end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

def printDistance():
    for row in range(5):
        for col in range(5):
            print(disArr[row][col], end=" ")
        print()  # New line between rows
    print()  # Empty line to separate multiple boxes

def MoveRight():
    global roombaX
    roombaX += 1
    Clean()

def MoveLeft():
    global roombaX
    roombaX -= 1
    Clean()

def MoveUp():
    global roombaY
    roombaY -= 1
    Clean()

def MoveDown():
    global roombaY
    roombaY += 1
    Clean()

def MoveUpRight():
    global roombaX, roombaY
    roombaX += 1
    roombaY -= 1
    Clean()

def MoveUpLeft():
    global roombaX, roombaY
    roombaX -= 1
    roombaY -= 1
    Clean()

def MoveDownRight():
    global roombaX, roombaY
    roombaX += 1
    roombaY += 1
    Clean()

def MoveDownLeft():
    global roombaX, roombaY
    roombaX -= 1
    roombaY += 1
    Clean()

def Clean():
    global roombaX, roombaY, boolArr
    boolArr[roombaY][roombaX] = True

def PopulateDistanceArray():
    global roombaX, roombaY, disArr
    for row in range(5):
        for col in range(5):
            disArr[row][col] = abs(roombaX - col) + abs(roombaY - row) #Manhattan Distance from starting square
    
def BeamSearch():
    print("start")

        

main()

"""