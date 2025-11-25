import json
from pathlib import Path

from ..models.car import Car
from ..models.bike import Bike
from ..models.truck import Truck
from ..utils.file_handler import FileHandler


class VehicleManager:
    def __init__(self):
        self.vehicles_file = FileHandler('vehicles')
        self.vehicles = self.load_vehicles()

    def load_vehicles(self):
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
        data = []
        for v in self.vehicles:
            data.append({
                "vehicle_id": v.vehicle_id,
                "type": v.vehicle_type(),
                "brand": v.brand,
                "model": v.model,
                "base_price": v.base_price,
                "available": v.available
            })

        self.vehicles_file.write(data)

    def get_vehicle_by_id(self, vehicle_id):
        return next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)

    def list_available(self):
        return [v for v in self.vehicles if v.available]

    def list_rented(self):
        return [v for v in self.vehicles if not v.available]
