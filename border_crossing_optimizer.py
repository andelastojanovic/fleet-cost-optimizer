"""
Border Crossing Optimizer
-------------------------
Simulation of customs border congestion on the Trieste–Belgrade logistics corridor.

Author:
Andela Stojanovic

Purpose:
Estimate customs waiting times and identify congestion scenarios
to support logistics planning and resource allocation.
"""

from dataclasses import dataclass


@dataclass
class BorderCrossingResult:
    """Stores the simulation results."""

    status: str
    trucks_waiting: int
    waiting_time_hours: float
    total_capacity: int


class BorderCrossingOptimizer:
    """Simulates customs border capacity and congestion."""

    def __init__(self, gates_open: int):
        self.gates_open = gates_open
        self.capacity_per_gate = 15

    def simulate(self, arriving_trucks_per_hour: int) -> BorderCrossingResult:

        total_capacity = self.gates_open * self.capacity_per_gate

        if arriving_trucks_per_hour > total_capacity:

            queue = arriving_trucks_per_hour - total_capacity
            waiting_time = round(queue / total_capacity, 2)

            status = "CRITICAL"

        else:

            queue = 0
            waiting_time = 0.15
            status = "OPTIMAL"

        return BorderCrossingResult(
            status=status,
            trucks_waiting=queue,
            waiting_time_hours=waiting_time,
            total_capacity=total_capacity,
        )


def main():

    optimizer = BorderCrossingOptimizer(gates_open=3)

    result = optimizer.simulate(arriving_trucks_per_hour=50)

    print("\n=== BORDER CROSSING REPORT ===\n")

    print(f"Status: {result.status}")
    print(f"Total Capacity: {result.total_capacity} trucks/hour")
    print(f"Queue: {result.trucks_waiting} trucks")
    print(f"Estimated Waiting Time: {result.waiting_time_hours} hours")


if __name__ == "__main__":
    main()
