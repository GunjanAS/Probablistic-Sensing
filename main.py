import agent6,agent7,agent8,random,astar,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class agent6and7():
    def __init__(self,dimensions,terrain):
        self.dim=dimensions
        self.generate_original_grid()
        self.terrain_fnr_dict={1:0.2,2:0.5,3:0.8}
        self.terrain_type_dict={1:"Flat",2:"Hilly",3:"Forest"}
        self.start_cell,self.target_cell=self.set_start_and_target_cell(terrain)
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
        
                    
        # self.print_original_grid()
        
    def set_start_and_target_cell(self,terrain):
        x=0
        while x==0: #loop until find an unblocked cell to set the start cell
            start_yCoord = random.randrange(self.dim)
            start_xCoord = random.randrange(self.dim) 
            x=self.original_grid[start_xCoord][start_yCoord]
        start_cell=(start_xCoord,start_yCoord)
        y=0
        while y==0: #loop until find an unblocked cell to set the target cell
            target_yCoord = random.randrange(self.dim)
            target_xCoord = random.randrange(self.dim) 
            y=self.original_grid[target_xCoord][target_yCoord]
        target_cell=(target_xCoord,target_yCoord)
        
        target_terrain_type=self.terrain_type_dict[self.original_grid[target_cell[0]][target_cell[1]]]

        while target_terrain_type!= self.terrain_type_dict[terrain]:
            y=0

            while y==0: #loop until find an unblocked cell to set the target cell
                target_yCoord = random.randrange(self.dim)
                target_xCoord = random.randrange(self.dim) 
                y=self.original_grid[target_xCoord][target_yCoord]
            target_cell=(target_xCoord,target_yCoord)
            target_terrain_type=self.terrain_type_dict[self.original_grid[target_cell[0]][target_cell[1]]]

        

        return start_cell,target_cell
                
    def print_original_grid(self):
        for row in self.original_grid:
            for e in row:
                print(e, end=" ")
            print()
dim=50
loops=[3, 25]
final_result=np.zeros((loops[0] + loops[1],6))

while loops[0] > 0:
    loops[0]-=1
    loops[1] = 25
    while True:
        a67obj = agent6and7(dim, loops[0] + 1)
        result,path=astar.main(a67obj.original_grid,a67obj.dim,a67obj.start_cell,a67obj.target_cell)
        if result=="Solvable":
            break

    while loops[1] > 0:
        loops[1]-=1

        print("Loop: ",loops)
        
        target_terrain_type=a67obj.terrain_type_dict[a67obj.original_grid[a67obj.target_cell[0]][a67obj.target_cell[1]]]


        print("Target terrain type is ",target_terrain_type)
        a67obj.belief_matrix = np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        a67obj.success_finding_matrix=np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        start_a6 = time.time()
        movements6,examinations6,actions6=agent6.main_a6(a67obj)
        print("movements6",movements6)
        print("examinations6",examinations6)
        end_a6= time.time()
        ##Resetiing matrices
        a67obj.belief_matrix = np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        a67obj.success_finding_matrix=np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        start_a7 = time.time()
        movements7,examinations7,actions7=agent7.main_a7(a67obj)
        print("movement76",movements7)
        print("examinations7",examinations7)
        end_a7 = time.time()
        a67obj.belief_matrix = np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        a67obj.success_finding_matrix=np.full((a67obj.dim, a67obj.dim), 1/(a67obj.dim**2))
        start_a8 = time.time()
        movements8,examinations8,actions8=agent8.main_a8(a67obj)
        end_a8 = time.time()
        print("movements8",movements8)
        print("examinations8",examinations8)
        final_result=np.append(final_result,[["Agent 6",target_terrain_type,int(movements6),int(examinations6),int(actions6), int(end_a6 - start_a6) ]],axis=0)
        final_result=np.append(final_result,[["Agent 7",target_terrain_type,int(movements7),int(examinations7),int(actions7),int(end_a6 - start_a6) ]],axis=0)
        final_result=np.append(final_result,[["Agent 8",target_terrain_type,int(movements8),int(examinations8),int(actions8),int(end_a6 - start_a6) ]],axis=0)

        

df = pd.DataFrame(final_result, 
             columns=['Agent Type', 'Terrain Type', 'Movements', 'Examinations', 'Actions','Time Taken'])
