import json
from ..utils.file_handler import FileHandler
from datetime import datetime


class RentalService:
    """Coordinate rentals/returns and persist the transaction history."""
    def __init__(self, vehicle_manager):
        self.rental_file = FileHandler("rentals.json")
        self.vehicle_manager = vehicle_manager
        self.rentals = self.load_rentals()

    def load_rentals(self):
        """Load previously saved rentals into memory."""
        return self.rental_file.read()

    def save_rentals(self):
        """Persist the current rentals list to disk."""
        self.rental_file.write(self.rentals)

    def rent_vehicle(self, renter_name, vehicle_id, days):
        """
        Reserve a vehicle for the requested number of days if it is available
        and append the transaction to the rental ledger.
        """
        vehicle = self.vehicle_manager.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return f"No vehicle found with ID {vehicle_id}."

        if not vehicle.available:
            return f"{vehicle.vehicle_type()} {vehicle_id} is already rented."

        # calculate cost using polymorphism (price_per_day)
        cost = vehicle.price_per_day * days

        # update state
        vehicle.available = False
        self.vehicle_manager.save_vehicles()

        rental_entry = {
            "renter": renter_name,
            "vehicle_id": vehicle_id,
            "days": days,
            "cost": cost,
            "date": datetime.today().isoformat()
        }

        self.rentals.append(rental_entry)
        self.save_rentals()

        return f"{renter_name} successfully rented {vehicle.vehicle_type()} {vehicle_id} for {days} days. Total cost: {cost}."

    def return_vehicle(self, vehicle_id):
        """Flip the vehicle's availability back to True and persist the change."""
        vehicle = self.vehicle_manager.get_vehicle_by_id(vehicle_id)

        if not vehicle:
            return f"Vehicle ID {vehicle_id} does not exist."

        if vehicle.available:
            return f"Vehicle {vehicle_id} is not currently rented."

        vehicle.available = True
        self.vehicle_manager.save_vehicles()

        return f"Vehicle {vehicle_id} has been returned successfully."

    def get_rent_history(self, reverse=True):
        """
        Return a date-sorted rental list (most recent first by default).
        reverse=True  → Most recent first
        reverse=False → Oldest first
        """
        return sorted(self.rentals, key=lambda r: datetime.strptime(r["date"], "%Y-%m-%d"),
        reverse=reverse)