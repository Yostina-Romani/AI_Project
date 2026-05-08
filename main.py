import matplotlib.pyplot as plt
import time
size=100
chromosome_length=100
import random   
Rows=15
Cols=15
grid=[['.' for _ in range(Cols)] for _ in range(Rows)]
grid[0][0]='S'
grid [14][14]='T'

# swaps random توزيع
count=0
num_swaps=30
while count<num_swaps:
    x=random.randint(0,Rows-1)
    y=random.randint(0,Cols-1)

    #عاشان نتاكد ان ما نحطش في   S OR W

    if grid[x][y]=='.':
        grid[x][y]='W'
    count +=1

#bfs task
########
from collections import deque
def bfs_search(grid):
    rows=len(grid)
    cols=len(grid[0])
    start=(0,0)
    t=grid[14][14]
    directions=[(0,1),(0,-1),(1,0),(-1,0)]
    cell_visited=set()
    
    q=deque()
    q.append((start[0],start[1],[(start[0],start[1])]))
    cell_visited.add(start)
    
    while q:
        x,y,path=q.popleft()
        if grid[x][y]=='T':
            return path,True
        for dx,dy in directions:
            nx=dx+x
            ny=dy+y
            if 0<=nx and nx<rows and 0<=ny and ny <cols :
                if (nx,ny) not in cell_visited :
                    cell_visited.add((nx,ny))
                   
                    q.append((nx,ny,path+[(nx,ny)]))

                
    return [] ,False

########
#calculate cost of bfs
def bfs_cost(path):
    cost =0;
    for x,y in path:
        if grid[x][y]=='.':
            cost+=1;

        if grid[x][y]=='W':
            cost+=5
    return cost





#GA Task
#########


directions=['U','D','L','R']

#generate chromosome
def generate_chromosome(chromosome_length):
    chromosome=[]
    for _ in range(chromosome_length):
        move = random.choice(directions)
        chromosome.append(move)

    return chromosome

#generate population
def generate_population(size):
    population=[]
    for _ in range(size):
        chromosome=generate_chromosome(chromosome_length)
        population.append(chromosome)
    return population


#simulate for chromosome
def simulate_chromosome(grid,chromosome):
    x,y=0,0
    total_cost=0
    path=[(x,y)]
    directions_map={
        'U':(-1,0),
        'D':(1,0),
        'R':(0,1),
        'L':(0,-1)
    }
    rows=len(grid)
    cols=len(grid[0])
    for move in chromosome:
        dx,dy=directions_map[move]
        nx=x+dx
        ny=y+dy
        if 0<=nx<rows and 0<=ny<cols:
            x,y=nx,ny
            path.append((x,y))
            if grid[x][y]=='.':
                total_cost+=1
            elif grid[x][y]=='W':
                total_cost+=5
            if grid[x][y] == 'S':
                total_cost+= 0
            if grid[x][y]=='T':
                return total_cost,True,path
    return total_cost ,False,path


#fitness function
def fitness(grid, chromosome):
    score=0
    cost, success, path = simulate_chromosome(grid, chromosome)

    x, y = path[-1]   # 👈 أهم تعديل

    if success:
        score+=500
    distance=(abs(14-x)+abs(14-y))*10
    score-=cost
    score-=distance

    return score
    

#evaluate population
def evaluate_population(population,grid):
    scores=[]
    for chromosome in population:
        score=fitness(grid,chromosome)
        scores.append(score)
    return scores


#selection

def selection(population,scores):
    selected=[]
    for _ in range(len(population)):
        r1=random.randint(0,len(population)-1)
        r2=random.randint(0,len(population)-1)
        r3=random.randint(0,len(population)-1)
        best_score=r1
        if scores[r2]>scores[best_score]:
            best_score=r2

        if scores[r3]>scores[best_score]:
            best_score=r3
        selected.append(population[best_score])
    return selected

#crossover
def crossover(parent1,parent2):
    size=len(parent1)
    point=random.randint(0,size-1)
    child=parent1[:point]+parent2[point:]
    
    return child





#mutation
def mutation(chromosome,mutation_rate=.03):
    directions=['U','D','L','R']
    for i in range(len(chromosome)):
        if random.random()<mutation_rate:
            chromosome[i]=random.choice(directions)
    return chromosome