df_actions_a6=df.loc[df['Agent Type'] == "Agent 6"]
mean_a6_actions=df_actions_a6['Actions'].astype(int).mean()
df_actions_a7=df.loc[df['Agent Type'] == "Agent 7"]
mean_a7_actions=df_actions_a7['Actions'].astype(int).mean()
df_actions_a8=df.loc[df['Agent Type'] == "Agent 8"]
mean_a8_actions=df_actions_a8['Actions'].astype(int).mean()
fig = plt.figure()
xaxis=["Agent 6", "Agent 7"]
yaxis=[mean_a6_actions,mean_a7_actions]
plt.bar(xaxis, yaxis)
plt.xlabel("Agents")
plt.ylabel("No. of actions")
plt.title("Actions for Agent 6 and 7")
plt.savefig("graphs/Agent6-7/Actions67.png")
fig = plt.figure()
xaxis=["Agent 6", "Agent 7","Agent 8"]
yaxis=[mean_a6_actions,mean_a7_actions,mean_a8_actions]
plt.bar(xaxis, yaxis)
plt.xlabel("Agents")
plt.ylabel("No. of actions")
plt.title("Actions for Agent 6 , 7 and 8")
plt.savefig("graphs/Agent6-7-8/Actions678.png")

adict = {
    "a6": df.loc[df['Agent Type'] == "Agent 6"],
    "a7": df.loc[df['Agent Type'] == "Agent 7"],
    "a8": df.loc[df['Agent Type'] == "Agent 8"],
}

mean_a6_moves=adict["a6"]['Movements'].astype(int).mean()
mean_a7_moves=adict["a7"]['Movements'].astype(int).mean()
mean_a8_moves=adict["a8"]['Movements'].astype(int).mean()

mean_a6_exams=adict["a6"]['Examinations'].astype(int).mean()
mean_a7_exams=adict["a7"]['Examinations'].astype(int).mean()
mean_a8_exams=adict["a8"]['Examinations'].astype(int).mean()



a6_hilly_avgactions=df.loc[(df['Agent Type'] == "Agent 6") & (df['Terrain Type'] == "Hilly")]['Actions'].astype(int).mean()
a6_hilly_avgmovements=df.loc[(df['Agent Type'] == "Agent 6") & (df['Terrain Type'] == "Hilly")]['Movements'].astype(int).mean()
a6_hilly_avgexaminations=df.loc[(df['Agent Type'] == "Agent 6") & (df['Terrain Type'] == "Hilly")]['Examinations'].astype(int).mean()

a7_hilly_avgactions=df.loc[(df['Agent Type'] == "Agent 7") & (df['Terrain Type'] == "Hilly")]['Actions'].astype(int).mean()
a7_hilly_avgexaminations=df.loc[(df['Agent Type'] == "Agent 7") & (df['Terrain Type'] == "Hilly")]['Examinations'].astype(int).mean()
a7_hilly_avgmovements=df.loc[(df['Agent Type'] == "Agent 7") & (df['Terrain Type'] == "Hilly")]['Movements'].astype(int).mean()

a8_hilly_avgactions=df.loc[(df['Agent Type'] == "Agent 8") & (df['Terrain Type'] == "Hilly")]['Actions'].astype(int).mean()
a8_hilly_avgexaminations=df.loc[(df['Agent Type'] == "Agent 8") & (df['Terrain Type'] == "Hilly")]['Examinations'].astype(int).mean()
a8_hilly_avgmovements=df.loc[(df['Agent Type'] == "Agent 8") & (df['Terrain Type'] == "Hilly")]['Movements'].astype(int).mean()

a6_flat_avgactions=df.loc[(df['Agent Type'] == "Agent 6" )& (df['Terrain Type'] == "Flat")]['Actions'].astype(int).mean()
a6_flat_avgmovements=df.loc[(df['Agent Type'] == "Agent 6" )& (df['Terrain Type'] == "Flat")]['Movements'].astype(int).mean()
a6_flat_avgexaminations=df.loc[(df['Agent Type'] == "Agent 6" )& (df['Terrain Type'] == "Flat")]['Examinations'].astype(int).mean()

