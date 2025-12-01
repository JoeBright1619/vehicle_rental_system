"""
Test suite for vehicle model classes.
Tests inheritance, polymorphism, and pricing calculations.
"""
import pytest
from src.vehicle_rental_system.models.vehicle import Vehicle
from src.vehicle_rental_system.models.car import Car
from src.vehicle_rental_system.models.bike import Bike
from src.vehicle_rental_system.models.truck import Truck


class TestVehicle:
    """Test the abstract Vehicle base class behavior through concrete implementations."""

    def test_vehicle_cannot_be_instantiated(self):
        """Test that Vehicle abstract class cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Vehicle(1, "Brand", "Model", 1000)

    def test_vehicle_has_correct_attributes(self):
        """Test that vehicle instances have all expected attributes."""
        car = Car(1, "Toyota", "Corolla", 10000)
        
        assert car.vehicle_id == 1
        assert car.brand == "Toyota"
        assert car.model == "Corolla"
        assert car._base_price == 10000
        assert car.available is True

    def test_vehicle_availability_defaults_to_true(self):
        """Test that vehicles are available by default."""
        car = Car(1, "Toyota", "Corolla", 10000)
        assert car.available is True

    def test_vehicle_can_set_availability(self):
        """Test that vehicle availability can be set."""
        car = Car(1, "Toyota", "Corolla", 10000, available=False)
        assert car.available is False

    def test_vehicle_repr(self):
        """Test the string representation of a vehicle."""
        car = Car(1, "Toyota", "Corolla", 10000)
        repr_str = repr(car)
        
        assert "Car(1)" in repr_str
        assert "Toyota" in repr_str
        assert "Corolla" in repr_str
        assert "Available" in repr_str

    def test_vehicle_repr_shows_rented_status(self):
        """Test that rented vehicles show correct status in repr."""
        car = Car(1, "Toyota", "Corolla", 10000, available=False)
        repr_str = repr(car)
        assert "Rented" in repr_str


class TestCar:
    """Test the Car vehicle type."""

    def test_car_vehicle_type(self):
        """Test that car returns correct vehicle type."""
        car = Car(1, "Toyota", "Corolla", 10000)
        assert car.vehicle_type() == "Car"

    def test_car_pricing_applies_20_percent_surcharge(self):
        """Test that car pricing applies 20% surcharge to base price."""
        base_price = 10000
        car = Car(1, "Toyota", "Corolla", base_price)
        expected_price = base_price * 1.2
        
        assert car.price_per_day == expected_price
        assert car.price_per_day == 12000

    def test_car_pricing_calculation(self):
        """Test car pricing with different base prices."""
        test_cases = [
            (34560, 41472.0),  # Example from data
            (36000, 43200.0),
            (57600, 69120.0),
            (100, 120.0),
            (0, 0.0)
        ]
        
        for base_price, expected_price in test_cases:
            car = Car(1, "Brand", "Model", base_price)
            assert car.price_per_day == expected_price


class TestBike:
    """Test the Bike vehicle type."""

    def test_bike_vehicle_type(self):
        """Test that bike returns correct vehicle type."""
        bike = Bike(1, "Yamaha", "MT-07", 10000)
        assert bike.vehicle_type() == "Bike"

    def test_bike_pricing_applies_20_percent_discount(self):
        """Test that bike pricing applies 20% discount to base price."""
        base_price = 10000
        bike = Bike(1, "Yamaha", "MT-07", base_price)
        expected_price = base_price * 0.8
        
        assert bike.price_per_day == expected_price
        assert bike.price_per_day == 8000

    def test_bike_pricing_calculation(self):
        """Test bike pricing with different base prices."""
        test_cases = [
            (7600, 6080.0),  # Example from data
            (5040, 4032.0),
            (9600, 7680.0),
            (100, 80.0),
            (0, 0.0)
        ]
        
        for base_price, expected_price in test_cases:
            bike = Bike(1, "Brand", "Model", base_price)
            assert bike.price_per_day == expected_price


class TestTruck:
    """Test the Truck vehicle type."""

    def test_truck_vehicle_type(self):
        """Test that truck returns correct vehicle type."""
        truck = Truck(1, "Ford", "F-150", 10000)
        assert truck.vehicle_type() == "Truck"

    def test_truck_pricing_applies_50_percent_premium(self):
        """Test that truck pricing applies 50% premium to base price."""
        base_price = 10000
        truck = Truck(1, "Ford", "F-150", base_price)
        expected_price = base_price * 1.5
        
        assert truck.price_per_day == expected_price
        assert truck.price_per_day == 15000

    def test_truck_pricing_calculation(self):
        """Test truck pricing with different base prices."""
        test_cases = [
            (61500, 92250.0),  # Example from data
            (117000, 175500.0),
            (52500, 78750.0),
            (100, 150.0),
            (0, 0.0)
        ]
        
        for base_price, expected_price in test_cases:
            truck = Truck(1, "Brand", "Model", base_price)
            assert truck.price_per_day == expected_price


class TestVehiclePolymorphism:
    """Test polymorphic behavior of different vehicle types."""

    def test_different_vehicles_have_different_pricing(self):
        """Test that different vehicle types calculate prices differently."""
        base_price = 10000
        
        car = Car(1, "Brand", "Model", base_price)
        bike = Bike(2, "Brand", "Model", base_price)
        truck = Truck(3, "Brand", "Model", base_price)
        
        assert car.price_per_day == 12000
        assert bike.price_per_day == 8000
        assert truck.price_per_day == 15000
        
        # Verify they all have different prices
        assert car.price_per_day != bike.price_per_day
        assert car.price_per_day != truck.price_per_day
        assert bike.price_per_day != truck.price_per_day

    def test_all_vehicles_implement_vehicle_type(self):
        """Test that all vehicle types implement the vehicle_type method."""
        car = Car(1, "Brand", "Model", 1000)
        bike = Bike(2, "Brand", "Model", 1000)
        truck = Truck(3, "Brand", "Model", 1000)
        
        assert isinstance(car.vehicle_type(), str)
        assert isinstance(bike.vehicle_type(), str)
        assert isinstance(truck.vehicle_type(), str)

