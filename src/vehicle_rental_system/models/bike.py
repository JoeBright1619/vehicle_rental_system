from .vehicle import Vehicle

class Bike(Vehicle):
    """Vehicle specialization for bikes, which are cheaper per day."""
    @property
    def price_per_day(self):
        """Offer a discounted daily rate for bikes."""
        return self._base_price * 0.8

    def vehicle_type(self):
        return "Bike"
