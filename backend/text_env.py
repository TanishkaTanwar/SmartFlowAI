from env import TrafficEnvironment


env = TrafficEnvironment()

state = env.reset()

print("🚦 Adaptive Flow - RL Environment")
print("---------------------------------")

print("Initial State:")
print(state)

for step in range(10):

    # For now, randomly choose an action
    action = 0

    next_state, reward, done, info = env.step(action)

    print(
        f"Step: {step + 1} | "
        f"Action: {action} | "
        f"Reward: {reward} | "
        f"State: {next_state}"
    )

    if done:
        break