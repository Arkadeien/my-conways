# my-conways

v0.1

Just a version of conways game of life using tkinter and PIL
I may come back a refactor the code later as this was the first attempt using both tk and PIL
But for right now it does what I need it to do.

v0.2

Changes:
-Removed usless comment from begining of code(Will add updated goals at end of v0.2 changes)
-Removed unsued imports
-Removed commented out code that will never be used
-Changed list comprehensions to nested loops for readablity
-new_grid function under Board class split into:
    +new_grid: which only returns a empty board now
    +new_random_grid: which will return a grid with cells that are randomly set True or False

Future: 
-Add file menu options to:
    +Create grids
    +Save current grid 
-Seperate Buttons and bindings from the window class so it can focus more on layout
-Add a label / status bar to show current info about the canvas.