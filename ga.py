directions=['U','D','L','R']
#generate chromosome
import random
def generate_chromosome():
    chromosome=[]
    for _ in range(100):
        move = random.choice(directions)
        chromosome.append(move)

    return chromosome

#generate population
def generate_population():
    population=[]
    for _ in range(100):
        chromosome=generate_chromosome()
        population.append(chromosome)
    return population


#simulate for chromosome
def simulate_chromosome(grid,chromosome):
    x,y=0,0
    energy=0
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
                energy+=1
            elif grid[x][y]=='W':
                energy+=5
            if grid[x][y] == 'S':
                energy += 0
            if grid[x][y]=='T':
                return energy,True,path
    return energy ,False,path


#fitness function
def fitness(grid, chromosome):

    energy, success, path = simulate_chromosome(grid, chromosome)

    x, y = path[-1]   # 👈 أهم تعديل

    if success:
        return 1000 - energy

    distance = abs(14 - x) + abs(14 - y)

    return 1000 - (distance * 10) - energy
    

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
        if scores[r1]>scores[r2]:
            selected.append(population[r1])
        else:
            selected.append(population[r2])
    return selected

#crossover
def crossover(parent1,parent2):
    point=random.randint(1,len(parent1)-1)
    child=parent1[:point]+parent2[point:]
    return child

#mutation
def mutation(chromosome,mutation_rate=.03):
    directions=['U','D','L','R']
    for i in range(len(chromosome)):
        if random.random()<mutation_rate:
            chromosome[i]=random.choice(directions)
    return chromosome




    







