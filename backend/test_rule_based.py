from simulator import TrafficSimulator
from controller import RuleBasedController


simulator = TrafficSimulator()

controller = RuleBasedController(
    minimum_green_time=3
)

print("🚦 Adaptive Flow - Rule-Based Controller")
print("----------------------------------------")

for step in range(30):

    # Controller looks at traffic
    controller.control(simulator)

    # Run one simulation step
    state = simulator.step()

    print(
        f"Time: {state['time']:2d} | "
        f"N: {state['north']:2d} | "
        f"S: {state['south']:2d} | "
        f"E: {state['east']:2d} | "
        f"W: {state['west']:2d} | "
        f"Signal: {state['phase']} | "
        f"Waiting: {state['waiting']:2d} | "
        f"Passed: {state['total_passed']:2d}"
    )