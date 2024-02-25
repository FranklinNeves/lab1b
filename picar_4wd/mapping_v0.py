import picar_4wd as fc
import numpy as np
import math
import time
import sys

sys.setrecursionlimit(5000)
grid_size = 100
grid = np.zeros((grid_size, grid_size))
car_x, car_y = 50, 0
x_pad = 9   # object width
y_pad = 5       # how close the object is detected
x_pad_ub = 9 # object width
y_pad_ub = 33   # how deep   

def make_rectangles(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def fill_rectangle(min_row, max_row, min_col, max_col):
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                grid[r][c] = 1
    
    def dfs(row, col, bounds):
        if row < 0 or col < 0 or row >= rows or col >= cols or grid[row][col] == 0 or visited[row][col]:
            return
        visited[row][col] = True
        bounds[0] = min(bounds[0], row)  # min_row
        bounds[1] = max(bounds[1], row)  # max_row
        bounds[2] = min(bounds[2], col)  # min_col
        bounds[3] = max(bounds[3], col)  # max_col
        dfs(row + 1, col, bounds)
        dfs(row - 1, col, bounds)
        dfs(row, col + 1, bounds)
        dfs(row, col - 1, bounds)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                bounds = [r, r, c, c]  # min_row, max_row, min_col, max_col
                dfs(r, c, bounds)
                fill_rectangle(*bounds)
    
    return grid


def polar_to_cartesian(angle, distance):
    radians = math.radians(-angle)
    x = distance * math.sin(radians)
    y = distance * math.cos(radians)
    return int(x + car_x), int(y + car_y)

def mark_obstacle_and_adjacent(x, y):
    for adj_x in range(x-x_pad, x+x_pad_ub+1):
        for adj_y in range(y-y_pad, y+y_pad_ub+1):
            if 0 <= adj_x < grid_size and 0 <= adj_y < grid_size:
                grid[adj_x, adj_y] = 1
                # print(adj_x,adj_y)
                

def generate_current_map():
    grid = np.zeros((grid_size, grid_size))                 #grid is cleared each time generate_current_map is called
    distance_measurements = []
    for angle in range(-90,91,10):
        distance = fc.get_distance_at(angle)
        distance_measurements.append((angle, distance))
        time.sleep(2)
    print(distance_measurements)
    obj_detected_at_prev_angle = False
    prev_obj_x = 0
    prev_obj_y = 0
    for i in range(0,len(distance_measurements)):
        if distance_measurements[i][1]== -1 or distance_measurements[i][1]== -2:
            obj_detected_at_prev_angle = False
            continue
        obst_x, obst_y = polar_to_cartesian(distance_measurements[i][0],distance_measurements[i][1])
        # print("Angle Distance:", distance_measurements[i])
        # print("x,y" ,obst_x, obst_y)
        # print("prev obst", obj_detected_at_prev_angle)
        if(0<= obst_x <grid_size and 0 <= obst_y < grid_size):
            if obj_detected_at_prev_angle == False:             # if object was not detected at previous angle        
                mark_obstacle_and_adjacent(obst_x,obst_y)
                obj_detected_at_prev_angle = True
                prev_obj_x = obst_x
                prev_obj_y = obst_y
            else:
                if(np.abs(distance_measurements[i][1]-distance_measurements[i-1][1])<=70):  
                    for block_x in range(max(0,min(prev_obj_x, obst_x)-x_pad), min(grid_size+1, max(prev_obj_x, obst_x) + x_pad_ub + 1)):
                        for block_y in range(max(0,min(prev_obj_y, obst_y)-y_pad), min(grid_size +1 ,max(prev_obj_y, obst_y) + y_pad_ub + 1)):
                            if 0 <= block_x < grid_size and 0 <= block_y < grid_size:
                                grid[block_x, block_y] = 1
                                # print(block_x,block_y)
                else:
                    mark_obstacle_and_adjacent(obst_x,obst_y)
                obj_detected_at_prev_angle = True               #if obstacle was detected at previous cell as well, then mark block of cells with corner cells as previous obstacle and currrent obstacle as 1s
                prev_obj_x = obst_x
                prev_obj_y = obst_y

    # for i in range(0,grid_size):
    #     for j in range(0,grid_size):
    #         if            


    # for row in grid:
    #     print(" ".join(str(int(cell)) for cell in row))
    grid = make_rectangles(grid)

    for row in grid:
        print(" ".join(str(int(cell)) for cell in row))
    return grid





if __name__ == "__main__":
    # print("First map")
    obstacle_map = generate_current_map()
    obstacle_map[50,0] = 9
    for row in obstacle_map:
        print(" ".join(str(int(cell)) for cell in row))
