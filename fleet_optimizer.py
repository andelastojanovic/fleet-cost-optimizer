"""Fleet Cost and Maintenance Optimizer.

This script analyzes fleet vehicle data to predict maintenance needs
and optimize corporate operational costs.
"""

import pandas as pd


class FleetOptimizer:
    """Manages fleet data to optimize maintenance schedules and costs."""

    def __init__(self, maintenance_budget: float):
        """Initializes the optimizer with a total available budget."""
        self.budget = maintenance_budget
        self.fleet_data = None

    def load_fleet_data(self, data_dict: dict) -> pd.DataFrame:
        """Loads vehicle asset data into a pandas DataFrame."""
        self.fleet_data = pd.DataFrame(data_dict)
        return self.fleet_data

    def calculate_risk_score(self) -> pd.DataFrame:
        """Calculates a dynamic risk score for each vehicle."""
        if self.fleet_data is None:
            raise ValueError("No fleet data loaded.")

        # Risk Formula: 60% Mileage weight + 40% Age weight
        self.fleet_data["Risk_Score"] = (
            (self.fleet_data["Mileage"] / 150000) * 0.6
            + (self.fleet_data["Age_Years"] / 10) * 0.4
        ).round(2)

        # Flag urgent maintenance if risk exceeds threshold
        self.fleet_data["Urgent_Action"] = self.fleet_data["Risk_Score"] > 0.75
        return self.fleet_data

    def optimize_budget(self) -> tuple[pd.DataFrame, float]:
        """Allocates budget to high-risk vehicles and calculates cost savings."""
        if "Risk_Score" not in self.fleet_data.columns:
            self.calculate_risk_score()

        # Sort by risk to prioritize budget allocation
        sorted_fleet = self.fleet_data.sort_values(
            by="Risk_Score", ascending=False
        )

        allocated_budget = 0.0
        prevented_damage_costs = 0.0
        selected_vehicles = []

        for _, vehicle in sorted_fleet.iterrows():
            cost = vehicle["Est_Maintenance_Cost"]
            if allocated_budget + cost <= self.budget and vehicle["Urgent_Action"]:
                allocated_budget += cost
                # Preventing a breakdown saves 3x the maintenance cost
                prevented_damage_costs += cost * 3.0
                selected_vehicles.append(vehicle["Vehicle_ID"])

        net_savings = prevented_damage_costs - allocated_budget

        # Add allocation flag
        self.fleet_data["Budget_Allocated"] = self.fleet_data["Vehicle_ID"].isin(
            selected_vehicles
        )

        return self.fleet_data, net_savings


# --- Execution Example ---
if __name__ == "__main__":
    # Simulated corporate fleet data
    mock_data = {
        "Vehicle_ID": ["V-01", "V-02", "V-03", "V-04", "V-05"],
        "Mileage": [140000, 45000, 160000, 30000, 125000],
        "Age_Years": [8, 2, 9, 1, 7],
        "Est_Maintenance_Cost": [1200, 400, 1500, 300, 1100],
    }

    # Initialize with a fixed corporate budget of 3000 EUR
    optimizer = FleetOptimizer(maintenance_budget=3000.0)
    optimizer.load_fleet_data(mock_data)
    optimizer.calculate_risk_score()
    final_report, total_savings = optimizer.optimize_budget()

    print("=== FLEET OPTIMIZATION REPORT ===")
    print(final_report[["Vehicle_ID", "Risk_Score", "Urgent_Action", "Budget_Allocated"]])
    print(f"\nTotal Net Savings Generated: {total_savings} EUR")
