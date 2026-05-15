import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
from model import PPOModel

class PPOAgent:
    def __init__(self, board_size, lr=3e-4, gamma=0.99, eps_clip=0.2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.board_size = board_size
        self.gamma = gamma
        self.eps_clip = eps_clip
        
        self.policy = PPOModel(board_size).to(self.device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.policy_old = PPOModel(board_size).to(self.device)
        self.policy_old.load_state_dict(self.policy.state_dict())
        self.MseLoss = nn.MSELoss()

    def select_action(self, state, valid_moves):
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            probs, _ = self.policy_old(state)
        
        mask = torch.zeros(self.board_size * self.board_size).to(self.device)
        for m in valid_moves:
            mask[m[0] * self.board_size + m[1]] = 1
        
        masked_probs = probs.squeeze() * mask
        if masked_probs.sum() > 0:
            masked_probs = masked_probs / masked_probs.sum()
        else:
            masked_probs = mask / mask.sum()

        dist = Categorical(masked_probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def update(self, memory):
        states = torch.stack(memory.states).to(self.device).detach()
        actions = torch.stack(memory.actions).to(self.device).detach()
        logprobs = torch.stack(memory.logprobs).to(self.device).detach()
        rewards = torch.tensor(memory.rewards).to(self.device).detach().float()
        
        if len(rewards) > 1:
            rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-5)

        for _ in range(10):
            probs, state_values = self.policy(states)
            dist = Categorical(probs)
            new_logprobs = dist.log_prob(actions)
            entropy = dist.entropy()
            
            ratios = torch.exp(new_logprobs - logprobs)
            advantages = rewards - state_values.detach().squeeze()
            
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1-self.eps_clip, 1+self.eps_clip) * advantages
            
            loss = -torch.min(surr1, surr2) + 0.5 * self.MseLoss(state_values.squeeze(), rewards) - 0.01 * entropy
            self.optimizer.zero_grad()
            loss.mean().backward()
            self.optimizer.step()
        
        self.policy_old.load_state_dict(self.policy.state_dict())
        return loss.mean().item()

class Memory:
    def __init__(self):
        self.states, self.actions, self.logprobs, self.rewards = [], [], [], []
    def clear(self):
        self.states.clear(); self.actions.clear(); self.logprobs.clear(); self.rewards.clear()