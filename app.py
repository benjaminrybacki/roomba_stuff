from flask import Flask, render_template, request, make_response
import time
import test_alg

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
  calculate_path(grid)
  return {"path": path}, 200

# function to calculate path
def calculate_path(grid):
  #Grid is in the form strings, convert to ints

  #Find size of grid
  rows = len(grid)
  cols = len(grid[0])

  #Make an int arry to represent grid
  array = [[0 for i in range(cols)] for j in range(rows)]

  #Populate array with intts
  for row in range(rows):
    for col in range(cols):
      array[row][col] = int(grid[row][col])

  #Call function to return path
  p = test_alg.getPath(array)
  print(p, "HERE IS THE PATH")

  global path
  path = p

  

@app.route('/path', methods=['GET'])
def get_path():
  # return the path as a json
  return {'path': path}

if __name__ == '__main__':
  app.run()
