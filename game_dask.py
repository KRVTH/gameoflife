import sys
import os.path
import random
import time  # check if this is needed later
import numpy as np
import dask
import dask.array as da


from dask.distributed import Client


from line_profiler import LineProfiler

def read_grid(input_path, chunksize, data_type):
    
    with open(input_path) as f:
        
        h, w = map(int, f.readline().split())
        # reads the first line with number or rows and columns
        
        grid = np.zeros((h, w), dtype = data_type )
        # using numpy fixed sized data types instead of python default int64 to construct the grid, less memory usage
        # da.zeros((h, w), chunks=(x, y)) # if it read it as a dask no point we have to compute it immediately to assign 1s

        for line in f:
            x, y = map(int, line.split())
            grid[x, y] = 1    
            # assigns 1 to desired cells, python counts rows and columns from 0

    
    #grid_da = da.from_array(grid, chunks=(chunksize[0], chunksize[1]))
    # convert numpy to dask array with chunks before return
    
    return grid

@profile
def save_grid(grid,output_path):
    with open (output_path, "w") as f:
        h, w = grid.shape
        f.write(f"{h} {w}\n")

        indices_1 = np.argwhere(grid == 1)
   
        for i in indices_1:
            f.write(f"{i[0]} {i[1]}\n")

@profile
def tick(grid_da):
    h, w = grid_da.shape

    temp = np.zeros_like(grid_da)
    
    neighbors = np.array([
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ], dtype='int8')
    
    for y, row in enumerate(grid_da):
        for x, cell in enumerate(row):
            
            count = 0
            
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                # if its neighbor doesn't go beyond the boundary and is alive 
                if 0 <= nx < w and 0 <= ny < h and grid_da[ny, nx]==1:
                    count += 1
                      
            if cell:
                cell = 1 if count >= 2 and count <=3 else 0
            else:
                cell = 1 if count == 3 else 0
            
            temp[y, x] = cell
            
            
    grid_da = temp
    return grid_da

def main():
    input_path = "benchmark/1000x1000_0.1.txt"
    output_path = "output_test1000x1000.txt"
    generations = 5
    chunksize = (100, 100)
    scheduler = "threads"
    data_type = "int32"
    
    grid = read_grid(input_path, chunksize, data_type)
    grid_da = da.from_array(grid, chunks=(chunksize[0], chunksize[1]))

    profile = LineProfiler()
    
    profile.add_function(save_grid)
    profile.add_function(tick)
    
    start_wall_time = time.time()
    start_cpu_time = time.process_time() 
    
    client = Client()
    
    for i in range(generations):
        grid_da = grid_da.map_overlap(tick, depth=1, boundary="none")

    
    grid = grid_da.compute(scheduler=scheduler)

    end_wall_time = time.time()
    end_cpu_time = time.process_time()
    
    save_grid(grid, output_path)
    client.shutdown()

    print(f"{end_cpu_time - start_cpu_time:.7f} seconds (CPU Time) elapsed for all {generations} generations.")
    print(f"{end_wall_time - start_wall_time:.7f} seconds (Wall Time) elapsed for all {generations} generations and saving.")


if __name__ == "__main__":
    main()
