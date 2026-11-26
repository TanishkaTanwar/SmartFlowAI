from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulator import TrafficSimulator

app = FastAPI(title="Adaptive Flow API")


# Allow our React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create simulator
simulator = TrafficSimulator(seed=42)


@app.get("/")
def home():
    return {
        "project": "Adaptive Flow",
        "message": "Adaptive Flow API is running 🚦"
    }


@app.get("/traffic")
def get_traffic():
    return {
        "time": simulator.time,
        "north": len(simulator.queues["north"]),
        "south": len(simulator.queues["south"]),
        "east": len(simulator.queues["east"]),
        "west": len(simulator.queues["west"]),
        "phase": simulator.phase,
        "phase_time": simulator.phase_time,
        "total_queue": simulator.get_total_queue(),
        "total_passed": simulator.total_passed,
        "max_waiting_time": simulator.max_waiting_time,
    }


@app.post("/step")
def simulation_step():
    state = simulator.step()

    return {
        "time": state["time"],
        "north": state["north"],
        "south": state["south"],
        "east": state["east"],
        "west": state["west"],
        "phase": state["phase"],
        "phase_time": state["phase_time"],
        "queue": state["queue"],
        "total_passed": state["total_passed"],
        "max_waiting_time": state["max_waiting_time"],
    }


@app.post("/switch")
def switch_signal():
    simulator.switch_signal()

    return {
        "phase": simulator.phase,
        "phase_time": simulator.phase_time,
    }


@app.post("/reset")
def reset_simulator():
    simulator.reset()

    return {
        "message": "Simulator reset",
        "phase": simulator.phase,
        "time": simulator.time,
    }