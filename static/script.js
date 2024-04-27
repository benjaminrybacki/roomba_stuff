gridBoxes = document.querySelectorAll('.grid-box');

// gridRows = document.querySelectorAll('.flex-row-container');
// buttonRows = document.querySelectorAll('.flex-row-container-button');

// addTopRow = buttonRows[0];
// addBottomRow = buttonRows[buttonRows.length - 1];

rowInput = document.getElementById('grid-rows');
colInput = document.getElementById('grid-cols');

// adding event listeners for walls for each grid box
gridBoxes.forEach((box) => {
  box.addEventListener('click', (e) => {
    if (!e.target.classList.contains('roomba'))
      e.target.classList.toggle('occupied');
  });

  box.addEventListener('mouseover', (e) => {
    if (e.buttons === 1 && !e.target.classList.contains('roomba')) {
      e.target.classList.toggle('occupied');
    }
  });
});

// add-left function to add a grid box to the left of the grid
// function addLeft(index) {
//   row = gridRows[index];
//   console.log(row.children.length)
//   // remove .left class from the first grid box in the row
//   row.children[1].classList.remove('left');

//   // add grid box to beginning of row (after the add-button)
//   let gridBox = document.createElement('div');
//   gridBox.classList.add('grid-box', 'left');
//   row.insertBefore(gridBox, row.children[1]);

//   // add new add-button to button row if it is in the first or last row
//   if (index == gridRows.length - 1) {
//     gridBox.classList.add('bottom'); // thicken bottom border
//     let addButton = document.createElement('button');
//     addButton.classList.add('add-box', 'add-bottom');
//     addButton.onclick = addBottom(0);
//     gridRows[index + 1].appendChild(addButton);
//   } else if (index == 0) {
//     gridBox.classList.add('top'); // thicken top border
//     let addButton = document.createElement('button');
//     addButton.classList.add('add-box', 'add-top');
//     addButton.onclick = addTop(0);
//     gridRows[index].appendChild(addButton);
//   }

//   // make sure button rows have the correct offset
//   calculatePaddingLeft();
//   calculateGridWidth();

//   if (row.children.length == 10) {
//     console.log(row.children[0])
//     row.children[0].disabled = true;
//   }
// }

// function addRight(index) {

// }

// function addBottom(index) {
//   // TODO: make sure to update gridRows variable with a new row!!
// }

// function addTop(index) {
//   // TODO: make sure to update gridRows variable with a new row!!
// }

// function getLongestRowLength() {
//   // calculate length of longest row
//   let longestRow = 0;
//   gridRows.forEach((row) => {
//     if (row.children.length > longestRow) {
//       longestRow = row.children.length;
//     }
//   });
//   return longestRow;
// }

// function calculatePaddingLeft() {
//   longestRow = getLongestRowLength();

//   // assign each row 60px * (longestRow - row.length) padding left
//   gridRows.forEach((row, index) => {
//     let padding = 60 * (longestRow - row.children.length);
//     console.log(padding, index)
//     row.style.paddingLeft = `${padding}px`;
//     // handle button rows
//     if(index == 0) {
//       // top button row should get padding equal to top row + 60px
//       buttonRows[index].style.paddingLeft = `${padding + 60}px`;
//     } else if (index == gridRows.length - 1) {
//       // bottom button row should get padding equal to bottom row + 60px
//       buttonRows[1].style.paddingLeft = `${padding + 60}px`;
//     }
//   });
// }

// function calculateGridWidth() {
//   longestRow = getLongestRowLength();
//   gridWidth = longestRow * 60;
//   document.documentElement.style.setProperty('--grid-width', `calc(${gridWidth}px + 6em)`);
// }


// a function that sends a 2d array representation of the grid to the flask server
function calculatePath() {
  // show loading spinner while waiting for response
  let spinner = document.querySelector('.loading-overlay');
  spinner.classList.remove('hidden');

  // disable the calculate path button
  let calculatePathButton = document.querySelector('.calculate');
  calculatePathButton.disabled = true;

  let grid = [];
  let gridRows = document.querySelectorAll('.flex-row-container');
  gridRows.forEach((row) => {
    let rowArray = [];
    let children = [...row.children];
    children.forEach((box) => {
      if (box.classList.contains('roomba')) {
        rowArray.push('2');
      } else if (box.classList.contains('occupied')) {
        rowArray.push('-1');
      } else {
        rowArray.push('1');
      }
    });
    grid.push(rowArray);
  });


  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ grid: grid })
  }).then(() => {
    spinner.classList.add('hidden');
    calculatePathButton.disabled = false;
    // get path
    fetch('/path', { method: "GET" }).then((response) => {
      response.json().then((data) => {
        console.log(data)
        let path = data['path'];
        console.log(path)

        path.forEach((coord, i) => {
          console.log(coord, i)
          let row = coord[0];
          let col = coord[1];
          let index = row * 5 + col;
          // add a delay for each box in the path
          setTimeout(() => {
            gridBoxes[index].classList.add('path');
          }, 200 * i);
        });
      });
    });
  });
}

// TODO: Fix the drag and drop functionality
// Make sure roomba can be dropped anywhere on the grid
// show roomba being dragged
let roomba = document.getElementById('roomba');
console.log(roomba)

roomba.addEventListener('dragstart', (e) => {
  e.preventDefault();
  console.log('dragging');
  roomba.classList.add('dragging');
});

roomba.addEventListener('drop', (e) => {
  e.preventDefault();
  console.log(e)
  if (e.target.classList.contains('grid-box')
    && !e.target.classList.contains('roomba')
    && !e.target.classList.contains('occupied')) {
    roomba.classList.remove('roomba');
    e.target.classList.add('roomba');
    roomba = e.target;
  }
});

function resizeGrid() {
  let rows = rowInput.value;
  let cols = colInput.value;

  if (rows < 1 || cols < 1 || rows > 10 || cols > 10) {
    document.querySelector('.error-message').classList.remove('hidden');
    return;
  } else {
    document.querySelector('.error-message').classList.add('hidden');
  }

  let squareSize = Math.max(rows, cols);

  // build out rows
  let grid = document.querySelector('.grid');
  grid.innerHTML = '';
  for (let i = 0; i < squareSize; i++) {
    let row = document.createElement('div');
    row.classList.add('flex-row-container');
    for (let j = 0; j < squareSize; j++) {
      let box = document.createElement('div');

      // adding event listeners for walls for each box
      box.addEventListener('click', (e) => {
        if (!e.target.classList.contains('roomba'))
          e.target.classList.toggle('occupied');
      });

      box.addEventListener('mouseover', (e) => {
        if (e.buttons === 1 && !e.target.classList.contains('roomba')) {
          e.target.classList.toggle('occupied');
        }
      });

      box.classList.add('grid-box');
      if (i == 0) {
        box.classList.add('top');
      }
      if (i == squareSize - 1) {
        box.classList.add('bottom');
      }
      if (j == 0) {
        box.classList.add('left');
      }
      if (j == squareSize - 1) {
        box.classList.add('right');
      }
      if (i == 0 && j == 0) {
        box.classList.add('roomba');
      }

      if (i > rows - 1 || j > cols - 1) {
        box.classList.add('occupied');
      }
      row.appendChild(box);
    }
    grid.appendChild(row);

    // adjust the box sizes so that they correspond to the ratio
    // 5x5 column = 60px squares, 10x10 column = 30px squares
    let boxSize = 300 / squareSize;
    let gridBoxes = document.querySelectorAll('.grid-box');
    gridBoxes.forEach((box) => {
      box.style.width = `${boxSize}px`;
      box.style.height = `${boxSize}px`;
    });
  }

}