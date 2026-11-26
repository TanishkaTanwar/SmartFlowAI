import random
import numpy as np

from simulator import TrafficSimulator
from controller import (
    FixedTimeController,
    RuleBasedController
)
from env import TrafficEnvironment
from qlearning import train_agent
from dqn import train_dqn


# ==================================================
# BASELINE CONTROLLERS
# ==================================================

def evaluate_baseline(controller_type, steps=200, seed=42):

    simulator = TrafficSimulator(seed=seed)

    if controller_type == "fixed":
        controller = FixedTimeController(green_time=5)

    elif controller_type == "rule":
        controller = RuleBasedController(
            minimum_green_time=3
        )

    else:
        raise ValueError("Unknown controller")

    total_queue = 0
    total_waiting = 0

    for _ in range(steps):

        controller.control(simulator)

        state = simulator.step()

        total_queue += state["queue"]

    # Actual cumulative waiting time
    total_waiting = simulator.total_waiting_time

    return {
        "average_queue": total_queue / steps,

        "average_waiting_time": (
            total_waiting / simulator.total_passed
            if simulator.total_passed > 0
            else 0
        ),

        "throughput": simulator.total_passed,

        "max_waiting_time": simulator.max_waiting_time
    }


# ==================================================
# Q-LEARNING EVALUATION
# ==================================================

def evaluate_q_learning(agent, steps=200, seed=42):

    env = TrafficEnvironment()

    # Make traffic reproducible
    env.simulator.seed = seed
    env.simulator.random = random.Random(seed)

    state = env.reset()

    # Disable exploration during evaluation
    old_epsilon = agent.epsilon
    agent.epsilon = 0.0

    total_queue = 0

    for _ in range(steps):

        action = agent.choose_action(state)

        next_state, reward, done, info = env.step(
            action
        )

        total_queue += info["queue"]

        state = next_state

        if done:
            break

    agent.epsilon = old_epsilon

    simulator = env.simulator

    actual_steps = simulator.time

    return {
        "average_queue": (
            total_queue / actual_steps
        ),

        "average_waiting_time": (
            simulator.total_waiting_time
            / simulator.total_passed
            if simulator.total_passed > 0
            else 0
        ),

        "throughput": simulator.total_passed,

        "max_waiting_time": simulator.max_waiting_time
    }


# ==================================================
# DQN EVALUATION
# ==================================================

def evaluate_dqn(agent, steps=200, seed=42):

    env = TrafficEnvironment()

    # Make traffic reproducible
    env.simulator.seed = seed
    env.simulator.random = random.Random(seed)

    state = env.reset()

    # Disable exploration
    old_epsilon = agent.epsilon
    agent.epsilon = 0.0

    total_queue = 0

    for _ in range(steps):

        action = agent.choose_action(state)

        next_state, reward, done, info = env.step(
            action
        )

        total_queue += info["queue"]

        state = next_state

        if done:
            break

    agent.epsilon = old_epsilon

    simulator = env.simulator

    actual_steps = simulator.time

    return {
        "average_queue": (
            total_queue / actual_steps
        ),

        "average_waiting_time": (
            simulator.total_waiting_time
            / simulator.total_passed
            if simulator.total_passed > 0
            else 0
        ),

        "throughput": simulator.total_passed,

        "max_waiting_time": simulator.max_waiting_time
    }


# ==================================================
# MAIN COMPARISON
# ==================================================

def compare_all_controllers():

    print("\n🚦 ADAPTIVE FLOW")
    print("=" * 70)

    # ------------------------------------------------
    # TRAIN Q-LEARNING
    # ------------------------------------------------

    print("\n🤖 Training Q-Learning...")

    q_agent, q_rewards = train_agent(
        episodes=500
    )

    # ------------------------------------------------
    # TRAIN DQN
    # ------------------------------------------------

    print("\n🧠 Training DQN...")

    dqn_agent, dqn_rewards = train_dqn(
        episodes=500
    )

    print("\n✅ Both RL agents trained successfully!")

    # ------------------------------------------------
    # EVALUATION
    # ------------------------------------------------

    results = {}

    print("\n🚦 Evaluating Fixed-Time...")
    results["Fixed-Time"] = evaluate_baseline(
        "fixed",
        steps=200,
        seed=42
    )

    print("🚦 Evaluating Rule-Based...")
    results["Rule-Based"] = evaluate_baseline(
        "rule",
        steps=200,
        seed=42
    )

    print("🤖 Evaluating Q-Learning...")
    results["Q-Learning"] = evaluate_q_learning(
        q_agent,
        steps=200,
        seed=42
    )

    print("🧠 Evaluating DQN...")
    results["DQN"] = evaluate_dqn(
        dqn_agent,
        steps=200,
        seed=42
    )

    # ------------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------------

    print("\n")
    print("=" * 95)

    print(
        "ADAPTIVE FLOW - CONTROLLER COMPARISON"
    )

    print("=" * 95)

    print(
        f"{'Controller':<20}"
        f"{'Avg Queue':<15}"
        f"{'Avg Wait Time':<18}"
        f"{'Throughput':<15}"
        f"{'Max Wait':<15}"
    )

    print("-" * 95)

    for name, result in results.items():

        print(
            f"{name:<20}"
            f"{result['average_queue']:<15.2f}"
            f"{result['average_waiting_time']:<18.2f}"
            f"{result['throughput']:<15}"
            f"{result['max_waiting_time']:<15}"
        )

    print("=" * 95)

    return results


# ==================================================
# PROGRAM START
# ==================================================

if __name__ == "__main__":

    results = compare_all_controllers()

    print(
        "\n🎉 Adaptive Flow evaluation completed!"
    )