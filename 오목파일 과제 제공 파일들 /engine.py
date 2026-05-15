import numpy as np

class OmokEngine:
    def __init__(self, board_size=10):
        """
        Initialize the Omok (Gomoku) game engine.
        :param board_size: The width and height of the square board.
        """
        self.board_size = board_size
        self.reset()

    def reset(self):
        """
        Resets the game state to start a new match.
        Returns the initial empty board state.
        """
        # Create a 2D array filled with zeros (0 = empty, 1 = Player 1, 2 = Player 2)
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1 
        self.is_over = False
        self.winner = None
        return self.get_state()

    def get_state(self):
        """
        Converts the board into a format suitable for the Neural Network (CNN).
        Returns a 3D float32 tensor of shape (1, board_size, board_size).
        """
        return self.board.copy().reshape(1, self.board_size, self.board_size).astype(np.float32)

    def get_valid_moves(self):
        """
        Finds all empty cells where a move is allowed.
        Returns an array of [row, col] coordinates.
        """
        return np.argwhere(self.board == 0)

    def make_move(self, row, col):
        """
        Executes a move for the current player.
        :param row: Row index to place the stone.
        :param col: Column index to place the stone.
        :return: True if move was successful, False if invalid.
        """
        # Validate move: Check if the spot is taken or if the game has ended
        if self.board[row, col] != 0 or self.is_over:
            return False
        
        # Place the stone for the current player
        self.board[row, col] = self.current_player
        
        # Check if this move resulted in a win
        if self.check_win(row, col):
            self.is_over = True
            self.winner = self.current_player
        # Check for a draw (no empty cells left)
        elif not np.any(self.board == 0):
            self.is_over = True
            self.winner = 0 # 0 indicates a draw
            
        # Switch turn: If 1 becomes 2, if 2 becomes 1
        self.current_player = 3 - self.current_player
        return True

    def check_win(self, r, c):
        """
        Checks if the last move placed at (r, c) created a line of 5 or more.
        """
        player = self.board[r, c]
        # Directions: Horizontal, Vertical, Diagonal (\), Anti-diagonal (/)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            # Check in both directions along the line (e.g., Left and Right)
            for sign in [1, -1]:
                nr, nc = r + dr * sign, c + dc * sign
                # Stay within board boundaries and match player stone
                while 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr, nc] == player:
                    count += 1
                    nr += dr * sign
                    nc += dc * sign
            
            # If 5 or more in a row are found, the player wins
            if count >= 5: return True
        return False

    def check_patterns(self, player, length):
        """
        Scans the entire board to find a sequence of stones of a specific 'length'.
        Used for Reward Shaping (e.g., giving the AI points for creating a 3-in-a-row).
        """
        # Directions: Horizontal, Vertical, Diagonal, Anti-diagonal
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(self.board_size):
            for c in range(self.board_size):
                # If the cell belongs to the player we are checking
                if self.board[r, c] == player:
                    for dr, dc in directions:
                        count = 1
                        nr, nc = r + dr, c + dc
                        
                        # Trace the line in the current direction
                        while 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr, nc] == player:
                            count += 1
                            nr += dr
                            nc += dc
                        
                        # If a sequence of the exact length is found
                        if count == length:
                            return True
        return False
