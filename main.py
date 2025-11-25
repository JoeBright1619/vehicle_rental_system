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
            pause()


def list_available_vehicles(vehicle_manager):
    print("1. view all?")
    print("2. view all by a specific brand?")
    print("3. view all by a specific type(car,bike etc)?")
    choice = input("Enter your option: ")
    if(choice=="1"):
        vehicles = vehicle_manager.list_available()
        print("\nAvailable Vehicles:")
    elif(choice=="2"):
        vehicle_brand = input("Enter the brand: ")
        vehicles = vehicle_manager.get_vehicles_by_brand(vehicle_brand)
        print(f"\nAvailable Vehicles by {vehicle_brand}:")
    elif(choice=="3"):
        print("\n===Choose the type of vehicles===")
        print("1. Car")
        print("2. Bike")
        print("3. Truck")
        choice = input("Enter the number for your choice: ")
        if(choice=="1"):
            vehicles = vehicle_manager.get_vehicles_by_type("Car")
        elif(choice=="2"):
            vehicles = vehicle_manager.get_vehicles_by_type("bike")
        elif(choice=="3"):
            vehicles = vehicle_manager.get_vehicles_by_type("Truck")
        else:
            print("Invalid option. Try again.")
            pause()
            return
    else:
        print("Invalid option. Try again.")
        pause()
        return
    
    if not vehicles:
        print("No vehicles available.")
        pause()
        return
        
    
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
