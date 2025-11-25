from src.vehicle_rental_system.services.vehicle_manager import VehicleManager
from src.vehicle_rental_system.services.rental_service import RentalService
from src.vehicle_rental_system.utils.helpers import pause

def main_menu(vehicle_manager, rental_service):
    while True:
        print("\n=== Vehicle Rental System ===")
        print("1. List available vehicles")
        print("2. List rented vehicles")
        print("3. Rent a vehicle")
        print("4. Return a vehicle")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_available_vehicles(vehicle_manager)
        elif choice == "2":
            list_rented_vehicles(vehicle_manager)
        elif choice == "3":
            rent_vehicle_cli( rental_service)
        elif choice == "4":
            return_vehicle_cli(rental_service)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


def list_available_vehicles(vehicle_manager):
    vehicles = vehicle_manager.list_available()
    if not vehicles:
        print("No vehicles available.")
        return
    print("\nAvailable Vehicles:")
    for v in vehicles:
        print(f"{v.vehicle_id}: {v.vehicle_type()} - {v.brand} {v.model}, Price per day: {v.price_per_day}")

    pause()

def list_rented_vehicles(vehicle_manager):
    vehicles = vehicle_manager.list_rented()
    if not vehicles:
        print("No vehicles are currently rented.")
        pause()
        return
    print("\nRented Vehicles:")
    for v in vehicles:
        print(f"{v.vehicle_id}: {v.vehicle_type()} - {v.brand} {v.model}")
    pause()

def rent_vehicle_cli( rental_service):
    renter_name = input("Enter your name: ").strip()
    vehicle_id = input("Enter vehicle ID to rent: ").strip()
    days = input("Enter number of days: ").strip()

    if not days.isdigit() or int(days) < 1:
        print("Invalid number of days.")
        pause()
        return

    message = rental_service.rent_vehicle(renter_name, vehicle_id, int(days))
    print(message)
    pause()

def return_vehicle_cli(rental_service):
    vehicle_id = input("Enter vehicle ID to return: ").strip()
    message = rental_service.return_vehicle(vehicle_id)
    print(message)
    pause()

if __name__ == "__main__":
    vm = VehicleManager()
    rs = RentalService(vm)
    main_menu(vm, rs)
