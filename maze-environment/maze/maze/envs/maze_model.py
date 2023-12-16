import numpy as np
import random
import copy

class MazeState:

    def __init__(self, size):
        if size % 2 == 0:
            raise Exception("Size must be odd!")
        self.maze = np.array(self.generate_maze(size+2, size+2), dtype=np.int8)
        self.size = size
        self.index_of_agent = 0
        self.index_of_goal = self.size * self.size - 1
        self.game_over = False
        self.cost = 0
        self.estimated_cost = 0
        self.parent = None
        self.action = None
        return

    def __lt__(self,other):
        return self.estimated_cost < other.estimated_cost

    def getIndexOfAgent(self):
        return self.index_of_agent

    def getLegalMoves(self):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

        actions = [0,1,2,3]
        index = self.getIndexOfAgent()

        if self.maze[index + 1] == 2 or index % self.size == self.size - 1:
            actions.remove(RIGHT)
            #remove RIGHT from actions

        if self.maze[index - 1] == 2 or index % self.size == 0:
            actions.remove(LEFT)
            #remove LEFT from actions

        if index + self.size > (self.size * self.size - 1) or self.maze[index + self.size] == 2:
            actions.remove(DOWN)
            #remove DOWN from actions

        if self.maze[index - self.size] == 2 or index - self.size < 0:
            actions.remove(UP)
            #remove UP from actions

        return actions

    def move(self, action):
        if action not in self.getLegalMoves():
            print("action not legal")
            return

        old_index = self.index_of_agent

        if action == 0:
            self.index_of_agent -= self.size
        if action == 1:
            self.index_of_agent += self.size
        if action == 2:
            self.index_of_agent -= 1
        if action == 3:
            self.index_of_agent += 1

        #Update the board
        self.maze[self.index_of_agent] = 0
        self.maze[old_index] = 1

        if self.checkGoal():
            self.game_over = True

        return

    def checkGoal(self):
        return self.index_of_agent == self.index_of_goal

    def randomize(self, seed=None):
        return

    @property
    def observation(self):
        return self.maze

    @observation.setter
    def observation(self, value):
        return

    def generate_maze(self, rows, cols):
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

    def __str__(self):
        #This is to rewrite the maze as ASCII
        maze_string = ""

        for i in range(self.size + 2):
            maze_string += "# "
        maze_string += "\n# "

        for i in range(len(self.maze)):
            if self.maze[i] == 0:
                maze_string += "A "
            if self.maze[i] == 1:
                maze_string += "  "
            if self.maze[i] == 2:
                maze_string += "# "
            if self.maze[i] == 3:
                maze_string += "G "
            if i % self.size == self.size - 1:
                maze_string += "#\n# "

        for i in range(self.size + 1):
            maze_string += "# "

        return maze_string

if __name__ == "__main__":
    s = MazeState()
    while not s.game_over:
        print(s)
        print(s.getLegalMoves())
        action = int(input("Choose an action: "))
        s.move(action)
    print("Game over, you win!")

    
class MazeModel:

    def ACTIONS(state):
        return state.getLegalMoves();

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.move(action)
        return state1

    def GOAL_TEST(state):
        return state.checkGoal()

    def STEP_COST(state, action, state1):
        return 1

    def HEURISTIC(state):
        estimated_cost = 0
        return estimated_cost

if __name__ == "__main__":
    maze = MazeState()
    print(maze)
