import gymnasium as gym
import numpy as np
from gymnasium import spaces
from maze.envs.maze_model import MazeModel
from maze.envs.maze_model import MazeState
import queue
import sys

def A_star(s0, model):
    states_generated = 0
    reached = {}
    Q = queue.PriorityQueue()
    Q.put(s0)

    reached[s0.index_of_agent] = s0

    while not Q.empty():
        s = Q.get()

        s.estimated_cost = 0
        if model.GOAL_TEST(s):
            history = []
            
            temp = s
            while temp.parent is not None:
                history.append(temp.action)
                temp = temp.parent

            history.reverse()
            return history, states_generated

        for a in model.ACTIONS(s):
            states_generated += 1
            s1 = model.RESULT(s, a)
            s1.parent = s
            s1.action = a
            s1.cost += s.cost
            s1.cost += model.STEP_COST(s1, a, s)
            s1.estimated_cost = s1.cost + model.HEURISTIC(s1)

            key = s1.index_of_agent
            if key not in reached or ((s1.estimated_cost + s1.cost) < (reached[key].estimated_cost + reached[key].cost)):
                Q.put(s1)
                reached[key] = s1

    raise Exception("couldn't find anything")

def main():
    sys.setrecursionlimit(100000)
    model = MazeModel

    render_mode = "ansi"
    maze_size = 51

    env = gym.make('maze/Maze', render_mode=render_mode, size = maze_size) #, maze_size=maze_size)
    observation, info = env.reset()
    state = MazeState(size = maze_size)
    state.observation = observation

    steps = A_star(state, model)
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
