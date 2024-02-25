from implementation import *
import picar_4wd as fc
import time
import precise_motion as pm
import mapping as map

def execute_commands(commands):
    for movement in commands:
        direction, times = movement
        update_car_direction(direction, times)

def load_matrix():
    matrix = GridWithWeights(100, 100)
    matrix.walls = []
    grid = map.generate_current_map()
    for i in range(0,100):
        for j in range(0,100):
            if(grid[i,j]==1):
                matrix.walls.append((j,i))

    draw_grid(matrix)
    return matrix

start, goal = (0, 50), (95,95)
current_direction = "RIGHT"

# def move_car(movements, start_node):
#     global start
#     new_direction = "RIGHT"
#     for movement in movements:
#         if movement != start_node:
#             if movement[0] == start_node[0]:
#                 if movement[1] > start_node[1]: # DOWN                    
#                     print("DOWN")
#                     new_direction = "DOWN"
#                     start = movement
#                 elif movement[1] < start_node[1]: # UP
#                     print("UP")
#                     new_direction = "UP"
#                     start = movement
#             elif movement[0] > start_node[0]: # RIGHT
#                 print("RIGHT")
#                 new_direction = "RIGHT"
#                 start = movement
#             elif movement[0] < start_node[0]: # LEFT
#                 print("LEFT")
#                 new_direction = "LEFT"
#                 start = movement
#             break

#     update_car_direction(new_direction)
    

# def update_car_direction(new_direction):
#     global current_direction
#     if current_direction == "UP":
#         if new_direction == "UP":
#             pass

#         elif new_direction == "RIGHT":
#             pm.turn_right()
#             current_direction = "RIGHT"

#         elif new_direction == "DOWN":
#             pm.turn_right()
#             pm.turn_right()
#             current_direction = "DOWN"

#         elif new_direction == "LEFT":
#             pm.turn_left()
#             current_direction = "LEFT"

#     elif current_direction == "RIGHT":
#         if new_direction == "UP":
#             pm.turn_left()
#             current_direction = "UP"

#         elif new_direction == "RIGHT":
#             pass

#         elif new_direction == "DOWN":
#             pm.turn_right()
#             current_direction = "DOWN"

#         elif new_direction == "LEFT":
#             pm.turn_left()
#             pm.turn_left()
#             current_direction = "LEFT"

#     elif current_direction == "DOWN":
#         if new_direction == "UP":
#             pm.turn_left()
#             pm.turn_left()
#             current_direction = "UP"

#         elif new_direction == "RIGHT":
#             pm.turn_left()
#             current_direction = "RIGHT"

#         elif new_direction == "DOWN":
#             pass

#         elif new_direction == "LEFT":
#             pm.turn_right()
#             current_direction = "LEFT"

#     elif current_direction == "LEFT":
#         if new_direction == "UP":
#             pm.turn_right()
#             current_direction = "UP"

#         elif new_direction == "RIGHT":
#             pm.turn_left()
#             pm.turn_left()
#             current_direction = "RIGHT"

#         elif new_direction == "DOWN":
#             pm.turn_left()
#             current_direction = "DOWN"

#         elif new_direction == "LEFT":
#             pass

#     pm.move_forward()
#     time.sleep(0.05)



def move_car_all(movements, start_node):
    previous_direction = "RIGHT"
    new_direction = "RIGHT"
    commands = []
    count = 0
    for movement in movements:
        if movement != start_node:
            if movement[0] == start_node[0]:
                if movement[1] > start_node[1]: # DOWN
                    new_direction = "DOWN"
                    start_node = movement
                elif movement[1] < start_node[1]: # UP
                    new_direction = "UP"
                    start_node = movement
            elif movement[0] > start_node[0]: # RIGHT
                new_direction = "RIGHT"
                start_node = movement
            elif movement[0] < start_node[0]: # LEFT
                new_direction = "LEFT"
                start_node = movement
            if new_direction == previous_direction:
                count += 1
            else:
                # Save the movements
                if count > 0:
                    commands.append((previous_direction, count))
                    count = 0
                previous_direction = new_direction
    if new_direction == previous_direction and count > 0:
        commands.append((previous_direction, count))
    for movement in commands:
        direction, times = movement
        update_car_direction(direction, times)



def update_car_direction(new_direction, times=1):
    global current_direction
    if current_direction == "UP":
        if new_direction == "UP":
            pass
        elif new_direction == "RIGHT":
            pm.turn_right()
            current_direction = "RIGHT"
        elif new_direction == "DOWN":
            pm.turn_right()
            pm.turn_right()
            current_direction = "DOWN"
        elif new_direction == "LEFT":
            pm.turn_left()
            current_direction = "LEFT"
    elif current_direction == "RIGHT":
        if new_direction == "UP":
            pm.turn_left()
            current_direction = "UP"
        elif new_direction == "RIGHT":
            pass
        elif new_direction == "DOWN":
            pm.turn_right()
            current_direction = "DOWN"
        elif new_direction == "LEFT":
            pm.turn_left()
            pm.turn_left()
            current_direction = "LEFT"
    elif current_direction == "DOWN":
        if new_direction == "UP":
            pm.turn_left()
            pm.turn_left()
            current_direction = "UP"
        elif new_direction == "RIGHT":
            pm.turn_left()
            current_direction = "RIGHT"
        elif new_direction == "DOWN":
            pass
        elif new_direction == "LEFT":
            pm.turn_right()
            current_direction = "LEFT"
    elif current_direction == "LEFT":
        if new_direction == "UP":
            pm.turn_right()
            current_direction = "UP"
        elif new_direction == "RIGHT":
            pm.turn_left()
            pm.turn_left()
            current_direction = "RIGHT"
        elif new_direction == "DOWN":
            pm.turn_left()
            current_direction = "DOWN"
        elif new_direction == "LEFT":
            pass
    pm.move_forward(times)
    time.sleep(0.05)
    print(current_direction,times)







matrix = load_matrix()
came_from, cost_so_far = a_star_search(matrix, start, goal)
path_1 = reconstruct_path(came_from, start=start, goal=goal)
print("Initial car position: " + str(start))
print(path_1)
draw_grid(matrix, path=path_1, start=start, goal=goal)  
# draw_grid(matrix)
move_car_all(path_1,start)




# while len(path) > 2: 
#     came_from, cost_so_far = a_star_search(matrix, start, goal)
#     path = reconstruct_path(came_from, start=start, goal=goal)    
#     move_car(path, start)
#     print("Current car position: " + str(start))
#     if start == goal:
#         print("Target Found !!!")
    
#    draw_grid(matrix, path)

