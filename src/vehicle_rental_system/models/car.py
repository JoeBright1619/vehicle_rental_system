from .vehicle import Vehicle

class Car(Vehicle):
    @property
    def price_per_day(self):
        return self._base_price * 1.2  # 20% extra charge

    def vehicle_type(self):
        return "Car"