a7_flat_avgactions=df.loc[(df['Agent Type'] == "Agent 7")& (df['Terrain Type'] == "Flat")]['Actions'].astype(int).mean()
a7_flat_avgmovements=df.loc[(df['Agent Type'] == "Agent 7" )& (df['Terrain Type'] == "Flat")]['Movements'].astype(int).mean()
a7_flat_avgexaminations=df.loc[(df['Agent Type'] == "Agent 7" )& (df['Terrain Type'] == "Flat")]['Examinations'].astype(int).mean()

a8_flat_avgactions=df.loc[(df['Agent Type'] == "Agent 8")& (df['Terrain Type'] == "Flat")]['Actions'].astype(int).mean()
a8_flat_avgmovements=df.loc[(df['Agent Type'] == "Agent 8" )& (df['Terrain Type'] == "Flat")]['Movements'].astype(int).mean()
a8_flat_avgexaminations=df.loc[(df['Agent Type'] == "Agent 8" )& (df['Terrain Type'] == "Flat")]['Examinations'].astype(int).mean()

a6_forest_avgactions=df.loc[(df['Agent Type'] == "Agent 6" )& (df['Terrain Type'] == "Forest")]['Actions'].astype(int).mean()
a6_forest_avgmovements=df.loc[(df['Agent Type'] == "Agent 6") & (df['Terrain Type'] == "Forest")]['Movements'].astype(int).mean()
a6_forest_avgexaminations=df.loc[(df['Agent Type'] == "Agent 6") & (df['Terrain Type'] == "Forest")]['Examinations'].astype(int).mean()

a7_forest_avgactions=df.loc[(df['Agent Type'] == "Agent 7")& (df['Terrain Type'] == "Forest")]['Actions'].astype(int).mean()
a7_forest_avgexaminations=df.loc[(df['Agent Type'] == "Agent 7") & (df['Terrain Type'] == "Forest")]['Examinations'].astype(int).mean()
a7_forest_avgmovements=df.loc[(df['Agent Type'] == "Agent 7") & (df['Terrain Type'] == "Forest")]['Movements'].astype(int).mean()

a8_forest_avgactions=df.loc[(df['Agent Type'] == "Agent 8")& (df['Terrain Type'] == "Forest")]['Actions'].astype(int).mean()
a8_forest_avgexaminations=df.loc[(df['Agent Type'] == "Agent 8") & (df['Terrain Type'] == "Forest")]['Examinations'].astype(int).mean()
a8_forest_avgmovements=df.loc[(df['Agent Type'] == "Agent 8") & (df['Terrain Type'] == "Forest")]['Movements'].astype(int).mean()

