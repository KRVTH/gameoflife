import sys
import os.path
import random
import time
import numpy as np
import dask
import dask.array as da



from dask.distributed import Client



def read_grid(input_path, chunksize, data_type):
    
    with open(input_path) as f:
        
        h, w = map(int, f.readline().split())
        
        grid = np.zeros((h, w), dtype = data_type )

        for line in f:
            x, y = map(int, line.split())
            grid[x, y] = 1    
  
    return grid

def save_grid(grid_da,output_path, scheduler):
    with open (output_path, "w") as f:
        h, w = grid_da.shape
        f.write(f"{h} {w}\n")
        indices_1 = np.argwhere(grid_da == 1)
        indices_1 = indices_1.compute(scheduler = scheduler)

        for i in indices_1:
            f.write(f"{i[0]} {i[1]}\n")

def count_neighbors(grid_da):
    h, w = grid_da.shape
    neighbor_count = np.zeros_like(grid_da, dtype='int32')
    
    for y in range(h):
        for x in range(w):
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue 
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        count += grid_da[ny, nx]
            neighbor_count[y, x] = count

    return neighbor_count


def tick(grid_da):

    neighbor_count = count_neighbors(grid_da)

    new_grid = (
        (grid_da == 1) & ((neighbor_count == 2) | (neighbor_count == 3)) |
        (grid_da == 0) & (neighbor_count == 3)
    )
    
    return new_grid


def main():
    input_path = "benchmark/10000x10000_0.2.txt"
    output_path = "output_t10000x10000.txt"
    generations = 1
    chunksize = (100, 100)
    scheduler = "distributeds"
    data_type = "int32"

    new_grid = read_grid(input_path, chunksize, data_type)
    grid_da = da.from_array(new_grid, chunks=(chunksize[0], chunksize[1]))
    
    start_wall_time = time.time()
    start_cpu_time = time.process_time() 
    
    client = Client()
    
    for i in range(generations):
        grid_da = grid_da.map_overlap(tick, depth=1, boundary="none")

    
    save_grid(grid_da, output_path, scheduler)
    client.shutdown()

    end_cpu_time = time.process_time()
    end_wall_time = time.time()
    
    print(f"{end_cpu_time - start_cpu_time:.7f} seconds (CPU Time) elapsed for all {generations} generations.")
    print(f"{end_wall_time - start_wall_time:.7f} seconds (Wall Time) elapsed for all {generations} generations and saving.")


if __name__ == "__main__":
    main()
