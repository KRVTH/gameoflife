# Game of Life
This is an implementation of Conway's Game of Life

## Description

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead.

Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

* Any **live cell** with *fewer than two* live neighbours dies, as if by underpopulation.
* Any **live cell** with *two or three* live neighbours lives on to the next generation.
* Any **live cell** with *more than three* live neighbours dies, as if by overpopulation.
* Any **dead cell** with *exactly three* live neighbours becomes a live cell, as if by reproduction.

## Implementation
*Our script will have the input file name, output file name, and the number of generations as arguments.
*It will load the initial pattern of the grid from the input file.
*It will apply the rules for the number of generations
*It will store the final grid in the output file.

## RULES
* Grid will be read from a text file.
* The first line of the text file indicated the width and height of the grid, unsigned integers separated space.
* All other lines will indicate the position of the living cells. Each line will have the horizontal and vertical positions of a living cell.
    1. The position is based on zero-indexing w/ top left cell is 0 0
    2. Horizontal index increases from left to right
    3. Vertical index increases from top to bottom. 

## Running the Game of Life without Dask

For running the Game of Life without Dask, use the `game_NoNdask.py` script. Update the following parameters in the main function:

```python
input_path = "benchmark/1000x1000_0.1.txt"  # Path to your input file
output_path = "output_test1000x1000.txt"   # Path to save your output file
generations = 1  # Number of generations to simulate
data_type = "int32"  # Format of the board data
>

You just need to run it in the terminal by using Python:
>
>python game_NoNdask.py <br>
>

> For game_dask <br>
> input_path = "benchmark/1000x1000_0.1.txt" ##This is directory to your input file <br>
> output_path = "output_test1000x1000.txt"   ##This is the directory to save your output file <br>
> generations = 5 ##This is for the generation <br>
> chunksize = (100, 100) ##This is specify chunks <br>
> scheduler = "threads"  ##This is specify scheduler for DASK <br> 
> data_type = "int32"    ###This is to change the format of the board <br>
>

You just need to run it in the terminal by using Python:
>
>python game_NoNdask.py <br>
>pyton game_dask.py <br>
>












    
## Input/Output File

The example of the input file is provided in the input example folder. The input file consists of board size and indices of the living cells.

This code reads files like this:
>
>5 5   ##The first line is the size of the board <br>
>0 0   ##The rest are indices of the living cells on the board<br>
>2 1<br>
>2 2<br>
>3 2<br>
>3 4<br>
>

The outputs files will have similar format.