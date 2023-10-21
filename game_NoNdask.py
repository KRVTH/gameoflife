import sys
import os.path
import random
import time
import numpy as np
import dask
import dask.array as da
from line_profiler import LineProfiler



def read_grid(input_path, data_type):
    
    with open(input_path) as f:
        
        h, w = map(int, f.readline().split())
        
        grid = np.zeros((h, w), dtype = data_type)

        for line in f:
            x, y = map(int, line.split())
            grid[x, y] = 1    

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
    generations = 1
    data_type = "int32"

    profile = LineProfiler()
    
    profile.add_function(save_grid)
    profile.add_function(tick)
    
    grid = read_grid(input_path, data_type)
    
    start_wall_time = time.time()
    start_cpu_time = time.process_time() 
    
    for i in range(generations):
        grid = tick(grid)

    end_wall_time = time.time()
    end_cpu_time = time.process_time()
    
    save_grid(grid, output_path)
    
    print(f"{end_cpu_time - start_cpu_time:.7f} seconds (CPU Time) elapsed for all {generations} generations.")
    print(f"{end_wall_time - start_wall_time:.7f} seconds (Wall Time) elapsed for all {generations} generations and saving.")

if __name__ == "__main__":
    main()
