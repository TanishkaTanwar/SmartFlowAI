from simulator import TrafficSimulator


class TrafficEnvironment:

    def __init__(self):
        self.simulator = TrafficSimulator()
        self.actions = [0, 1]

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.simulator.reset()

        return self.get_state()

    # --------------------------------------------------
    # STATE
    # --------------------------------------------------

    def get_state(self):

        state = (
            len(self.simulator.queues["north"]),
            len(self.simulator.queues["south"]),
            len(self.simulator.queues["east"]),
            len(self.simulator.queues["west"]),
            self.simulator.phase,
            self.simulator.phase_time
        )

        return state

    # --------------------------------------------------
    # STEP
    # --------------------------------------------------

    def step(self, action):

        # Action 1 = switch signal
        if action == 1:
            self.simulator.switch_signal()

        simulation_state = self.simulator.step()

        next_state = self.get_state()

        reward = self.calculate_reward()

        done = self.simulator.time >= 100

        return (
            next_state,
            reward,
            done,
            simulation_state
        )

    # --------------------------------------------------
    # REWARD
    # --------------------------------------------------

    def calculate_reward(self):

        total_queue = (
            len(self.simulator.queues["north"])
            + len(self.simulator.queues["south"])
            + len(self.simulator.queues["east"])
            + len(self.simulator.queues["west"])
        )

        # Lower queue = better reward
        reward = -total_queue

        return reward