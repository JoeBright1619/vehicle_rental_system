import json
from ..utils.file_handler import FileHandler
from datetime import date


class RentalService:
    def __init__(self, vehicle_manager):
        self.rental_file = FileHandler("rentals.json")
        self.vehicle_manager = vehicle_manager
        self.rentals = self.load_rentals()

    def load_rentals(self):
        return self.rental_file.read()

    def save_rentals(self):
        self.rental_file(self.rentals)

    def rent_vehicle(self, renter_name, vehicle_id, days):
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
            "date": date.today().isoformat()
        }

        self.rentals.append(rental_entry)
        self.save_rentals()

        return f"{renter_name} successfully rented {vehicle.vehicle_type()} {vehicle_id} for {days} days. Total cost: {cost}."

    def return_vehicle(self, vehicle_id):
        vehicle = self.vehicle_manager.get_vehicle_by_id(vehicle_id)

        if not vehicle:
            return f"Vehicle ID {vehicle_id} does not exist."

        if vehicle.available:
            return f"Vehicle {vehicle_id} is not currently rented."

        vehicle.available = True
        self.vehicle_manager.save_vehicles()

        return f"Vehicle {vehicle_id} has been returned successfully."
