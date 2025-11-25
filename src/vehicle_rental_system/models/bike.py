from .vehicle import Vehicle

class Bike(Vehicle):
    @property
    def price_per_day(self):
        return self._base_price * 0.8

    def vehicle_type(self):
        return "Bike"
