import torch
import torch.nn as nn
import torch.nn.functional as F

class PPOModel(nn.Module):
    def __init__(self, board_size):
        """
        Initialize the Actor-Critic Neural Network for PPO.
        The network uses Convolutional layers to 'see' the board patterns
        and Linear layers to make decisions.
        """
        super(PPOModel, self).__init__()
        self.board_size = board_size
        
        # --- CONVOLUTIONAL BLOCK (The 'Eyes' of the AI) ---
        # These layers extract spatial features (like lines of 3 or 4 stones)
        self.conv_block = nn.Sequential(
            # First layer: Detects basic patterns (1 input channel -> 64 feature maps)
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            
            # Second layer: Deepens the understanding (64 -> 128 feature maps)
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            
            # Third layer: Solidifies pattern recognition (128 -> 128 feature maps)
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU()
        )
        
        # Calculate the total number of features after flattening the 2D grid
        self.flatten_size = 128 * board_size * board_size
        
        # --- ACTOR HEAD (The Decision Maker) ---
        # Suggests where to move next by outputting a score for every cell on the board
        self.actor = nn.Sequential(
            nn.Linear(self.flatten_size, 256),
            nn.ReLU(),
            # Output size is board_size^2 (one value for each possible move)
            nn.Linear(256, board_size * board_size)
        )
        
        # --- CRITIC HEAD (The Judge) ---
        # Predicts the 'Value' of the current board state (how likely is Player 1 to win?)
        self.critic = nn.Sequential(
            nn.Linear(self.flatten_size, 256),
            nn.ReLU(),
            # Output is a single number representing the state value
            nn.Linear(256, 1)
        )

    def forward(self, x):
        """
        The forward pass: How data flows through the network.
        :param x: The input board state (Tensor)
        :return: Action probabilities and State Value
        """
        # 1. Pass through convolutional layers to extract features
        x = self.conv_block(x)
        
        # 2. Flatten the 3D feature map into a 1D vector for the linear layers
        x = x.view(x.size(0), -1) 
        
        # 3. Actor: Generate 'logits' (raw scores) and convert to probabilities using Softmax
        logits = self.actor(x)
        probs = F.softmax(logits, dim=-1) # All probabilities will sum to 1.0
        
        # 4. Critic: Generate a single value estimate for the current state
        value = self.critic(x)
        
        return probs, value