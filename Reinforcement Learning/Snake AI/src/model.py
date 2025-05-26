
# =====================================
# NEURAL NETWORK MODEL FOR DEEP Q-LEARNING
# =====================================
# Implements the Q-Network and training components for the Snake AI agent

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# =====================================
# Q-NETWORK ARCHITECTURE
# =====================================

class Linear_QNet(nn.Module):
    """
    Neural network for Q-value approximation in Deep Q-Learning.
    Simple feedforward network with one hidden layer.
    """
    
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize the Q-Network architecture.
        
        Args:
            input_size: Number of input features (state size)
            hidden_size: Number of neurons in hidden layer
            output_size: Number of possible actions
        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x: Input state tensor
            
        Returns:
            Q-values for each possible action
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Save the trained model to disk.
        
        Args:
            file_name: Name of the file to save the model
        """
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

# =====================================
# Q-LEARNING TRAINER
# =====================================

class QTrainer:
    """
    Training component for the Q-Network using Deep Q-Learning algorithm.
    Handles loss computation, backpropagation, and parameter updates.
    """
    
    def __init__(self, model, lr, gamma):
        """
        Initialize the trainer with model and hyperparameters.
        
        Args:
            model: Q-Network to train
            lr: Learning rate for optimization
            gamma: Discount factor for future rewards
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Perform one training step using the Q-Learning update rule.
        
        Args:
            state: Current state(s)
            action: Action(s) taken
            reward: Reward(s) received
            next_state: Next state(s) reached
            done: Whether episode(s) ended
        """
        # Convert inputs to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        # Handle single experience vs batch
        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        # 2: Apply Q-Learning update rule: Q_new = reward + gamma * max(next_Q_values)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        
        # Perform gradient descent step
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()


