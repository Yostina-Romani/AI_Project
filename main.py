from bfs import bfs_search
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
print(bfs_search(grid))