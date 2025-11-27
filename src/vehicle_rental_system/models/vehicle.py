from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Base class for all rentable vehicles in the system."""
    def __init__(self, vehicle_id, brand, model, base_price, available=True, type=None):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self._base_price = base_price
        self.available = available
        self.type = type

    # price per day, subclasses modify this
    @property
    def price_per_day(self):
        """Return the computed daily rate (subclasses may override)."""
        return self._base_price

    @abstractmethod
    def vehicle_type(self):
        """Return the friendly string name representing the vehicle category."""
        pass

    def __repr__(self):
        status = "Available" if self.available else "Rented"
        return f"{self.vehicle_type()}({self.vehicle_id}): {self.brand} {self.model} - {status}"
