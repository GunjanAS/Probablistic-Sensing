import numpy as np
import random, agent2


def get_fnr(a67obj, cell):
    grid_val = a67obj.original_grid[cell[0]][cell[1]]
    return a67obj.terrain_fnr_dict[grid_val]


def examine_current_cell(curr_cell, a67obj):
    if curr_cell == a67obj.target_cell:
        p = random.uniform(0, 1)
        currentcell_fnr = get_fnr(a67obj, curr_cell)
        if p > currentcell_fnr:
            return True  # exit
    return False  # couldn't find, decrease prob


def get_closest_cells(curr_cell, listOfCoordinates):
    min_dist = float('inf')
    closest_cell_loc = []
    for cord in listOfCoordinates:
        dist = abs(cord[0]-curr_cell[0])+abs(cord[1]-curr_cell[1])
        if dist <= min_dist:
            min_dist = dist
            closest_cell_loc.append(cord)
    finalclosest_cell_loc = []
    for cellpos in closest_cell_loc:
        if abs(cellpos[0]-curr_cell[0])+abs(cellpos[1]-curr_cell[1]) == min_dist:
            finalclosest_cell_loc.append(cellpos)
    return finalclosest_cell_loc

def _update_belief_and_success(belief_matrix, success_finding_matrix, target, fnr, updateBelief = True):
    if (updateBelief):
        belief_matrix[target[0]][target[1]] *= fnr
        belief_sum = np.sum(belief_matrix)
        belief_matrix = belief_matrix/belief_sum
    success_finding_matrix[target[0]][target[1]] = belief_matrix[target[0]][target[1]] * (1 - fnr)
    conf_sum = np.sum(success_finding_matrix)
    success_finding_matrix = success_finding_matrix/conf_sum
    return belief_matrix, success_finding_matrix

def _get_max_probcells_helper(curr_cell, success_finding_matrix):
    maxval = np.max(success_finding_matrix)
    locations = np.where(success_finding_matrix == maxval)
    listOfCoordinates = list(zip(locations[0], locations[1]))
    return listOfCoordinates


def get_max_probcell(curr_cell, success_finding_matrix):
    listOfCoordinates = _get_max_probcells_helper(curr_cell, success_finding_matrix)

    if len(listOfCoordinates) > 1:
        listOfCoordinates = get_closest_cells(curr_cell, listOfCoordinates)
    if len(listOfCoordinates) > 1:
        return random.choice(listOfCoordinates)
    return listOfCoordinates[0]


def get_max_probcell_by_target(curr_cell, success_finding_matrix, target_cell):
    cells = _get_max_probcells_helper(curr_cell, success_finding_matrix)
    if (target_cell in cells):
        return target_cell
    return get_max_probcell(curr_cell, success_finding_matrix)


def current_target_not_reachable(target, current, a67obj, knowledge_grid, count):
    a67obj.belief_matrix, a67obj.success_finding_matrix = _update_belief_and_success(a67obj.belief_matrix, a67obj.success_finding_matrix,target, 0)
    next_target_cell = get_max_probcell(current, a67obj.success_finding_matrix)
    path, knowledge_grid = agent2.main(
        a67obj.dim, "No", a67obj.original_grid, knowledge_grid, current, next_target_cell)
    count += 1
    return path, next_target_cell, count

def get_threshold(curr_cell,success_finding_matrix):
    k=3
    topkelements=[]
    # Convert it into a 1D array
    a_1d = success_finding_matrix.flatten()
    # Find the indices in the 1D array
    idx_1d = a_1d.argsort()[-k:]
    # convert the idx_1d back into indices arrays for each dimension
    x_idx, y_idx = np.unravel_index(idx_1d, success_finding_matrix.shape)
    for x, y, in zip(x_idx, y_idx):
        if success_finding_matrix[x][y]!=0:
            topkelements.append(success_finding_matrix[x][y])
    return topkelements[0]


def main_a8(a67obj):
    knowledge_grid = [[1 for _ in range(a67obj.dim)]
                      for _ in range(a67obj.dim)]
    curr_cell = a67obj.start_cell
    examination = 0
    movements = 0
    count = 0
    while True:
        examination += 1
        ##examine the current cell
        if examine_current_cell(curr_cell, a67obj):
            actions = movements+examination
            print("Found Target!! EXITING GAME!!")
            return movements, examination, actions
        else:
            ##update the belief_matrix and success_finding_matrix
            a67obj.belief_matrix, a67obj.success_finding_matrix = _update_belief_and_success(a67obj.belief_matrix, a67obj.success_finding_matrix, curr_cell, get_fnr(a67obj, curr_cell))
        ##find maximum probability cell fromsuccess_finding_matrix
        next_target_cell = get_max_probcell(curr_cell, a67obj.success_finding_matrix)
        ##get current threshold value(which is the top kth element in the success_finding_matrix )
        threshold=get_threshold(curr_cell,a67obj.success_finding_matrix)
        ##get A* path from start to nect_target_goal
        path, knowledge_grid = agent2.main(a67obj.dim, "No", a67obj.original_grid, knowledge_grid, curr_cell, next_target_cell)
        while (len(path) == 0):
            ##re-plan if current target is not reachable
            path, next_target_cell, count = current_target_not_reachable(next_target_cell, curr_cell, a67obj, knowledge_grid, count)
        while True:
            flag = 0
            for i in path[::-1]:
                movements += 1
                if(a67obj.original_grid[i[0]][i[1]] == 0):
                    #bumped into a blocked cell, update the belief matrix and success_finding_matrix
                    knowledge_grid[i[0]][i[1]] = 0
                    a67obj.belief_matrix, a67obj.success_finding_matrix = _update_belief_and_success(a67obj.belief_matrix, a67obj.success_finding_matrix, (i[0], i[1]), 0)
                    flag = 1
                    new_start_position = path[path.index(i)+1][0], path[path.index(i)+1][1]
                    break
                elif (i[0], i[1]) == next_target_cell:
                    ##reached the next_target_cell, time to examine
                    flag = 2
                    break
                elif a67obj.original_grid[i[0]][i[1]] != 0:
                    ##while traversing, update the success_finding_matrix
                    new_start_position = path[path.index(i)][0], path[path.index(i)][1]
                    a67obj.belief_matrix, a67obj.success_finding_matrix = _update_belief_and_success(a67obj.belief_matrix, a67obj.success_finding_matrix, new_start_position, get_fnr(a67obj, new_start_position), False)
                    cell_for_replanning = get_max_probcell_by_target(new_start_position, a67obj.success_finding_matrix, next_target_cell)
                    ##check if target cell prob cell has changed or not, re-plan if it has changed
                    if cell_for_replanning != next_target_cell:
                        next_target_cell = cell_for_replanning
                        flag = 1
                        break
                    ## check if the current cell value is above or equal to threshold. If yes, examine the cell; else : continue
                    if(a67obj.success_finding_matrix[i[0]][i[1]]>= threshold):
                        next_target_cell=new_start_position
                        flag=2
                        break
            if flag == 1:
                 ##replan after bumped a blocked cell
                path, knowledge_grid = agent2.main(
                    a67obj.dim, "No", a67obj.original_grid, knowledge_grid, new_start_position, next_target_cell)
                while (len(path) == 0):
                    path, next_target_cell, count = current_target_not_reachable(
                        next_target_cell, curr_cell, a67obj, knowledge_grid, count)
            elif flag == 2:
                break
        curr_cell = next_target_cell
