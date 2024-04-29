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
  # time.sleep(3)
  # for testing, return fake path
  return [[4,4], [3,3], [2,2], [3,1], [4,2], [3,3], [4,3], [4,2], [4,1], [4,0],
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
