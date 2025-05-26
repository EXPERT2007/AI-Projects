
# =====================================
# SNAKE GAME FOR HUMAN PLAYERS
# =====================================
# Traditional Snake game implementation with keyboard controls
# Allows human players to play the classic Snake game

import pygame
import random
from enum import Enum
from collections import namedtuple

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
SPEED = 20

# =====================================
# SNAKE GAME CLASS
# =====================================

class SnakeGame:
    """
    Classic Snake game for human players with keyboard controls.
    """
    
    def __init__(self, w=640, h=480):
        """
        Initialize the game with display and initial state.
        
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
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()

    # =====================================
    # GAME STATE MANAGEMENT
    # =====================================
        
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
        
    def play_step(self):
        """
        Execute one game step.
        Handles input, movement, collision detection, and rendering.
        
        Returns:
            Tuple of (game_over, score)
        """
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    # =====================================
    # COLLISION DETECTION
    # =====================================
    
    def _is_collision(self):
        """
        Check if snake has collided with boundaries or itself.
        
        Returns:
            True if collision detected, False otherwise
        """
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
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
        
    def _move(self, direction):
        """
        Update snake head position based on direction.
        
        Args:
            direction: Direction enum value
        """
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

# =====================================
# GAME EXECUTION
# =====================================            

if __name__ == '__main__':
    """
    Main game loop for human player.
    Runs until game over, then displays final score.
    """
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
    pygame.quit()