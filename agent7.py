import numpy as np
import random

class Agent7():
    def __init__(self,dimensions):
        self.dim=dimensions
        self.generate_original_grid()
        self.start_cell,self.target_cell=self.set_start_and_target_cell()
        print("Start cell is" ,self.start_cell)
        print("target cell is" ,self.target_cell)
        self.terrain_fnr_dict={1:0.8,2:0.5,3:0.2}
        self.belief_matrix = np.full((self.dim, self.dim), 1/(self.dim**2))
        self.success_finding_matrix=np.full((self.dim, self.dim), 1/(self.dim**2))


    def generate_original_grid(self):
        self.original_grid = [[0 for i in range(self.dim)] for j in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                actual_prob = np.random.random_sample()  
                if actual_prob >= 0.3:                      
                    p = np.random.random_sample()
                    if p<=1/3:
                        self.original_grid[i][j]=1  #flat
                    elif p>1/3 and p<=2/3:
                        self.original_grid[i][j]=2   #hilly
                    else:
                        self.original_grid[i][j]=3   #forest                  
                else:
                    self.original_grid[i][j] = 0 #blocked
        
                    
        self.print_original_grid()
        
    def set_start_and_target_cell(self):
        x=0
        while x==0: #loop until find an unblocked cell to set the start cell
            start_yCoord = random.randrange(self.dim)
            start_xCoord = random.randrange(self.dim) 
            x=self.original_grid[start_xCoord][start_yCoord]
        start_cell=(start_xCoord,start_yCoord)
        y=0
        while y==0: #loop until find an unblocked cell to set the start cell
            target_yCoord = random.randrange(self.dim)
            target_xCoord = random.randrange(self.dim) 
            y=self.original_grid[target_xCoord][target_yCoord]
        target_cell=(target_xCoord,target_yCoord)
        return start_cell,target_cell
                
    def print_original_grid(self):
        for row in self.original_grid:
            for e in row:
                print(e, end=" ")
            print()

def get_fnr(a7obj,cell):
    grid_val=a7obj.original_grid[cell[0]][cell[1]]
    return a7obj.terrain_fnr_dict[grid_val]

def examine_current_cell(a7obj):

    current_cell=a7obj.start_cell
    if current_cell== a7obj.target_cell:
        p = random.uniform(0, 1)
        currentcell_fnr=get_fnr(a7obj,current_cell)
        if p>currentcell_fnr:
            print("Found the target and exiting")
            return 1 #exit
        else:
            return 2 #todo
    return 3 #couldm't find, decrease prob
    
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
        print("closest_cell_list",closest_cell_list)
        if len(closest_cell_list)>1:
            return random.choice(closest_cell_list)
    return listOfCoordinates



def main_a7():
    a7obj= Agent7(5)
    curr_cell=a7obj.start_cell
    if examine_current_cell(a7obj)==1:
        return
    elif examine_current_cell(a7obj)==3:
        a7obj.belief_matrix[a7obj.start_cell[0]][a7obj.start_cell[1]]*= get_fnr(a7obj,a7obj.start_cell)
        belief_sum = np.sum(a7obj.belief_matrix)
        a7obj.belief_matrix = a7obj.belief_matrix/belief_sum
        
        a7obj.success_finding_matrix[a7obj.start_cell[0]][a7obj.start_cell[1]]=a7obj.belief_matrix[a7obj.start_cell[0]][a7obj.start_cell[1]]*(1-get_fnr(a7obj,a7obj.start_cell))
        conf_sum = np.sum(a7obj.success_finding_matrix)
        a7obj.success_finding_matrix = a7obj.success_finding_matrix/conf_sum
    print(a7obj.belief_matrix)
    print(a7obj.success_finding_matrix)
    
    next_target_cell=get_max_probcell(curr_cell,a7obj.success_finding_matrix)
    print(next_target_cell)



main_a7()