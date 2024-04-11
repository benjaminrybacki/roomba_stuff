from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

# create a route to catch the grid that is posted
@app.route('/calculate_path', methods=['POST'])
def calculate_path():
  # get the grid from the post request
  json_grid = request.get_json()
  print(json_grid)
  # parse the grid out of the json
  grid = json_grid['grid']
  # TODO: show loading somehow  while we are waiting for the path to finish
  # calculate the path
  path = calculate_path(grid)
  return render_template('index.html', path=path)

# function to calculate path
def calculate_path(grid):
  path = []
  # TODO: Chance algorithm here
  return path

if __name__ == '__main__':
  app.run()