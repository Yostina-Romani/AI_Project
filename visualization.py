import matplotlib.pyplot as plt

def draw_grid(grid, bfs_path=None, ga_path=None):

    rows = len(grid)
    cols = len(grid[0])

    # رسم الأساس
    for i in range(rows):
        for j in range(cols):

            if grid[i][j] == 'W':
                plt.scatter(j, i, color='black', s=100)  # swamp
            elif grid[i][j] == 'S':
                plt.scatter(j, i, color='green', s=100)  # start
            elif grid[i][j] == 'T':
                plt.scatter(j, i, color='red', s=100)    # treasure

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