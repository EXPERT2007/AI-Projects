
# =====================================
# VISUALIZATION HELPER FOR TRAINING PROGRESS
# =====================================
# Provides real-time plotting functionality to track agent performance during training

import matplotlib.pyplot as plt
from IPython import display

# Enable interactive plotting mode
plt.ion()

def plot(scores, mean_scores):
    """
    Create and update a real-time plot showing training progress.
    Displays both individual game scores and running mean scores.
    
    Args:
        scores: List of scores from individual games
        mean_scores: List of running mean scores
    """
    # Clear previous output and display current plot
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    
    # Set up plot appearance
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    
    # Plot both score lines
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    
    # Add text labels showing latest values
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    
    # Display plot without blocking execution
    plt.show(block=False)
    plt.pause(.1)