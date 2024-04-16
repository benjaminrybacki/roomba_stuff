gridBoxes = document.querySelectorAll('.grid-box');

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

// a function that sends a 2d array representation of the grid to the flask server
function calculatePath() {
  // show loading spinner while waiting for response
  let spinner = document.querySelector('.loading-overlay');
  spinner.classList.remove('hidden');

  // disable the calculate path button
  let calculatePathButton = document.querySelector('.calculate');
  calculatePathButton.disabled = true;

  let grid = [];
  let row = [];
  let gridBoxes = document.querySelectorAll('.grid-box');
  let index = 0;
  gridBoxes.forEach((box) => {
    box.classList.remove('path');
      if (box.classList.contains('roomba')) {
        row.push(2);
      } else if (box.classList.contains('occupied')) {
        row.push(1);
      } else {
        row.push(0);
      }
      index++;
      
      if(index == 5) {
        grid.push(row);
        row = [];
        index = 0;
      }
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
    fetch('/path', {method: "GET"}).then((response) => {
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