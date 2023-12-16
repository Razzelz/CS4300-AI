import gymnasium
import numpy as np
from gymnasium import spaces
from maze.envs.maze_model import MazeModel
from maze.envs.maze_model import MazeState

try:
    import pygame
except ImportError as e:
    raise DependencyNotInstalled(
        "pygame is not installed, `pip install` must have failed."
    ) from e

class MazeEnv(gymnasium.Env):

    metadata = {
        "render_modes": ["human", "rgb_array", "ansi"],
        "render_fps": 1,
    }

    def __init__(self, render_mode=None, size=4):
        self.render_mode = render_mode
        self.size = size
        self.action_space = spaces.Discrete(size)
        self.observation_space = spaces.Box(0, 3, shape=(size * size,), dtype=np.int8)

    #    # display support
    #    self.cell_size = (800//size, 60)
    #    self.window_size = (
    #        self.size * self.cell_size[0],
    #        1 * self.cell_size[1],
    #    )
    #    self.window_surface = None
    #    self.clock = None
    #    self.head_color = (255, 0, 0)
    #    self.tail_color = (0, 0, 255)
    #    self.background_color = (170, 170, 170)
    #    return

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = MazeState(size = self.size)
        self.state.randomize(seed)

        observation = self.state.observation
        info = {}
        return observation, info

    def step(self, action):
        state = self.state
        state1 = MazeModel.RESULT(state, action)
        self.state = state1
        
        observation = self.state.observation
        reward = MazeModel.STEP_COST(state, action, state1)
        terminated = MazeModel.GOAL_TEST(state1)
        info = {}

        # display support
        if self.render_mode == "human":
            self.render()
        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        if self.render_mode == "ansi":
            return self._render_text()
        else:
            return self._render_gui(self.render_mode)

    def _render_text(self):
        return str(self.state)

    #def _render_gui(self, mode):
    #    if self.window_surface is None:
    #        pygame.init()

    #        if mode == "human":
    #            pygame.display.init()
    #            pygame.display.set_caption("Maze")
    #            self.window_surface = pygame.display.set_mode(self.window_rize)
    #        else:  # rgb_array
    #            self.window_surface = pygame.Surface(self.window_size)
    #    if self.clock is None:
    #        self.clock = pygame.time.Clock()

    #    rect = pygame.Rect((0,0), self.window_size)
    #    pygame.draw.rect(self.window_surface, self.background_color, rect)
    #    for coin in range(self.size):
    #        x = (coin+0.5)*self.cell_size[0]
    #        y = 0.5*self.cell_size[1]
    #        r = 0.4*min(self.cell_size)
    #        if self.state.coin(coin):
    #            color = self.tail_color
    #        else:
    #            color = self.head_color
    #        pygame.draw.circle(self.window_surface, color, (x,y), r)

    #    if mode == "human":
    #        pygame.event.pump()
    #        pygame.display.update()
    #        self.clock.tick(self.metadata["render_fps"])
    #    else:  # rgb_array
    #        return np.transpose(
    #            np.array(pygame.surfarray.pixels3d(self.window_surface)), axes=(1, 0, 2)
    #        )
    #
    #def close(self):
    #    if self.window_surface is not None:
    #        pygame.display.quit()
    #        pygame.quit()
    #    return
