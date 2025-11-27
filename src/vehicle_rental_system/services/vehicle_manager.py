import json
from pathlib import Path

from ..models.car import Car
from ..models.bike import Bike
from ..models.truck import Truck
from ..utils.file_handler import FileHandler


class VehicleManager:
    """Persist vehicles to disk and provide query helpers for the CLI/services."""
    def __init__(self):
        self.vehicles_file = FileHandler('vehicles.json')
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
        """Instantiate Vehicle subclasses from the serialized JSON records."""
        data = self.vehicles_file.read()
        vehicles = []
        for v in data:
            vtype = v["type"]
            if vtype == "Car":
                vehicles.append(Car(**v))
            elif vtype == "Bike":
                vehicles.append(Bike(**v))
            elif vtype == "Truck":
                vehicles.append(Truck(**v))
            else:
                continue  # ignore unknown types
        return vehicles

    def save_vehicles(self):
        """Write the in-memory vehicle state back to the JSON file."""
        data = []
        for v in self.vehicles:
            data.append({
                "vehicle_id": v.vehicle_id,
                "type": v.vehicle_type(),
                "brand": v.brand,
                "model": v.model,
                "base_price": v.price_per_day,
                "available": v.available
            })

        self.vehicles_file.write(data)

    def get_vehicle_by_id(self, vehicle_id):
        """Return the vehicle matching the identifier or None if missing."""
        return next((v for v in self.vehicles if int(v.vehicle_id) == int(vehicle_id)), None)

    def get_vehicles_by_brand(self, vehicle_brand):
        """Filter vehicles by exact brand name (case-insensitive)."""
        return [v for v in self.vehicles if v.brand.lower() == vehicle_brand.lower()]
    
    def get_vehicles_by_type(self, vehicle_type):
        """Filter vehicles by their declared type string (case-insensitive)."""
        return [v for v in self.vehicles if v.type.lower() == vehicle_type.lower()]
    
    def list_available(self):
        """Return only vehicles that are currently free to rent."""
        return [v for v in self.vehicles if v.available]

    def list_rented(self):
        """Return only vehicles that are currently checked out."""
        return [v for v in self.vehicles if not v.available]
