import random

def generate_maze(rows, cols):
    maze = [['#' for _ in range(cols)] for _ in range(rows)]
    
    # Set start
    start = (1, 1)
    maze[start[0]][start[1]] = 'A'
    
    stack = [start]
    visited = set([start])

    while stack:
        current_cell = stack[-1]
        x, y = current_cell

        neighbors = [
            (x + 2, y), (x - 2, y),  # Move vertically
            (x, y + 2), (x, y - 2)   # Move horizontally
        ]
        random.shuffle(neighbors)

        found = False
        for nx, ny in neighbors:
            if 0 < nx < rows - 1 and 0 < ny < cols - 1 and (nx, ny) not in visited:
                # Carve a passage
                maze[(x + nx) // 2][(y + ny) // 2] = ' '
                maze[nx][ny] = ' '
                stack.append((nx, ny))
                visited.add((nx, ny))
                found = True
                break

        if not found:
            stack.pop()

    # Set goal
    goal = (rows - 2, cols - 2)
    maze[goal[0]][goal[1]] = 'G'

    conversion_dict = {'#': 2, 'A': 0, ' ': 1, 'G': 3}
    output_array = []

    for i, row in enumerate(maze):
        if i == 0:
            continue
        if i == len(maze) - 1:
            continue
        for j, col in enumerate(row):
            if j == 0:
                continue
            if j == len(maze) - 1:
                continue
            output_array.append(conversion_dict[col])

    return output_array

def print_maze(maze):
    for row in maze:
        print(' '.join(row))

if __name__ == "__main__":
    rows = 5
    cols = 5
    maze = generate_maze(rows, cols)
    print(maze)
