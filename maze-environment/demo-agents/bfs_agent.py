import gymnasium as gym
import numpy as np
from gymnasium import spaces
from maze.envs.maze_model import MazeModel
from maze.envs.maze_model import MazeState

def bfs(state, model):
    states_generated = 0
    Q = []
    Q.append((state, None, None))

    while len(Q) > 0:
        current_node = Q.pop(0)
        if model.GOAL_TEST(current_node[0]):
            state1, action, parent = current_node
            history = []
            while parent is not None:
                history.append(action)
                state1, action, parent = parent
            history.reverse()
            return history, states_generated

        for action in model.ACTIONS(current_node[0]):
            states_generated += 1
            child = model.RESULT(current_node[0], action)
            Q.append((child, action, current_node))

def main():
    model = MazeModel

    render_mode = "ansi"
    maze_size = 7

    env = gym.make('maze/Maze', render_mode=render_mode, size = maze_size) #, maze_size=maze_size)
    observation, info = env.reset()
    state = MazeState(size = maze_size)
    #state.observation = observation

    steps = bfs(state, model)
    print(state)
    print()
    for step in steps:
        state = model.RESULT(state, step)
        print(state)
        print()

    env.close()
    return

if __name__ == "__main__":
    main()
