
# =====================================
# DEEP Q-LEARNING AGENT FOR SNAKE GAME
# =====================================
# Implements a Deep Q-Learning agent that learns to play Snake game
# using neural networks and experience replay

import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

# Hyperparameters for training
MAX_MEMORY = 100_000  # Maximum size of experience replay buffer
BATCH_SIZE = 1000     # Number of experiences to sample for training
LR = 0.001           # Learning rate for neural network

# =====================================
# DEEP Q-LEARNING AGENT CLASS
# =====================================

class Agent:
    """
    Deep Q-Learning agent that learns to play Snake game.
    Uses neural network to approximate Q-values and epsilon-greedy exploration.
    """

    def __init__(self):
        """
        Initialize the agent with neural network, memory buffer, and hyperparameters.
        """
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # =====================================
    # STATE REPRESENTATION
    # =====================================

    def get_state(self, game):
        """
        Extract the current state of the game as an 11-dimensional feature vector.
        Includes danger detection, movement direction, and food location relative to snake head.
        
        Args:
            game: Current SnakeGameAI instance
            
        Returns:
            numpy array representing the current state
        """
        head = game.snake[0]
        # Define points in each direction from the snake head
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        # Current direction booleans
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    # =====================================
    # MEMORY AND TRAINING
    # =====================================

    def remember(self, state, action, reward, next_state, done):
        """
        Store experience in replay buffer for later training.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
            done: Whether episode ended
        """
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        """
        Train the neural network using a batch of experiences from memory buffer.
        Implements experience replay to improve learning stability.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train the neural network on a single experience immediately.
        Used for online learning during game play.
        """
        self.trainer.train_step(state, action, reward, next_state, done)

    # =====================================
    # ACTION SELECTION
    # =====================================

    def get_action(self, state):
        """
        Select action using epsilon-greedy strategy.
        Balances exploration (random actions) with exploitation (neural network predictions).
        
        Args:
            state: Current game state
            
        Returns:
            List representing action [straight, right, left] with one-hot encoding
        """
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

# =====================================
# TRAINING LOOP
# =====================================

def train():
    """
    Main training loop for the Deep Q-Learning agent.
    Runs continuous episodes, collecting experiences and training the neural network.
    Tracks scores and displays real-time performance plots.
    """
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

# =====================================
# SCRIPT EXECUTION
# =====================================

if __name__ == '__main__':
    # Start training the agent
    train()