#----------------Comparison of Agent 6 and 7---------------#
plotdata = pd.DataFrame({
    "Agent 6":[a6_flat_avgactions,a6_hilly_avgactions,a6_forest_avgactions],
    "Agent 7":[a7_flat_avgactions,a7_hilly_avgactions,a7_forest_avgactions],
    }, 
    index=["Flat", "Hilly", "Forest"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions for agent 6 and 7 for different terrain types")
plt.xlabel("Terrain Types")
plt.ylabel("Number of actions")
plt.savefig("graphs/Agent6-7/Actionsperterrain67.png")

#Hilly
plotdata = pd.DataFrame({
    "Actions":[a6_hilly_avgactions,a7_hilly_avgactions],
    "Movements":[a6_hilly_avgmovements,a7_hilly_avgmovements],
    "Examinations":[a6_hilly_avgexaminations,a7_hilly_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 and 7 for Hilly terrain types")
plt.xlabel("Hilly Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7/ActionsMovesExams-Hilly-67.png")

#Flat
plotdata = pd.DataFrame({
    "Actions":[a6_flat_avgactions,a7_flat_avgactions],
    "Movements":[a6_flat_avgmovements,a7_flat_avgmovements],
    "Examinations":[a6_flat_avgexaminations,a7_flat_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 and 7 for flat terrain types")
plt.xlabel("Flat Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7/ActionsMovesExams-Flat-67.png")

#Forest
plotdata = pd.DataFrame({
    "Actions":[a6_forest_avgactions,a7_forest_avgactions],
    "Movements":[a6_forest_avgmovements,a7_forest_avgmovements],
    "Examinations":[a6_forest_avgexaminations,a7_forest_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 and 7 for forest terrain types")
plt.xlabel("Forest Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7/ActionsMovesExams-Forest-67.png")

#time comparison
df_timetaken_a6=df.loc[df['Agent Type'] == "Agent 6"]
mean_a6_timetaken=df_timetaken_a6['Time Taken'].astype(int).mean()
df_timetaken_a7=df.loc[df['Agent Type'] == "Agent 7"]
mean_a7_timetaken=df_timetaken_a7['Time Taken'].astype(int).mean()
fig = plt.figure()
xaxis=["Agent 6", "Agent 7"]
yaxis=[mean_a6_timetaken,mean_a7_timetaken]
plt.bar(xaxis, yaxis)
plt.xlabel("Agents")
plt.ylabel("Time taken to execute")
plt.title("Time taken for Agent 6 and 7 ")
# plt.show()
plt.savefig("graphs/Agent6-7/TimeTaken67.png")
#----------------Comparison of Agent 6 , 7 and 8---------------#
plotdata = pd.DataFrame({
    "Agent 6":[a6_flat_avgactions,a6_hilly_avgactions,a6_forest_avgactions],
    "Agent 7":[a7_flat_avgactions,a7_hilly_avgactions,a7_forest_avgactions],
    "Agent 8":[a8_flat_avgactions,a8_hilly_avgactions,a8_forest_avgactions],
    }, 
    index=["Flat", "Hilly", "Forest"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions for agent 6 , 7 and 8 for different terrain types")
plt.xlabel("Terrain Types")
plt.ylabel("Number of actions")
# plt.show()
plt.savefig("graphs/Agent6-7-8/Actionsperterrain678.png")

#Hilly
plotdata = pd.DataFrame({
    "Actions":[a6_hilly_avgactions,a7_hilly_avgactions,a8_hilly_avgactions],
    "Movements":[a6_hilly_avgmovements,a7_hilly_avgmovements,a8_hilly_avgmovements],
    "Examinations":[a6_hilly_avgexaminations,a7_hilly_avgexaminations,a8_hilly_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7","Agent 8"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 , 7 and 8 for Hilly terrain types")
plt.xlabel("Hilly Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7-8/ActionsMovesExams-Hilly-678.png")

#Flat
plotdata = pd.DataFrame({
    "Actions":[a6_flat_avgactions,a7_flat_avgactions,a8_flat_avgactions],
    "Movements":[a6_flat_avgmovements,a7_flat_avgmovements,a8_flat_avgmovements],
    "Examinations":[a6_flat_avgexaminations,a7_flat_avgexaminations,a8_flat_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7","Agent 8"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 , 7 and 8 for flat terrain types")
plt.xlabel("Flat Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7-8/ActionsMovesExams-Flat-678.png")

#Forest
plotdata = pd.DataFrame({
    "Actions":[a6_forest_avgactions,a7_forest_avgactions,a8_forest_avgactions],
    "Movements":[a6_forest_avgmovements,a7_forest_avgmovements,a8_forest_avgmovements],
    "Examinations":[a6_forest_avgexaminations,a7_forest_avgexaminations,a8_forest_avgexaminations]
    }, 
    index=["Agent 6", "Agent 7","Agent 8"]
)
plotdata.plot(kind="bar")
plt.title("Number of actions/movements/examinations for agent 6 , 7 and 8 for forest terrain types")
plt.xlabel("Forest Terrain Type")
plt.ylabel("Number of actions/movements/examinations")
# plt.show()
plt.savefig("graphs/Agent6-7-8/ActionsMovesExams-Forest-678.png")

df_timetaken_a6=df.loc[df['Agent Type'] == "Agent 6"]
mean_a6_timetaken=df_timetaken_a6['Time Taken'].astype(int).mean()
df_timetaken_a7=df.loc[df['Agent Type'] == "Agent 7"]
mean_a7_timetaken=df_timetaken_a7['Time Taken'].astype(int).mean()
df_timetaken_a8=df.loc[df['Agent Type'] == "Agent 8"]
mean_a8_timetaken=df_timetaken_a8['Time Taken'].astype(int).mean()
fig = plt.figure()
xaxis=["Agent 6", "Agent 7", "Agent 8"]
yaxis=[mean_a6_timetaken,mean_a7_timetaken,mean_a8_timetaken]
plt.bar(xaxis, yaxis)
plt.xlabel("Agents")
plt.ylabel("Time taken to execute")
plt.title("Time Taken for Agent 6 , 7 and 8")
# plt.show()
plt.savefig("graphs/Agent6-7-8/TimeTaken678.png")

