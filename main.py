from bfs import *
from ga import *
Rows=15
Cols=15
grid=[['.' for _ in range(Cols)] for _ in range(Rows)]
grid[0][0]='S'
grid [14][14]='T'

# swaps random توزيع
import random
count=0
num_swaps=30
while count<num_swaps:
    x=random.randint(0,Rows-1)
    y=random.randint(0,Cols-1)

    #عاشان نتاكد ان ما نحطش في   S OR W

    if grid[x][y]=='.':
        grid[x][y]='W'
    count +=1
bfs_energy, bfs_path = bfs_search(grid)
print(bfs_energy, bfs_path)

population=generate_population()

for generation in range(300):
    scores=evaluate_population(population,grid)
    selected=selection(population,scores)
    new_population=[]
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

scores=evaluate_population(population,grid)
best_index=scores.index(max(scores))
best_chromosome=population[best_index]
print(best_chromosome)
energy, success, ga_path = simulate_chromosome(grid, best_chromosome)
print("energy:",energy)
print("treasure:" ,success)
print("final position:" ,ga_path)

#visualization

from visualization import draw_grid

draw_grid(grid, bfs_path, ga_path)