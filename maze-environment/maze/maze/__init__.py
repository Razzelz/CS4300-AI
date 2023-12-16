from gymnasium.envs.registration import register

from maze.envs.maze_env import MazeEnv
from maze.envs.maze_model import MazeModel
from maze.envs.maze_model import MazeState

register(
    # maze is this folder name
    # -v0 is because this first version
    # Maze is the pretty name for gym.make
    id="maze/Maze-v0",
    
    # maze.envs is the path maze/envs
    # MazeEnv is the class name
    entry_point="maze.envs:MazeEnv",
    
    # configure the automatic wrapper to truncate after 50 steps
    max_episode_steps=50,
)
