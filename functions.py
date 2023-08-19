import datetime

# to show in table
def display_equipment(equipment_list):
    ''' to display the available equipment in the shop'''
    print("Available Equipment:")
    print(
        "{:<4} {:<35} {:<20} {:<12} {:<8}".format(
            "No.", "Equipment", "Brand", "Price ($)", "Quantity"
        )
    )
    print("=" * 83)
    for index, equipment in enumerate(equipment_list, 1):
        print(
            "{:<4} {:<35} {:<20} {:<12} {:<8}".format(
                index,
                equipment["name"],
                equipment["brand"],
                equipment["price"],
                equipment["quantity"],
            )
        )


def read_equipment_data(file_name):
    equipment_data = []
    with open(file_name, "r") as file:
        for line in file:
            name, brand, price, quantity = line.strip().split(", ")
            equipment = {
                "name": name,
                "brand": brand,
                "price": price,
                "quantity": int(quantity),
            }
            equipment_data.append(equipment)
    return equipment_data


def return_equipment(equipment_list):
    display_equipment(equipment_list)

    try:
        choice = int(input("Enter the number of the equipment you are returning: ")) - 1

        if choice < 0 or choice >= len(equipment_list):
            print("Invalid choice.")
            return

        equipment = equipment_list[choice]

        customer_name = input("Enter your name: ")
        if customer_name != equipment.get("rented_to"):
            print("Invalid customer name. This equipment was not rented to you.")
            return

        print("\nRented Equipment Details:")
        print(f"Name: {equipment['name']}")
        print(f"Brand: {equipment['brand']}")
        print(f"Customer: {customer_name}")
        print(
            f"Rental Date: {equipment['rental_date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        return_date = datetime.datetime.now()

        while True:
            try:
                rented_days = int(
                    input(
                        f"Enter the number of days you rented {equipment['name']} for: "
                    )
                )
                break
            except ValueError:
                print("Please enter a valid number.")

        rental_duration = 5
        overdue_days = max(rented_days - rental_duration, 0)
        fines = overdue_days * 10

        rental_price_per_period = float(equipment["price"].replace("$", ""))

        invoice_name = f"{customer_name}_{return_date.strftime('%Y%m%d_%H%M%S')}_return_invoice.txt"

        with open(invoice_name, "w") as invoice_file:
            invoice_file.write("===================================\n")
            invoice_file.write("          RETURN INVOICE           \n")
            invoice_file.write("===================================\n")
            invoice_file.write(f"Date: {return_date.strftime('%Y-%m-%d_%H-%M-%S')}\n")
            invoice_file.write("===================================\n")
            invoice_file.write(f"Customer: {customer_name}\n")
            invoice_file.write("===================================\n")
            invoice_file.write("Equipment Details:\n")
            invoice_file.write(f"Name: {equipment['name']}\n")
            invoice_file.write(f"Brand: {equipment['brand']}\n")
            invoice_file.write(
                f"Initial Quantity: {equipment.get('initial_quantity', '')}\n"
            )
            invoice_file.write(f"Rented Quantity: {equipment.get('rented_qn', '')}\n")
            invoice_file.write(
                f"Rental Date: {equipment['rental_date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            invoice_file.write("===================================\n")
            invoice_file.write(
                f"Return Date: {return_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            invoice_file.write(f"Rental Duration: {rental_duration} days\n")
            invoice_file.write(f"Rented Days: {rented_days} days\n")
            invoice_file.write(f"Overdue Days: {overdue_days} days\n")
            invoice_file.write(
                f"Fines: ${fines:.2f} (Charged at $10 per day for overdue days)\n"
            )
            invoice_file.write("===================================\n")
            invoice_file.write(f"To be paid: ${fines:.2f}\n")
            invoice_file.write("===================================\n")
        print(f"Return successful! Invoice has been generated: {invoice_name}")

        equipment["rental_date"] = None
        equipment["rented_to"] = None

        equipment["quantity"] += equipment.get("rented_qn", 0)

        with open("equipment.txt", "w") as equipment_file:
            for equip in equipment_list:
                equipment_file.write(
                    f"{equip['name']}, {equip['brand']}, {equip['price']}, {equip['quantity']}\n"
                )

    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return


def rent_equipment(equipment_list):
    display_equipment(equipment_list)

    try:
        choice = int(input("Enter the number of the equipment you want to rent: ")) - 1

        if choice < 0 or choice >= len(equipment_list):
            print("Invalid choice.")
            return

        equipment = equipment_list[choice]
        if equipment["quantity"] > 0:
            customer_name = input("Enter your name: ")
            rental_date = datetime.datetime.now()

            while True:
                try:
                    rental_duration = int(
                        input(
                            f"Enter rental duration in days for {equipment['name']} (in multiples of 5): "
                        )
                    )
                    break
                except ValueError:
                    print("Please enter a valid number.")

            while True:
                try:
                    quantity_to_rent = int(
                        input(
                            f"Enter the quantity of {equipment['name']} you want to rent: "
                        )
                    )
                    if quantity_to_rent <= equipment["quantity"]:
                        break
                    else:
                        print("Not enough quantity available.")
                except ValueError:
                    print("Please enter a valid number.")

            rental_periods = rental_duration // 5
            if rental_duration % 5 != 0:
                rental_periods += 1

            rental_price_per_period = float(equipment["price"].replace("$", ""))
            rental_amount = rental_price_per_period * rental_periods * quantity_to_rent

            invoice_name = f"{customer_name}_{rental_date.strftime('%Y-%m-%d_%H-%M-%S')}_invoice.txt"

            print("\nEquipment rented:")
            print(f"  Name: {equipment['name']}")
            print(f"  Brand: {equipment['brand']}")
            print(f"  Customer: {customer_name}")
            print(f"  Rental Date: {rental_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Rental Duration: {rental_duration} days")
            print(f"  Quantity Rented: {quantity_to_rent}")
            print(f"  Total Amount: ${rental_amount}")

            equipment["rented_to"] = customer_name
            equipment["rental_date"] = rental_date
            equipment["rented_qn"] = quantity_to_rent
            equipment["initial_quantity"] = equipment["quantity"]
            equipment["quantity"] -= quantity_to_rent

            with open("equipment.txt", "w") as equipment_file:
                for equip in equipment_list:
                    equipment_file.write(
                        f"{equip['name']}, {equip['brand']}, {equip['price']}, {equip['quantity']}\n"
                    )

            with open(invoice_name, "w") as invoice_file:
                invoice_file.write("===================================\n")
                invoice_file.write("           RENTAL INVOICE           \n")
                invoice_file.write("===================================\n")
                invoice_file.write(
                    f"Date: {rental_date.strftime('%Y-%m-%d_%H-%M-%S')}\n"
                )
                invoice_file.write("===================================\n")
                invoice_file.write(f"Customer: {customer_name}\n")
                invoice_file.write("===================================\n")
                invoice_file.write("Equipment Details:\n")
                invoice_file.write(f"Name: {equipment['name']}\n")
                invoice_file.write(f"Brand: {equipment['brand']}\n")
                invoice_file.write(f"Quantity: {quantity_to_rent}\n")
                invoice_file.write(f"Price per 5 days: {equipment['price']}\n")
                invoice_file.write("===================================\n")
                invoice_file.write(
                    f"Total Amount for {rental_duration} days: ${rental_amount:.2f}\n"
                )
                invoice_file.write("===================================\n")
            print(f"Rental successful! Invoice has been generated: {invoice_name}")
        else:
            print("Sorry, this equipment is currently unavailable.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
