import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from env import TrafficEnvironment


# ==================================================
# DQN NEURAL NETWORK
# ==================================================

class DQN(nn.Module):

    def __init__(self, state_size, action_size):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(state_size, 64),
            nn.ReLU(),

            nn.Linear(64, 64),
            nn.ReLU(),

            nn.Linear(64, action_size)
        )

    def forward(self, state):

        return self.network(state)


# ==================================================
# REPLAY BUFFER
# ==================================================

class ReplayBuffer:

    def __init__(self, capacity=10000):

        self.buffer = deque(
            maxlen=capacity
        )

    def add(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        self.buffer.append(
            (
                state,
                action,
                reward,
                next_state,
                done
            )
        )

    def sample(self, batch_size):

        batch = random.sample(
            self.buffer,
            batch_size
        )

        states, actions, rewards, next_states, dones = zip(
            *batch
        )

        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32)
        )

    def __len__(self):

        return len(self.buffer)


# ==================================================
# DQN AGENT
# ==================================================

class DQNAgent:

    def __init__(
        self,
        state_size=6,
        action_size=2
    ):

        self.state_size = state_size
        self.action_size = action_size

        # Learning parameters
        self.gamma = 0.95

        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

        self.learning_rate = 0.001

        # Networks
        self.policy_network = DQN(
            state_size,
            action_size
        )

        self.target_network = DQN(
            state_size,
            action_size
        )

        # Initially both networks are identical
        self.target_network.load_state_dict(
            self.policy_network.state_dict()
        )

        self.target_network.eval()

        # Optimizer
        self.optimizer = optim.Adam(
            self.policy_network.parameters(),
            lr=self.learning_rate
        )

        self.loss_function = nn.MSELoss()

        # Replay memory
        self.memory = ReplayBuffer(
            capacity=10000
        )

    # ------------------------------------------------
    # CONVERT ENVIRONMENT STATE TO NUMPY ARRAY
    # ------------------------------------------------

    def prepare_state(self, state):

        north, south, east, west, phase, phase_time = state

        # Convert phase to numerical value
        phase_value = 0 if phase == "NS" else 1

        # Normalize queue values
        north = min(north / 20.0, 1.0)
        south = min(south / 20.0, 1.0)
        east = min(east / 20.0, 1.0)
        west = min(west / 20.0, 1.0)

        # Normalize phase time
        phase_time = min(
            phase_time / 20.0,
            1.0
        )

        return np.array(
            [
                north,
                south,
                east,
                west,
                phase_value,
                phase_time
            ],
            dtype=np.float32
        )

    # ------------------------------------------------
    # CHOOSE ACTION
    # ------------------------------------------------

    def choose_action(self, state):

        state = self.prepare_state(state)

        # Exploration
        if random.random() < self.epsilon:

            return random.randrange(
                self.action_size
            )

        # Exploitation
        state_tensor = torch.tensor(
            state,
            dtype=torch.float32
        ).unsqueeze(0)

        with torch.no_grad():

            q_values = self.policy_network(
                state_tensor
            )

        return q_values.argmax(
            dim=1
        ).item()

    # ------------------------------------------------
    # STORE EXPERIENCE
    # ------------------------------------------------

    def remember(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        state = self.prepare_state(state)

        next_state = self.prepare_state(
            next_state
        )

        self.memory.add(
            state,
            action,
            reward,
            next_state,
            done
        )

    # ------------------------------------------------
    # TRAIN NETWORK
    # ------------------------------------------------

    def train_step(self, batch_size=64):

        if len(self.memory) < batch_size:

            return None

        (
            states,
            actions,
            rewards,
            next_states,
            dones
        ) = self.memory.sample(
            batch_size
        )

        states = torch.tensor(
            states,
            dtype=torch.float32
        )

        actions = torch.tensor(
            actions,
            dtype=torch.long
        )

        rewards = torch.tensor(
            rewards,
            dtype=torch.float32
        )

        next_states = torch.tensor(
            next_states,
            dtype=torch.float32
        )

        dones = torch.tensor(
            dones,
            dtype=torch.float32
        )

        # Current Q-values
        current_q_values = (
            self.policy_network(states)
            .gather(
                1,
                actions.unsqueeze(1)
            )
            .squeeze(1)
        )

        # Target Q-values
        with torch.no_grad():

            next_q_values = (
                self.target_network(
                    next_states
                )
                .max(dim=1)[0]
            )

            target_q_values = (
                rewards
                + self.gamma
                * next_q_values
                * (1 - dones)
            )

        # Calculate loss
        loss = self.loss_function(
            current_q_values,
            target_q_values
        )

        # Backpropagation
        self.optimizer.zero_grad()

        loss.backward()

        self.optimizer.step()

        return loss.item()

    # ------------------------------------------------
    # EPSILON DECAY
    # ------------------------------------------------

    def decay_epsilon(self):

        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

    # ------------------------------------------------
    # UPDATE TARGET NETWORK
    # ------------------------------------------------

    def update_target_network(self):

        self.target_network.load_state_dict(
            self.policy_network.state_dict()
        )


# ==================================================
# TRAIN DQN
# ==================================================

def train_dqn(episodes=500):

    env = TrafficEnvironment()

    agent = DQNAgent()

    rewards = []

    print(
        "🧠 Training Adaptive Flow DQN Agent"
    )

    print(
        "-----------------------------------"
    )

    for episode in range(episodes):

        state = env.reset()

        total_reward = 0

        done = False

        while not done:

            action = agent.choose_action(
                state
            )

            (
                next_state,
                reward,
                done,
                _
            ) = env.step(action)

            agent.remember(
                state,
                action,
                reward,
                next_state,
                done
            )

            agent.train_step(
                batch_size=64
            )

            state = next_state

            total_reward += reward

        # Reduce exploration
        agent.decay_epsilon()

        # Update target network
        if (episode + 1) % 10 == 0:

            agent.update_target_network()

        rewards.append(
            total_reward
        )

        if (episode + 1) % 50 == 0:

            print(
                f"Episode: {episode + 1:3d} | "
                f"Reward: {total_reward:8.2f} | "
                f"Epsilon: {agent.epsilon:.3f}"
            )

    return agent, rewards


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    agent, rewards = train_dqn(
        episodes=500
    )

    print(
        "\n✅ DQN training completed!"
    )

    print(
        f"Final epsilon: {agent.epsilon:.3f}"
    )

    print(
        f"Replay memory size: "
        f"{len(agent.memory)}"
    )