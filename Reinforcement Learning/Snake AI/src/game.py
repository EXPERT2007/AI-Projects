
# =====================================
# SNAKE GAME ENVIRONMENT FOR AI TRAINING
# =====================================
# Pygame-based Snake game implementation designed for reinforcement learning
# Provides state observation, action execution, and reward feedback for AI agents

import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# Initialize pygame and font
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

# =====================================
# GAME CONSTANTS AND ENUMS
# =====================================

class Direction(Enum):
    """Enumeration for movement directions."""
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Named tuple for 2D coordinates
Point = namedtuple('Point', 'x, y')

# RGB color definitions
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

# Game parameters
BLOCK_SIZE = 20
SPEED = 40

# =====================================
# SNAKE GAME CLASS
# =====================================

class SnakeGameAI:
    """
    Snake game environment designed for AI training.
    Provides standard RL interface with states, actions, and rewards.
    """

    def __init__(self, w=640, h=480):
        """
        Initialize the game environment.
        
        Args:
            w: Window width in pixels
            h: Window height in pixels
        """
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    # =====================================
    # GAME STATE MANAGEMENT
    # =====================================

    def reset(self):
        """
        Reset the game to initial state.
        Called at the start of each episode.
        """
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        """
        Randomly place food on the game board.
        Ensures food doesn't spawn on snake body.
        """
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    # =====================================
    # MAIN GAME LOOP
    # =====================================

    def play_step(self, action):
        """
        Execute one game step with the given action.
        
        Args:
            action: List representing action [straight, right, left]
            
        Returns:
            Tuple of (reward, game_over, score)
        """
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    # =====================================
    # COLLISION DETECTION
    # =====================================

    def is_collision(self, pt=None):
        """
        Check if the given point (or snake head) collides with boundaries or snake body.
        
        Args:
            pt: Point to check for collision (defaults to snake head)
            
        Returns:
            True if collision detected, False otherwise
        """
        if pt is None:
                        pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    # =====================================
    # RENDERING AND DISPLAY
    # =====================================

    def _update_ui(self):
        """
        Update the game display with current state.
        Renders snake, food, and score.
        """
        self.display.fill(BLACK)

        # Draw snake body
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # Draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    # =====================================
    # MOVEMENT CONTROL
    # =====================================

    def _move(self, action):
        """
        Update snake direction and position based on action.
        
        Args:
            action: List representing action [straight, right, left]
        """
        # [straight, right, left]

        # Define clockwise direction cycle
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        # Determine new direction based on action
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        # Update head position based on new direction
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)