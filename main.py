from src.vehicle_rental_system.services.vehicle_manager import VehicleManager
from src.vehicle_rental_system.services.rental_service import RentalService
from src.vehicle_rental_system.utils.helpers import pause


def main_menu(vehicle_manager, rental_service):
    """
    Simple CLI router that loops through menu options and dispatches to the
    appropriate helper based on user keyboard input.
    """
    while True:
        print("\n=== Vehicle Rental System ===")
        print("1. List available vehicles")
        print("2. List rented vehicles")
        print("3. Rent a vehicle")
        print("4. Return a vehicle")
        print("5. Rent history")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_available_vehicles(vehicle_manager)

        elif choice == "2":
            list_rented_vehicles(vehicle_manager)

        elif choice == "3":
            rent_vehicle_cli(rental_service)

        elif choice == "4":
            return_vehicle_cli(rental_service)

        elif choice == "5":
            rental_history_cli(rental_service)
            
        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")
            pause()


def list_available_vehicles(vehicle_manager):
    """
    Collect filter criteria from the user, fetch the resulting vehicles from the
    manager, and render them in the console.
    """
    print("\n--- Filter Options ---")
    print("1. View all")
    print("2. Filter by brand")
    print("3. Filter by type")
    choice = input("Choose option: ").strip()

    if choice == "1":
        vehicles = vehicle_manager.list_available()

    elif choice == "2":
        brand = input("Enter brand: ").strip()
        vehicles = vehicle_manager.get_vehicles_by_brand(brand)

    elif choice == "3":
        print("\nTypes:")
        print("1. Car")
        print("2. Bike")
        print("3. Truck")
        t = input("Choose type: ").strip()

        type_map = {"1": "Car", "2": "Bike", "3": "Truck"}
        vehicle_type = type_map.get(t)

        if not vehicle_type:
            print("Invalid type.")
            pause()
            return

        vehicles = vehicle_manager.get_vehicles_by_type(vehicle_type)

    else:
        print("Invalid option.")
        pause()
        return

    # Display results
    if not vehicles:
        print("No vehicles found.")
        pause()
        return

    print("\nAvailable Vehicles:")
    for v in vehicles:
        print(f"{v.vehicle_id}: {v.vehicle_type()} - {v.brand} {v.model} | {v.price_per_day}/day")

    pause()


def list_rented_vehicles(vehicle_manager):
    """Display the list of vehicles that are currently marked as rented."""
    vehicles = vehicle_manager.list_rented()
    if not vehicles:
        print("No rented vehicles.")
        pause()
        return

    print("\nRented Vehicles:")
    for v in vehicles:
        print(f"{v.vehicle_id}: {v.vehicle_type()} - {v.brand} {v.model}")

    pause()


def rent_vehicle_cli(rental_service):
    """
    Gather rental details from the CLI and delegate the actual rental logic to
    the RentalService instance.
    """
    renter_name = input("Enter your name: ").strip()
    vehicle_id = input("Enter vehicle ID: ").strip()

    days = input("Enter number of days: ").strip()
    if not days.isdigit() or int(days) <= 0:
        print("Invalid number of days.")
        pause()
        return

    result = rental_service.rent_vehicle(renter_name, vehicle_id, int(days))
    print(result)
    pause()


def return_vehicle_cli(rental_service):
    """Handle return prompts and hand off the work to RentalService."""
    vehicle_id = input("Enter vehicle ID to return: ").strip()
    result = rental_service.return_vehicle(vehicle_id)
    print(result)
    pause()

def rental_history_cli(rental_service):
    """Pretty-print the persisted rental history in reverse chronological order."""
    history = rental_service.get_rent_history()

    if not history:
        print("\nNo rental history found.\n")
        pause()
        return

    print("\n===== RENTAL HISTORY =====\n")

    for entry in history:
        print(f"Renter:       {entry['renter']}")
        print(f"Vehicle ID:   {entry['vehicle_id']}")
        print(f"Days:         {entry['days']}")
        print(f"Cost:         {entry['cost']} RWF")
        print(f"Date:         {entry['date']}")
        print("-" * 35)

    print()
    pause()

if __name__ == "__main__":
    vm = VehicleManager()
    rs = RentalService(vm)
    main_menu(vm, rs)
