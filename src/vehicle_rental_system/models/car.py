from .vehicle import Vehicle

class Car(Vehicle):
    """Vehicle specialization that represents standard passenger cars."""
    @property
    def price_per_day(self):
        """Apply a 20% surcharge on the base rate for cars."""
        return self._base_price * 1.2  # 20% extra charge

    def vehicle_type(self):
        return "Car"
