from .vehicle import Vehicle

class Truck(Vehicle):
    """Vehicle specialization for trucks, which incur higher rental rates."""
    @property
    def price_per_day(self):
        """Include a 50% premium to account for truck capacity and wear."""
        return self._base_price * 1.5

    def vehicle_type(self):
        return "Truck"
