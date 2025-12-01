"""
Pytest configuration and shared fixtures for test suite.
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.vehicle_rental_system.models.car import Car
from src.vehicle_rental_system.models.bike import Bike
from src.vehicle_rental_system.models.truck import Truck


@pytest.fixture
def sample_car():
    """Fixture providing a sample Car instance."""
    return Car(1, "Toyota", "Corolla", 34560.0, available=True)


@pytest.fixture
def sample_bike():
    """Fixture providing a sample Bike instance."""
    return Bike(2, "Yamaha", "MT-07", 7600.0, available=True)


@pytest.fixture
def sample_truck():
    """Fixture providing a sample Truck instance."""
    return Truck(3, "Ford", "F-150", 61500.0, available=False)


@pytest.fixture
def sample_vehicles(sample_car, sample_bike, sample_truck):
    """Fixture providing a list of sample vehicles."""
    return [sample_car, sample_bike, sample_truck]

