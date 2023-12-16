#!/usr/bin/env python3
import gymnasium as gym
import maze
import random
import queue
import time
import argparse
import os
import sys

import bfs_agent
import a_star_agent

def main(iterations=10, size=5, searches=[], debug=False, outputFile=False):
    model = maze.MazeModel

    render_mode = "ansi"

    for search in searches:
        averageNodes = 0
        nodesGenerated = []

        averageTime = 0
        times = []

        for i in range(iterations):
            print(f"Working on iteration {i}", end="")
            env = gym.make('maze/Maze-v0', render_mode=render_mode, size=size)
            observation, info = env.reset()
            state = maze.MazeState(size=size)
            state.observation = observation
            if debug:
                print(state)

            terminated = truncated = False

            startTime = time.time()
            steps, total_states_generated = search(state, model)
            endTime = time.time()
            if debug:
                print(steps)

            averageTime += (endTime - startTime)
            times.append((endTime - startTime))

            averageNodes += total_states_generated
            nodesGenerated.append(total_states_generated)
            print(f" --> {endTime-startTime:.2f} seconds\n")

            env.close()

        nodesGenerated.sort()
        times.sort()
        output = f"{search.__name__} iterations: {iterations} size: {size}\n"
        output += f"\tgridSize: {size}x{size}\n"
        output += f"\titerations: {iterations}\n"
        output += f"\taverage nodes generated: {averageNodes / iterations}\n"
        output += f"\tMedian nodes generated: {nodesGenerated[len(nodesGenerated) // 2]}\n"
        output += f"\tLowest nodes generated: {nodesGenerated[0]}\n"
        output += f"\tLargest nodes generated: {nodesGenerated[-1]}\n"
        # output += f"\tAll node counts list: {nodesGenerated}\n"
        output += "\n"
        output += f"\tAverageTime: {averageTime / iterations:.6f}\n"
        output += f"\tMedian times: {times[len(times) // 2]:.6f}\n"
        output += f"\tLowest time: {times[0]:.6f}\n"
        output += f"\tLargest time: {times[-1]:.6f}\n"
        # output += f"\tTimes list: {times}\n"
        output += f"\n\n"

        if outputFile:
            f = open(f"{search.__name__}_{size}.txt", "a")
            f.write(output)
            f.close()

        print(output)
    return

if __name__ == "__main__":
    sys.setrecursionlimit(100_000_000)
    print(f"PID: {os.getpid()}")
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--i', type=int, help='how many iterations to do')
    parser.add_argument('--s', type=int, help='size to use')
    parser.add_argument('--astar', action='store_true', help='enable ASTAR search')
    parser.add_argument('--bfs', action='store_true', help='enable BFS search')
    parser.add_argument('--debug', action='store_true', help='enable debug')
    parser.add_argument('--outputFile', action='store_true', help='output to file')

    args = parser.parse_args()
    print(args)
    print()

    if args.i == None:
        args.i = 10
    if args.s == None:
        args.s = 5

    searches = []
    if args.astar:
        searches.append(a_star_agent.A_star)
    if args.bfs:
        searches.append(bfs_agent.bfs)

    main(iterations=args.i, size=args.s, searches=searches, debug=args.debug, outputFile=args.outputFile)