#########

#main code
bfs_time_start=time.time()
bfs_path,success_bfs = bfs_search(grid)
bfs_end_time=time.time();
bfs_total_cost=bfs_cost(bfs_path)
steps=len(bfs_path)-1
bfs_time=bfs_end_time-bfs_time_start;
print(" total cost of bfs :",bfs_total_cost)
print(" total steps of bfs :",steps)
print(" reached treasure :",success_bfs)
print(" bfs time :",bfs_time)




global_best=None
global_best_score = float("-inf")

population=generate_population(size)

best_scores=[]
start_ga = time.time()

for generation in range(400):
    scores=evaluate_population(population,grid)
    best_score=max(scores)
    best_scores.append(best_score)
    selected=selection(population,scores)
    new_population=[]

    if best_score>global_best_score:
        global_best_score=best_score
        global_best=population[scores.index(best_score)]
    new_population.append(global_best)
    for i in range(0,len(selected)-1,2):
        parent1=selected[i]
        parent2=selected[i+1]
        child1=crossover(parent1,parent2)     
        child2=crossover(parent2,parent1)

        child1=mutation(child1)
        child2=mutation(child2)
        new_population.append(child1)
        new_population.append(child2)

    population=new_population
 

end_ga = time.time()
ga_time=end_ga-start_ga

best_chromosome=global_best
#print(best_chromosome)
energy, success, ga_path = simulate_chromosome(grid, best_chromosome)
print("total cost of ga:",energy)
print("reached treasure:" ,success)
print("GA time:" ,ga_time)

#print("final position:" ,ga_path)



#visualization
import numpy as np

def draw_grid(grid, bfs_path=None, ga_path=None):

    rows = len(grid)
    cols = len(grid[0])
    heatmap=np.zeros((rows,cols))
    # رسم الأساس
    for i in range(rows):
        for j in range(cols):

            if grid[i][j] == 'W':
                heatmap[i][j]=5
            

            else:
                heatmap[i][j]=1  
    plt.figure(figsize=(6,6))
    plt.imshow(heatmap,cmap='YlOrRd')

    # رسم BFS path
    if bfs_path:
        bx = [p[1] for p in bfs_path]
        by = [p[0] for p in bfs_path]
        plt.plot(bx, by, color='blue', label='BFS Path')

    # رسم GA path
    if ga_path:
        gx = [p[1] for p in ga_path]
        gy = [p[0] for p in ga_path]
        plt.plot(gx, gy, color='orange', label='GA Path')

    plt.legend()
    plt.title("Treasure Hunt - BFS vs GA")
    plt.gca().invert_yaxis()  # عشان الشكل يبقى زي المصفوفة
    plt.grid()
    plt.show()

draw_grid(grid, bfs_path, ga_path)
#######

#draw bfs path

def plot_bfs(grid, bfs_path):
    rows = len(grid)
    cols = len(grid[0])
    heatmap = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            heatmap[i][j] = 5 if grid[i][j] == 'W' else 1

    plt.figure(figsize=(6,6))
    plt.imshow(heatmap, cmap='YlOrRd')

    bx = [p[1] for p in bfs_path]
    by = [p[0] for p in bfs_path]
    plt.plot(bx, by, color='blue', label='BFS Path')

    plt.title("BFS Path Only")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid()
    plt.show()
plot_bfs(grid,bfs_path)

#######

#draw GA path
def plot_ga(grid, ga_path):
    rows = len(grid)
    cols = len(grid[0])
    heatmap = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            heatmap[i][j] = 5 if grid[i][j] == 'W' else 1

    plt.figure(figsize=(6,6))
    plt.imshow(heatmap, cmap='YlOrRd')

    gx = [p[1] for p in ga_path]
    gy = [p[0] for p in ga_path]
    plt.plot(gx, gy, color='orange', label='GA Path')

    plt.title("GA Path Only")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid()
    plt.show()
plot_ga(grid,ga_path)



#generations_fitnesss visualization
plt.plot(best_scores)
plt.xlabel("generation")
plt.ylabel("best fitness")
plt.title("genetic algorithm progress")
plt.show()