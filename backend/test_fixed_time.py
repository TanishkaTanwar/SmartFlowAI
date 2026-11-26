from simulator import TrafficSimulator
from controller import FixedTimeController


simulator = TrafficSimulator()

controller = FixedTimeController(green_time=5)


print("🚦 Adaptive Flow - Fixed-Time Controller")
print("----------------------------------------")

for step in range(20):

    # Controller decides whether to change signal
    controller.control(simulator)

    # Run simulation
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