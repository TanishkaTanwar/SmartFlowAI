import random
from collections import defaultdict

from env import TrafficEnvironment


class QLearningAgent:

    def __init__(
        self,
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05
    ):

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.q_table = defaultdict(
            lambda: [0.0, 0.0]
        )

    # --------------------------------------------------
    # DISCRETIZE STATE
    # --------------------------------------------------

    def get_state(self, state):

        north, south, east, west, phase, phase_time = state

        north = min(north // 5, 10)
        south = min(south // 5, 10)
        east = min(east // 5, 10)
        west = min(west // 5, 10)

        phase_time = min(
            phase_time // 5,
            10
        )

        return (
            north,
            south,
            east,
            west,
            phase,
            phase_time
        )

    # --------------------------------------------------
    # ACTION
    # --------------------------------------------------

    def choose_action(self, state):

        state = self.get_state(state)

        # Exploration
        if random.random() < self.epsilon:
            return random.choice([0, 1])

        # Exploitation
        q_values = self.q_table[state]

        return q_values.index(
            max(q_values)
        )

    # --------------------------------------------------
    # UPDATE Q TABLE
    # --------------------------------------------------

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        state = self.get_state(state)
        next_state = self.get_state(next_state)

        current_q = self.q_table[state][action]

        max_next_q = max(
            self.q_table[next_state]
        )

        new_q = current_q + self.learning_rate * (
            reward
            + self.discount_factor * max_next_q
            - current_q
        )

        self.q_table[state][action] = new_q

    # --------------------------------------------------
    # EPSILON DECAY
    # --------------------------------------------------

    def decay_epsilon(self):

        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )


# --------------------------------------------------
# TRAINING
# --------------------------------------------------

def train_agent(episodes=500):

    env = TrafficEnvironment()

    agent = QLearningAgent()

    rewards_per_episode = []

    print(
        "🤖 Training Adaptive Flow Q-Learning Agent"
    )

    print(
        "------------------------------------------"
    )

    for episode in range(episodes):

        state = env.reset()

        total_reward = 0

        done = False

        while not done:

            action = agent.choose_action(
                state
            )

            next_state, reward, done, _ = (
                env.step(action)
            )

            agent.update(
                state,
                action,
                reward,
                next_state
            )

            state = next_state

            total_reward += reward

        agent.decay_epsilon()

        rewards_per_episode.append(
            total_reward
        )

        if (episode + 1) % 50 == 0:

            print(
                f"Episode: {episode + 1:3d} | "
                f"Reward: {total_reward:8.2f} | "
                f"Epsilon: {agent.epsilon:.3f}"
            )

    return agent, rewards_per_episode


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    agent, rewards = train_agent(
        episodes=500
    )

    print(
        "\n✅ Q-Learning training completed!"
    )

    print(
        f"Final epsilon: {agent.epsilon:.3f}"
    )

    print(
        f"Number of learned states: "
        f"{len(agent.q_table)}"
    )