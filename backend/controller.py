class FixedTimeController:
    def __init__(self, green_time=5):
        self.green_time = green_time

    def control(self, simulator):

        if simulator.phase_time >= self.green_time:
            simulator.switch_signal()

        return simulator.phase


class RuleBasedController:
    def __init__(self, minimum_green_time=3):
        self.minimum_green_time = minimum_green_time

    def control(self, simulator):

        # Don't switch too quickly
        if simulator.phase_time < self.minimum_green_time:
            return simulator.phase

        north_south_queue = (
            len(simulator.queues["north"])
            + len(simulator.queues["south"])
        )

        east_west_queue = (
            len(simulator.queues["east"])
            + len(simulator.queues["west"])
        )

        if north_south_queue > east_west_queue:
            desired_phase = "NS"

        elif east_west_queue > north_south_queue:
            desired_phase = "EW"

        else:
            desired_phase = simulator.phase

        if desired_phase != simulator.phase:
            simulator.switch_signal()

        return simulator.phase