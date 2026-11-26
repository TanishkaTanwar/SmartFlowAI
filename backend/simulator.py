import random


class Vehicle:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.waiting_time = 0


class TrafficSimulator:
    def __init__(self, seed=42):
        self.seed = seed
        self.random = random.Random(seed)

        self.time = 0

        self.queues = {
            "north": [],
            "south": [],
            "east": [],
            "west": []
        }

        self.phase = "NS"
        self.phase_time = 0

        self.total_passed = 0
        self.total_waiting_time = 0
        self.max_waiting_time = 0

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):
        self.time = 0

        self.queues = {
            "north": [],
            "south": [],
            "east": [],
            "west": []
        }

        self.phase = "NS"
        self.phase_time = 0

        self.total_passed = 0
        self.total_waiting_time = 0
        self.max_waiting_time = 0

        self.random = random.Random(self.seed)

    # --------------------------------------------------
    # TRAFFIC GENERATION
    # --------------------------------------------------

    def generate_traffic(self):
        """
        Generate new vehicles at each approach.

        Currently uses a simple random arrival model.
        """

        approaches = ["north", "south", "east", "west"]

        for approach in approaches:

            arrivals = self.random.randint(0, 3)

            for _ in range(arrivals):
                vehicle = Vehicle(arrival_time=self.time)
                self.queues[approach].append(vehicle)

    # --------------------------------------------------
    # UPDATE WAITING TIME
    # --------------------------------------------------

    def update_waiting_times(self):

        for approach in self.queues:

            for vehicle in self.queues[approach]:
                vehicle.waiting_time += 1

                self.total_waiting_time += 1

                self.max_waiting_time = max(
                    self.max_waiting_time,
                    vehicle.waiting_time
                )

    # --------------------------------------------------
    # MOVE VEHICLES
    # --------------------------------------------------

    def move_vehicles(self):

        vehicles_passed = 0

        if self.phase == "NS":

            north_pass = min(
                len(self.queues["north"]),
                2
            )

            south_pass = min(
                len(self.queues["south"]),
                2
            )

            del self.queues["north"][:north_pass]
            del self.queues["south"][:south_pass]

            vehicles_passed = north_pass + south_pass

        elif self.phase == "EW":

            east_pass = min(
                len(self.queues["east"]),
                2
            )

            west_pass = min(
                len(self.queues["west"]),
                2
            )

            del self.queues["east"][:east_pass]
            del self.queues["west"][:west_pass]

            vehicles_passed = east_pass + west_pass

        self.total_passed += vehicles_passed

        return vehicles_passed

    # --------------------------------------------------
    # SWITCH SIGNAL
    # --------------------------------------------------

    def switch_signal(self):

        if self.phase == "NS":
            self.phase = "EW"
        else:
            self.phase = "NS"

        self.phase_time = 0

    # --------------------------------------------------
    # CURRENT QUEUE LENGTH
    # --------------------------------------------------

    def get_queue_lengths(self):

        return {
            "north": len(self.queues["north"]),
            "south": len(self.queues["south"]),
            "east": len(self.queues["east"]),
            "west": len(self.queues["west"])
        }

    # --------------------------------------------------
    # TOTAL QUEUE
    # --------------------------------------------------

    def get_total_queue(self):

        return sum(
            len(queue)
            for queue in self.queues.values()
        )

    # --------------------------------------------------
    # SIMULATION STEP
    # --------------------------------------------------

    def step(self):

        self.time += 1
        self.phase_time += 1

        # New vehicles arrive
        self.generate_traffic()

        # Vehicles waiting at this timestep
        self.update_waiting_times()

        # Vehicles move if their signal is green
        vehicles_passed = self.move_vehicles()

        queue_lengths = self.get_queue_lengths()

        total_queue = sum(queue_lengths.values())

        return {
            "time": self.time,

            "north": queue_lengths["north"],
            "south": queue_lengths["south"],
            "east": queue_lengths["east"],
            "west": queue_lengths["west"],

            "phase": self.phase,
            "phase_time": self.phase_time,

            "queue": total_queue,

            "waiting_time": self.total_waiting_time,

            "max_waiting_time": self.max_waiting_time,

            "vehicles_passed": vehicles_passed,

            "total_passed": self.total_passed
        }


# --------------------------------------------------
# TEST THE SIMULATOR
# --------------------------------------------------

if __name__ == "__main__":

    simulator = TrafficSimulator(seed=42)

    print("🚦 Adaptive Flow - Improved Traffic Simulator")
    print("----------------------------------------------")

    for _ in range(20):

        state = simulator.step()

        print(
            f"Time: {state['time']:2d} | "
            f"N: {state['north']:2d} | "
            f"S: {state['south']:2d} | "
            f"E: {state['east']:2d} | "
            f"W: {state['west']:2d} | "
            f"Signal: {state['phase']} | "
            f"Queue: {state['queue']:2d} | "
            f"Passed: {state['total_passed']:2d} | "
            f"Max Wait: {state['max_waiting_time']:2d}"
        )

        if simulator.phase_time >= 5:
            simulator.switch_signal()