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




def get_max_probcell(curr_cell,success_finding_matrix):
    maxval=np.max(success_finding_matrix)
    locations=np.where(success_finding_matrix==maxval)
    listOfCoordinates= list(zip(locations[0], locations[1]))
    if len(listOfCoordinates)>1:
        closest_cell_list=get_closest_cell(curr_cell,listOfCoordinates)
        # print("closest_cell_list",closest_cell_list)
        if len(closest_cell_list)>1:
            return random.choice(closest_cell_list)
        
        return closest_cell_list[0]
    return listOfCoordinates[0]

def current_target_not_reachable(target,current,a67obj,knowledge_grid,count):
    a67obj.belief_matrix[target[0]][target[1]]=0
    belief_sum = np.sum(a67obj.belief_matrix)
    a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
    a67obj.success_finding_matrix[target[0]][target[1]]=0
    conf_sum = np.sum(a67obj.success_finding_matrix)
    a67obj.success_finding_matrix = a67obj.success_finding_matrix/conf_sum
    next_target_cell=get_max_probcell(current,a67obj.success_finding_matrix)
    path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,current,next_target_cell)
    count+=1
    return path,next_target_cell,count

def get_threshold(curr_cell,success_finding_matrix):
    k=5
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
    #check if the grid is solvable
    knowledge_grid = [[1 for _ in range(a67obj.dim)] for _ in range(a67obj.dim)]
    #while loop
    curr_cell=a67obj.start_cell
    examination=0
    movements=0
    count=0
    while True:
        examination+=1
        if examine_current_cell(curr_cell,a67obj):
            print("Total number of actions for agent 8 are ",movements+examination)
            # print("Repeated A* for agent 8 is called ",count, "times")
            # print("Found Target!! EXITING GAME!!")
            actions=movements+examination
            return movements,examination,actions
        else:
            
            a67obj.belief_matrix[curr_cell[0]][curr_cell[1]]*= get_fnr(a67obj,curr_cell)
            belief_sum = np.sum(a67obj.belief_matrix)
            a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
            a67obj.success_finding_matrix[curr_cell[0]][curr_cell[1]]=a67obj.belief_matrix[curr_cell[0]][curr_cell[1]]*(1-get_fnr(a67obj,curr_cell))
            conf_sum = np.sum(a67obj.success_finding_matrix)
            a67obj.success_finding_matrix = a67obj.success_finding_matrix/conf_sum
            
        next_target_cell=get_max_probcell(curr_cell,a67obj.success_finding_matrix)
        #find threshold
        threshold=get_threshold(curr_cell,a67obj.success_finding_matrix)
        # print("My next target cell is ",next_target_cell)
        # print("curr_cell",curr_cell)
        count+=1
        # print("a67obj.belief_matrix",a67obj.belief_matrix)
        # print("a67obj.belief_matrix",a67obj.belief_matrix)
        path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,curr_cell,next_target_cell)
        # print("my path here in 131 ", path)
        while (len(path)==0):
            path,next_target_cell,count=current_target_not_reachable(next_target_cell,curr_cell,a67obj,knowledge_grid,count)
        while True:
            flag=0
            for i in path[::-1]:
                movements+=1
                # print("I am walking on cell ",(i[0],i[1]))
                if(a67obj.original_grid[i[0]][i[1]] == 0): #bumped into a blocked cell
                    knowledge_grid[i[0]][i[1]] = 0
                    # print("faced block")
                    # print("updayes")
                    a67obj.belief_matrix[i[0]][i[1]]=0

                    belief_sum = np.sum(a67obj.belief_matrix)
                    a67obj.belief_matrix = a67obj.belief_matrix/belief_sum
                    flag=1
                    new_start_position = path[path.index(i)+1][0], path[path.index(i)+1][1]
                    next_target_cell=get_max_probcell(new_start_position,a67obj.belief_matrix)
                    a67obj.success_finding_matrix[i[0]][i[1]]=0
                    conf_sum = np.sum(a67obj.success_finding_matrix)
                    a67obj.success_finding_matrix = a67obj.success_finding_matrix/conf_sum
                    # print("My new pos after bumpong to a blocked cell ",new_start_position)
                    break
                elif (i[0],i[1])==next_target_cell:
                    flag=2
                    break
                elif (a67obj.original_grid[i[0]][i[1]] != 0):
                    a67obj.success_finding_matrix[i[0]][i[1]]=a67obj.belief_matrix[i[0]][i[1]]*(1-get_fnr(a67obj,(i[0],i[1])))
                    conf_sum = np.sum(a67obj.success_finding_matrix)
                    a67obj.success_finding_matrix = a67obj.success_finding_matrix/conf_sum
                    if(a67obj.success_finding_matrix[i[0]][i[1]]>= threshold):
                        next_target_cell=(i[0],i[1])
                        flag=2
                        break
                ##check if the cell's prob is greater than threshold

            if flag==1:
                #replanning
                # print("new start pos", new_start_position)
                # print("End targer for now", next_target_cell)
                path,knowledge_grid=agent2.main(a67obj.dim,"No",a67obj.original_grid,knowledge_grid,new_start_position,next_target_cell)
                # print("path",path)
                #cant reach my tagerget cell
                while (len(path)==0):
                    # print("len(path)",len(path))
                    path,next_target_cell,count=current_target_not_reachable(next_target_cell,curr_cell,a67obj,knowledge_grid,count)
                    
            elif flag==2:
                break
        curr_cell=next_target_cell
        

    #run A* get path and execute
    #if one of the cell encountered is block- change probab

    # print(next_target_cell)



