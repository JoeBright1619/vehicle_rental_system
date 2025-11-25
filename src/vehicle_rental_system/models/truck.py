from .vehicle import Vehicle

class Truck(Vehicle):
    @property
    def price_per_day(self):
        return self._base_price * 1.5

    def vehicle_type(self):
        return "Truck"
