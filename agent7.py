import numpy as np
import random

class Agent7():
    def __init__(self,dimensions):
        self.dim=dimensions
        self.generate_original_grid()
        self.start_cell,self.target_cell=self.set_start_and_target_cell()
        print("Start cell is" ,self.start_cell)
        print("target cell is" ,self.target_cell)
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

a= Agent7(8)