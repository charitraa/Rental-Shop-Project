import functions


def main():
    print("\n==========================================")
    print("Welcome to the Event Equipment Rental Shop!")
    print("===========================================")

    equipment_data = functions.read_equipment_data("equipment.txt")

    while True:
        print("\nMenu:")
        print("1. Display Available Equipment")
        print("2. Rent Equipment")
        print("3. Return Equipment")
        print("4. Exit")

        try:

            choice = int(input("Enter your choice: "))

            if choice == 1:
                functions.display_equipment(equipment_data)
            elif choice == 2:
                functions.rent_equipment(equipment_data)
            elif choice == 3:
                functions.return_equipment(equipment_data)
            elif choice == 4:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()
