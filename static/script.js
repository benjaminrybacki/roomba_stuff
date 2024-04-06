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

