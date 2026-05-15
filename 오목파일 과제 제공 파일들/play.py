import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import torch
import pygame
import sys
import numpy as np
from engine import OmokEngine
from model import PPOModel

# --- UI CONSTANTS ---
BOARD_SIZE = 10
CELL_SIZE = 60
SIDEBAR_WIDTH = 250
PADDING = 60
SCREEN_WIDTH = (BOARD_SIZE * CELL_SIZE) + PADDING + SIDEBAR_WIDTH
SCREEN_HEIGHT = (BOARD_SIZE * CELL_SIZE) + PADDING
COLOR_BG = (28, 28, 38)
COLOR_SIDEBAR = (35, 35, 50)
COLOR_BOARD = (210, 170, 110)
COLOR_GRID = (45, 45, 55)
COLOR_ACCENT = (0, 255, 200)

class ModernOmok:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OMOK - SANKALPA EDITION")
        self.font_m = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_s = pygame.font.SysFont("Segoe UI", 18)
        self.clock = pygame.time.Clock()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = PPOModel(BOARD_SIZE).to(self.device)
        self.load_model()
        self.reset_game()

    def load_model(self):
        model_path = "ppo_omok_reward.pth"
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            self.model_status = "LOADED"
        else:
            self.model_status = "RANDOM MODE"

    def reset_game(self):
        self.env = OmokEngine(BOARD_SIZE)
        self.last_move = None
        self.game_over_fade = 0

    def draw_glass_rect(self, rect, color, alpha):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*color, alpha))
        self.screen.blit(s, (rect.x, rect.y))

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # --- DRAW SIDEBAR ---
        pygame.draw.rect(self.screen, COLOR_SIDEBAR, (SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.font_m.render("OMOK", True, COLOR_ACCENT), (SCREEN_WIDTH - SIDEBAR_WIDTH + 30, 40))
        self.screen.blit(self.font_s.render(f"STATUS: {self.model_status}", True, (150, 150, 150)), (SCREEN_WIDTH - SIDEBAR_WIDTH + 30, 80))
        
        # Turn Indicator
        turn_txt = "YOUR TURN" if self.env.current_player == 1 else "AI THINKING..."
        turn_clr = (255, 255, 255) if self.env.current_player == 1 else COLOR_ACCENT
        self.screen.blit(self.font_s.render(turn_txt, True, turn_clr), (SCREEN_WIDTH - SIDEBAR_WIDTH + 30, 150))

        # Instructions
        self.screen.blit(self.font_s.render("PRESS 'R' TO RESTART", True, (100, 100, 100)), (SCREEN_WIDTH - SIDEBAR_WIDTH + 30, SCREEN_HEIGHT - 60))

        # --- DRAW BOARD ---
        board_rect = pygame.Rect(PADDING//2, PADDING//2, BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect, border_radius=10)
        
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (PADDING, PADDING + i*CELL_SIZE), (BOARD_SIZE*CELL_SIZE, PADDING + i*CELL_SIZE), 1)
            pygame.draw.line(self.screen, COLOR_GRID, (PADDING + i*CELL_SIZE, PADDING), (PADDING + i*CELL_SIZE, BOARD_SIZE*CELL_SIZE), 1)

        # --- DRAW STONES ---
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                pos = (PADDING + c * CELL_SIZE, PADDING + r * CELL_SIZE)
                if self.env.board[r, c] == 1: # Black
                    pygame.draw.circle(self.screen, (20, 20, 25), (pos[0]+2, pos[1]+2), 22) # Shadow
                    pygame.draw.circle(self.screen, (10, 10, 15), pos, 22)
                    pygame.draw.circle(self.screen, (60, 60, 70), (pos[0]-6, pos[1]-6), 6)
                elif self.env.board[r, c] == 2: # White
                    pygame.draw.circle(self.screen, (150, 150, 160), (pos[0]+2, pos[1]+2), 22) # Shadow
                    pygame.draw.circle(self.screen, (240, 240, 250), pos, 22)
                    pygame.draw.circle(self.screen, (255, 255, 255), (pos[0]-6, pos[1]-6), 7)

        if self.last_move:
            pygame.draw.circle(self.screen, (255, 50, 50), (PADDING + self.last_move[1]*CELL_SIZE, PADDING + self.last_move[0]*CELL_SIZE), 6)

        # --- GAME OVER OVERLAY ---
        if self.env.is_over:
            self.draw_glass_rect(pygame.Rect(0,0, SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0), 180)
            msg = "VICTORY!" if self.env.winner == 1 else "DEFEAT!" if self.env.winner == 2 else "DRAW"
            color = (0, 255, 150) if self.env.winner == 1 else (255, 80, 80)
            txt = self.font_m.render(msg, True, color)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2 - 100, SCREEN_HEIGHT//2 - 20))
            sub_txt = self.font_s.render("PRESS 'R' TO PLAY AGAIN", True, (200, 200, 200))
            self.screen.blit(sub_txt, (SCREEN_WIDTH//2 - sub_txt.get_width()//2 - 100, SCREEN_HEIGHT//2 + 30))

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()
            
            if not self.env.is_over:
                if self.env.current_player == 1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset_game()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            c, r = round((mx-PADDING)/CELL_SIZE), round((my-PADDING)/CELL_SIZE)
                            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                                if self.env.make_move(r, c): self.last_move = (r, c)
                else:
                    pygame.time.wait(600)
                    state = torch.FloatTensor(self.env.get_state()).unsqueeze(0).to(self.device)
                    with torch.no_grad(): probs, _ = self.model(state)
                    mask = torch.zeros(BOARD_SIZE * BOARD_SIZE).to(self.device)
                    for m in self.env.get_valid_moves(): mask[m[0]*BOARD_SIZE + m[1]] = 1
                    probs = probs.squeeze() * mask
                    action = torch.argmax(probs).item() if probs.sum() > 0 else np.random.choice([m[0]*BOARD_SIZE + m[1] for m in self.env.get_valid_moves()])
                    r, c = divmod(action, BOARD_SIZE)
                    self.env.make_move(r, c)
                    self.last_move = (r, c)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset_game()
            
            self.clock.tick(60)

    def resource_path(relative_path):
        try:
            
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    model_file_path = resource_path("ppo_omok_reward.pth")

if __name__ == "__main__":
    ModernOmok().run()