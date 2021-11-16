import numpy as np
import random,agent2



def get_fnr(a67obj,cell):
    grid_val=a67obj.original_grid[cell[0]][cell[1]]
    return a67obj.terrain_fnr_dict[grid_val]

def examine_current_cell(curr_cell,a67obj):
    if curr_cell== a67obj.target_cell:
        p = random.uniform(0, 1)
        currentcell_fnr=get_fnr(a67obj,curr_cell)
        if p>currentcell_fnr:
            return True #exit
    return False #couldm't find, decrease prob
    
def get_closest_cell(curr_cell,listOfCoordinates) :
    min_dist=float('inf')
    closest_cell_loc=[]
    for cord in listOfCoordinates:
        dist=abs(cord[0]-curr_cell[0])+abs(cord[1]-curr_cell[1])
        if dist<=min_dist:
            min_dist=dist
            closest_cell_loc.append(cord)
    finalclosest_cell_loc=[] 
    for cellpos in closest_cell_loc:
        if abs(cellpos[0]-curr_cell[0])+abs(cellpos[1]-curr_cell[1])==min_dist:
            finalclosest_cell_loc.append(cellpos)
    return finalclosest_cell_loc




def get_max_probcell(curr_cell,belief_matrix):
    maxval=np.max(belief_matrix)
    locations=np.where(belief_matrix==maxval)
    listOfCoordinates= list(zip(locations[0], locations[1]))
    if len(listOfCoordinates)>1:
        closest_cell_list=get_closest_cell(curr_cell,listOfCoordinates)
        if len(closest_cell_list)>1:
            return random.choice(closest_cell_list)
        return closest_cell_list[0]
    return listOfCoordinates[0]

def current_target_not_reachable(target,current,a67obj,knowledge_grid,count):
    a67obj.belief_matrix[target[0]][target[1]]=0
    belief_sum = np.sum(a67obj.belief_matrix)
    a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
    next_target_cell=get_max_probcell(current,a67obj.belief_matrix)
    count+=1
    path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,current,next_target_cell)
    return path,next_target_cell,count

def main_a6(a67obj):
    count=0
    movements=0
    examinations=0
    knowledge_grid = [[1 for _ in range(a67obj.dim)] for _ in range(a67obj.dim)]
    curr_cell=a67obj.start_cell
    while True:
        examinations+=1
        ##examine the current cell
        if examine_current_cell(curr_cell,a67obj):
            print("Found Target!! EXITING GAME!!")
            actions=movements+examinations
            return movements,examinations,actions
        else:
            ##update the belief_matrix
            a67obj.belief_matrix[curr_cell[0]][curr_cell[1]]*= get_fnr(a67obj,curr_cell)
            belief_sum = np.sum(a67obj.belief_matrix)
            a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
        ##find maximum probability cell from belief_matrix
        next_target_cell=get_max_probcell(curr_cell,a67obj.belief_matrix)
        ##get A* path from start to nect_target_goal
        path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,curr_cell,next_target_cell)
        ##re-plan if current target is not reachable
        while (len(path)==0):
            path,next_target_cell,count=current_target_not_reachable(next_target_cell,curr_cell,a67obj,knowledge_grid,count)
        while True:
            flag=0
            ##execute the path
            for i in path[::-1]:
                movements+=1
                if(a67obj.original_grid[i[0]][i[1]] == 0): #bumped into a blocked cell, update the belief matrix
                    knowledge_grid[i[0]][i[1]] = 0
                    a67obj.belief_matrix[i[0]][i[1]]=0
                    belief_sum = np.sum(a67obj.belief_matrix)
                    a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
                    flag=1
                    new_start_position = path[path.index(i)+1][0], path[path.index(i)+1][1]
                    break
                elif (i[0],i[1])==next_target_cell:
                    ##reached the next_target_cell, time to examine
                    flag=2
                    break
            if flag==1:
                ##replan after bumped a blocked cell
                path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,new_start_position,next_target_cell)
                while (len(path)==0):
                    path,next_target_cell,count=current_target_not_reachable(next_target_cell,curr_cell,a67obj,knowledge_grid,count)
            elif flag==2:
                break
        curr_cell=next_target_cell