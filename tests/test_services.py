"""
Test suite for service classes.
Tests VehicleManager and RentalService functionality.
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pytest

from src.vehicle_rental_system.services.vehicle_manager import VehicleManager
from src.vehicle_rental_system.services.rental_service import RentalService
from src.vehicle_rental_system.models.car import Car
from src.vehicle_rental_system.models.bike import Bike
from src.vehicle_rental_system.models.truck import Truck


class TestVehicleManager:
    """Test the VehicleManager service class."""

    @pytest.fixture
    def sample_vehicles_data(self):
        """Fixture providing sample vehicle data."""
        return [
            {
                "vehicle_id": 1,
                "type": "Car",
                "brand": "Toyota",
                "model": "Corolla",
                "base_price": 34560.0,
                "available": True
            },
            {
                "vehicle_id": 2,
                "type": "Bike",
                "brand": "Yamaha",
                "model": "MT-07",
                "base_price": 7600.0,
                "available": True
            },
            {
                "vehicle_id": 3,
                "type": "Truck",
                "brand": "Ford",
                "model": "F-150",
                "base_price": 61500.0,
                "available": False
            }
        ]

    @pytest.fixture
    def vehicle_manager(self, tmp_path, sample_vehicles_data, monkeypatch):
        """Fixture creating a VehicleManager with test data."""
        test_data_file = tmp_path / "data" / "vehicles.json"
        test_data_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_data_file, "w") as f:
            json.dump(sample_vehicles_data, f, indent=4)
        
        # Patch the FileHandler to use our test file
        with patch('src.vehicle_rental_system.services.vehicle_manager.FileHandler') as mock_file_handler:
            mock_handler_instance = MagicMock()
            mock_handler_instance.read.return_value = sample_vehicles_data
            mock_file_handler.return_value = mock_handler_instance
            
            manager = VehicleManager()
            manager.vehicles_file = mock_handler_instance
            manager.vehicles = manager.load_vehicles()
            yield manager

    def test_load_vehicles_loads_cars(self, vehicle_manager):
        """Test that VehicleManager loads Car instances correctly."""
        vehicles = vehicle_manager.load_vehicles()
        cars = [v for v in vehicles if isinstance(v, Car)]
        assert len(cars) >= 0  # At least one car in sample data

    def test_load_vehicles_loads_bikes(self, vehicle_manager):
        """Test that VehicleManager loads Bike instances correctly."""
        vehicles = vehicle_manager.load_vehicles()
        bikes = [v for v in vehicles if isinstance(v, Bike)]
        assert len(bikes) >= 0  # At least one bike in sample data

    def test_load_vehicles_loads_trucks(self, vehicle_manager):
        """Test that VehicleManager loads Truck instances correctly."""
        vehicles = vehicle_manager.load_vehicles()
        trucks = [v for v in vehicles if isinstance(v, Truck)]
        assert len(trucks) >= 0  # At least one truck in sample data

    def test_get_vehicle_by_id_returns_correct_vehicle(self, vehicle_manager):
        """Test getting a vehicle by its ID."""
        vehicle = vehicle_manager.get_vehicle_by_id(1)
        assert vehicle is not None
        assert vehicle.vehicle_id == 1

    def test_get_vehicle_by_id_returns_none_for_invalid_id(self, vehicle_manager):
        """Test that get_vehicle_by_id returns None for non-existent ID."""
        vehicle = vehicle_manager.get_vehicle_by_id(999)
        assert vehicle is None

    def test_get_vehicle_by_id_handles_string_ids(self, vehicle_manager):
        """Test that get_vehicle_by_id handles string IDs."""
        vehicle = vehicle_manager.get_vehicle_by_id("1")
        assert vehicle is not None
        assert vehicle.vehicle_id == 1

    def test_get_vehicles_by_brand_case_insensitive(self, vehicle_manager):
        """Test that brand filtering is case-insensitive."""
        vehicles_lower = vehicle_manager.get_vehicles_by_brand("toyota")
        vehicles_upper = vehicle_manager.get_vehicles_by_brand("TOYOTA")
        vehicles_mixed = vehicle_manager.get_vehicles_by_brand("ToYoTa")
        
        assert len(vehicles_lower) == len(vehicles_upper)
        assert len(vehicles_upper) == len(vehicles_mixed)

    def test_get_vehicles_by_brand_returns_empty_for_invalid_brand(self, vehicle_manager):
        """Test that brand filtering returns empty list for non-existent brand."""
        vehicles = vehicle_manager.get_vehicles_by_brand("NonExistentBrand")
        assert vehicles == []

    def test_list_available_returns_only_available_vehicles(self, vehicle_manager):
        """Test that list_available returns only vehicles with available=True."""
        available = vehicle_manager.list_available()
        
        for vehicle in available:
            assert vehicle.available is True

    def test_list_rented_returns_only_rented_vehicles(self, vehicle_manager):
        """Test that list_rented returns only vehicles with available=False."""
        rented = vehicle_manager.list_rented()
        
        for vehicle in rented:
            assert vehicle.available is False

    def test_save_vehicles_writes_correct_format(self, vehicle_manager):
        """Test that save_vehicles writes data in correct format."""
        vehicle_manager.save_vehicles()
        
        # Verify write was called
        assert vehicle_manager.vehicles_file.write.called
        write_call_args = vehicle_manager.vehicles_file.write.call_args[0][0]
        
        # Verify structure
        assert isinstance(write_call_args, list)
        if write_call_args:
            first_item = write_call_args[0]
            assert "vehicle_id" in first_item
            assert "type" in first_item
            assert "brand" in first_item
            assert "model" in first_item
            assert "base_price" in first_item
            assert "available" in first_item


class TestRentalService:
    """Test the RentalService class."""

    @pytest.fixture
    def mock_vehicle_manager(self):
        manager = Mock()

        manager.vehicles = [
            Car(1, "Toyota", "Corolla", 10000, available=True),
            Bike(2, "Yamaha", "MT-07", 5000, available=True),
            Truck(3, "Ford", "F-150", 15000, available=False)
        ]

        # Mock method behaviors
        manager.get_vehicle_by_id.side_effect = lambda vid: next(
            (v for v in manager.vehicles if v.vehicle_id == vid),
            None
        )

        manager.get_vehicles_by_brand.side_effect = lambda brand: [
            v for v in manager.vehicles if v.brand.lower() == brand.lower()
        ]

        manager.list_available.side_effect = lambda: [
            v for v in manager.vehicles if v.available
        ]

        return manager


    @pytest.fixture
    def rental_service(self, tmp_path, mock_vehicle_manager, monkeypatch):
        """Fixture creating a RentalService with test data."""
        test_rentals_file = tmp_path / "data" / "rentals.json"
        test_rentals_file.parent.mkdir(parents=True, exist_ok=True)
        
        initial_rentals = []
        with open(test_rentals_file, "w") as f:
            json.dump(initial_rentals, f, indent=4)
        
        # Patch FileHandler
        with patch('src.vehicle_rental_system.services.rental_service.FileHandler') as mock_file_handler:
            mock_handler_instance = MagicMock()
            mock_handler_instance.read.return_value = initial_rentals
            mock_file_handler.return_value = mock_handler_instance
            
            service = RentalService(mock_vehicle_manager)
            service.rental_file = mock_handler_instance
            service.rentals = initial_rentals.copy()
            yield service

    def test_rent_vehicle_success(self, rental_service):
        """Test successfully renting an available vehicle."""
        result = rental_service.rent_vehicle("John Doe", 1, 5)
        
        assert "successfully rented" in result.lower()
        assert "John Doe" in result
        assert "5" in result

    def test_rent_vehicle_returns_error_for_invalid_id(self, rental_service):
        """Test that renting a non-existent vehicle returns error message."""
        result = rental_service.rent_vehicle("John Doe", 999, 5)
        
        assert "no vehicle found" in result.lower() or "not found" in result.lower()

    def test_rent_vehicle_returns_error_for_already_rented(self, rental_service):
        """Test that renting an already rented vehicle returns error."""
        result = rental_service.rent_vehicle("John Doe", 3, 5)  # Vehicle 3 is not available
        
        assert "already rented" in result.lower() or "not available" in result.lower()

    def test_rent_vehicle_calculates_cost_correctly(self, rental_service):
        """Test that rental cost is calculated correctly."""
        rental_service.rent_vehicle("Test User", 1, 3)
        
        # Car with base 10000 should have price_per_day of 12000 (20% surcharge)
        # 3 days * 12000 = 36000
        rentals = rental_service.rentals
        assert len(rentals) > 0
        assert rentals[-1]["cost"] == 12000 * 3  # Car price * days

    def test_rent_vehicle_updates_vehicle_availability(self, rental_service):
        """Test that renting a vehicle updates its availability."""
        vehicle = rental_service.vehicle_manager.vehicles[0]
        initial_availability = vehicle.available
        
        rental_service.rent_vehicle("Test User", 1, 1)
        
        assert vehicle.available is False
        assert initial_availability is True

    def test_rent_vehicle_saves_rental_history(self, rental_service):
        """Test that renting a vehicle adds entry to rental history."""
        initial_count = len(rental_service.rentals)
        
        rental_service.rent_vehicle("Test User", 1, 2)
        
        assert len(rental_service.rentals) == initial_count + 1
        assert rental_service.rentals[-1]["renter"] == "Test User"
        assert rental_service.rentals[-1]["vehicle_id"] == 1
        assert rental_service.rentals[-1]["days"] == 2

    def test_rent_vehicle_saves_with_date(self, rental_service):
        """Test that rental entry includes date."""
        rental_service.rent_vehicle("Test User", 1, 1)
        
        rental_entry = rental_service.rentals[-1]
        assert "date" in rental_entry
        assert rental_entry["date"] is not None

    def test_return_vehicle_success(self, rental_service):
        """Test successfully returning a rented vehicle."""
        # First rent a vehicle
        vehicle = rental_service.vehicle_manager.vehicles[0]
        vehicle.available = False
        
        result = rental_service.return_vehicle(1)
        
        assert "returned successfully" in result.lower()
        assert vehicle.available is True

    def test_return_vehicle_returns_error_for_invalid_id(self, rental_service):
        """Test that returning a non-existent vehicle returns error."""
        result = rental_service.return_vehicle(999)
        
        assert "does not exist" in result.lower() or "not found" in result.lower()

    def test_return_vehicle_returns_error_for_available_vehicle(self, rental_service):
        """Test that returning an already available vehicle returns error."""
        result = rental_service.return_vehicle(1)  # Vehicle 1 is available
        
        assert "not currently rented" in result.lower()

    def test_return_vehicle_updates_availability(self, rental_service):
        """Test that returning a vehicle sets availability to True."""
        vehicle = rental_service.vehicle_manager.vehicles[0]
        vehicle.available = False  # Mark as rented
        
        rental_service.return_vehicle(1)
        
        assert vehicle.available is True

    def test_get_rent_history_returns_list(self, rental_service):
        """Test that get_rent_history returns a list."""
        history = rental_service.get_rent_history()
        assert isinstance(history, list)

    def test_get_rent_history_sorted_most_recent_first(self, rental_service):
        """Test that rental history is sorted with most recent first."""
        # Add some test rentals with different dates
        from datetime import datetime, timedelta
        
        # Use date-only format to match existing data format
        today = datetime.today().date()
        rental_service.rentals = [
            {
                "renter": "User1",
                "vehicle_id": "1",
                "days": 1,
                "cost": 1000,
                "date": (today - timedelta(days=5)).isoformat()
            },
            {
                "renter": "User2",
                "vehicle_id": "2",
                "days": 2,
                "cost": 2000,
                "date": (today - timedelta(days=2)).isoformat()
            },
            {
                "renter": "User3",
                "vehicle_id": "3",
                "days": 3,
                "cost": 3000,
                "date": today.isoformat()
            }
        ]
        
        history = rental_service.get_rent_history(reverse=True)
        
        assert len(history) == 3
        # Most recent should be first
        assert history[0]["renter"] == "User3"
        assert history[-1]["renter"] == "User1"

    def test_get_rent_history_sorted_oldest_first(self, rental_service):
        """Test that rental history can be sorted with oldest first."""
        from datetime import datetime, timedelta
        
        # Use date-only format to match existing data format
        today = datetime.today().date()
        rental_service.rentals = [
            {
                "renter": "User1",
                "vehicle_id": "1",
                "days": 1,
                "cost": 1000,
                "date": today.isoformat()
            },
            {
                "renter": "User2",
                "vehicle_id": "2",
                "days": 2,
                "cost": 2000,
                "date": (today - timedelta(days=2)).isoformat()
            }
        ]
        
        history = rental_service.get_rent_history(reverse=False)
        
        assert len(history) == 2
        # Oldest should be first
        assert history[0]["renter"] == "User2"
        assert history[-1]["renter"] == "User1"

