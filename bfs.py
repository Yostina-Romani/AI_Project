from collections import deque
def bfs_search(grid):
    rows=len(grid)
    cols=len(grid[0])
    start=(0,0)
    cost=0
    t=grid[14][14]
    directions=[(0,1),(0,-1),(1,0),(-1,0)]
    cell_visited=set()
    
    q=deque()
    q.append((start[0],(start[1]),[start],cost))
    
    while q:
        x,y,path,cost=q.popleft()
        if grid[x][y]=='T':
            return cost ,path
        for dx,dy in directions:
            nx=dx+x
            ny=dy+y
            if 0<=nx and nx<rows and 0<=ny and ny <cols and (nx,ny) not in cell_visited :
                cell_visited.add((nx,ny))
                if grid[nx][ny]=='.':
                    cost+=1
                if grid[nx][ny]=='W':
                    cost+=5
                q.append((nx,ny,path+[(nx,ny)],cost))
                
    return None ,float('inf')