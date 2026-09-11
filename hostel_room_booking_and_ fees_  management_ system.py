import json
import os

DATA_FILE = "hostel_data.json"

# Hostel information
hostels = {
    "A": {"name": "Block A", "rooms": 10, "capacity": 4},
    "B": {"name": "Block B", "rooms": 8, "capacity": 4},
    "C": {"name": "Block C", "rooms": 6, "capacity": 3}
}

students = {}
rooms = {}
payments = []


def create_rooms():
    """Create all hostel rooms when there is no saved room data."""
    for block, details in hostels.items():
        for number in range(1, details["rooms"] + 1):
            room_id = block + str(number)
            rooms[room_id] = {
                "block": block,
                "capacity": details["capacity"],
                "students": []
            }


def save_data():
    """Save students, rooms and payments to a JSON file."""
    data = {
        "students": students,
        "rooms": rooms,
        "payments": payments
    }

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print("Records saved successfully.")
    except OSError as error:
        print("Could not save the records:", error)


def load_data():
    """Load saved records. If the file is missing or damaged, start fresh."""
    global students, rooms, payments

    if not os.path.exists(DATA_FILE):
        create_rooms()
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        students = data.get("students", {})
        rooms = data.get("rooms", {})
        payments = data.get("payments", [])

        # Make sure rooms exist even if an old/incomplete file is found.
        if not rooms:
            create_rooms()

    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        print("The saved data file could not be read.")
        print("Starting with new records.")
        students = {}
        rooms = {}
        payments = []
        create_rooms()


def show_occupancy():
    print("\nHOSTEL OCCUPANCY OVERVIEW")
    print("-" * 50)

    for block, details in hostels.items():
        total_rooms = details["rooms"]
        capacity = details["capacity"]
        occupied = 0
        total_students = 0

        for room in rooms.values():
            if room["block"] == block:
                total_students += len(room["students"])
                if len(room["students"]) > 0:
                    occupied += 1

        total_spaces = total_rooms * capacity
        print(
            f"{details['name']}: {total_students}/{total_spaces} students "
            f"({occupied}/{total_rooms} rooms occupied)"
        )


def display_rooms():
    print("\nROOM LIST")
    print("-" * 50)

    for room_id, room in rooms.items():
        current = len(room["students"])
        print(
            f"Room {room_id} | Capacity: {room['capacity']} | "
            f"Occupied: {current} | Spaces left: {room['capacity'] - current}"
        )


def register_student():
    print("\nSTUDENT REGISTRATION")

    reg_no = input("Enter student registration number: ").strip()

    if not reg_no:
        print("Registration number cannot be empty.")
        return

    if reg_no in students:
        print("A student with that registration number already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    room_id = input("Enter room number (for example A1): ").strip().upper()

    if room_id not in rooms:
        print("That room does not exist.")
        return

    if len(rooms[room_id]["students"]) >= rooms[room_id]["capacity"]:
        print("Allocation failed. The room is already full.")
        return

    student = {
        "name": name,
        "room": room_id,
        "total_fee": 1000000.0
    }

    students[reg_no] = student
    rooms[room_id]["students"].append(reg_no)

    print("Student registered and allocated successfully.")
    print("Student:", name)
    print("Room:", room_id)
    print("Total hostel fee: UGX 1,000,000")


def get_total_paid(reg_no):
    total = 0

    for payment in payments:
        if payment["reg_no"] == reg_no:
            total += payment["amount"]

    return total


def get_balance(reg_no):
    if reg_no not in students:
        return 0

    total_fee = students[reg_no]["total_fee"]
    total_paid = get_total_paid(reg_no)

    return total_fee - total_paid


def record_payment():
    print("\nRECORD FEE PAYMENT")

    reg_no = input("Enter student registration number: ").strip()

    if reg_no not in students:
        print("Student not found.")
        return

    try:
        amount = float(input("Enter amount paid (UGX): "))
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Payment must be greater than zero.")
        return

    balance = get_balance(reg_no)

    if balance <= 0:
        print("This student's fees are already fully paid.")
        return

    if amount > balance:
        print(f"Payment is greater than the outstanding balance of UGX {balance:,.2f}.")
        return

    payment = {
        "reg_no": reg_no,
        "amount": amount
    }

    payments.append(payment)

    new_balance = get_balance(reg_no)

    print("Payment recorded successfully.")
    print(f"Amount paid: UGX {amount:,.2f}")
    print(f"Outstanding balance: UGX {new_balance:,.2f}")


def search_student():
    print("\nSEARCH FOR STUDENT")
    print("1. Search by registration number")
    print("2. Search by name")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        reg_no = input("Enter registration number: ").strip()

        if reg_no not in students:
            print("Student not found.")
            return

        show_student(reg_no)

    elif choice == "2":
        name = input("Enter student name: ").strip().lower()
        found = False

        for reg_no, student in students.items():
            if name in student["name"].lower():
                show_student(reg_no)
                found = True

        if not found:
            print("No student with that name was found.")

    else:
        print("Invalid option.")


def show_student(reg_no):
    student = students[reg_no]
    paid = get_total_paid(reg_no)
    balance = get_balance(reg_no)

    print("\nStudent Details")
    print("-" * 35)
    print("Registration No.:", reg_no)
    print("Name:", student["name"])
    print("Room:", student["room"])
    print(f"Total Fee: UGX {student['total_fee']:,.2f}")
    print(f"Paid: UGX {paid:,.2f}")
    print(f"Balance: UGX {balance:,.2f}")


def occupancy_report():
    print("\nFULL HOSTEL OCCUPANCY REPORT")
    print("=" * 60)

    for block, details in hostels.items():
        print(f"\n{details['name']}")
        print("-" * 60)

        block_students = 0

        for room_id, room in rooms.items():
            if room["block"] == block:
                current = len(room["students"])
                block_students += current

                student_names = []

                for reg_no in room["students"]:
                    if reg_no in students:
                        student_names.append(students[reg_no]["name"])

                names = ", ".join(student_names) if student_names else "Empty"

                print(
                    f"Room {room_id}: {current}/{room['capacity']} "
                    f"| {names}"
                )

        total_capacity = details["rooms"] * details["capacity"]

        print(
            f"Block total: {block_students}/{total_capacity} students"
        )


def fee_defaulters():
    print("\nFEE DEFAULTERS")
    print("-" * 60)

    try:
        threshold = float(
            input("Enter outstanding balance threshold (UGX): ")
        )
    except ValueError:
        print("Please enter a valid amount.")
        return

    found = False

    for reg_no, student in students.items():
        balance = get_balance(reg_no)

        if balance > threshold:
            print(
                f"{reg_no} | {student['name']} | "
                f"Room {student['room']} | "
                f"Balance: UGX {balance:,.2f}"
            )
            found = True

    if not found:
        print("No students were found above that threshold.")


def view_all_students():
    print("\nALL REGISTERED STUDENTS")
    print("-" * 70)

    if not students:
        print("There are no registered students.")
        return

    for reg_no, student in students.items():
        balance = get_balance(reg_no)
        print(
            f"{reg_no} | {student['name']} | Room {student['room']} | "
            f"Balance: UGX {balance:,.2f}"
        )


def menu():
    while True:
        print("\n")
        print("=" * 50)
        print(" HOSTEL ROOM BOOKING AND FEES MANAGEMENT")
        print("=" * 50)
        print("1. View hostel occupancy")
        print("2. Display rooms")
        print("3. Register student and allocate room")
        print("4. Record fee payment")
        print("5. Search student")
        print("6. View full occupancy report")
        print("7. View fee defaulters")
        print("8. View all students")
        print("9. Save records")
        print("0. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_occupancy()

        elif choice == "2":
            display_rooms()

        elif choice == "3":
            register_student()

        elif choice == "4":
            record_payment()

        elif choice == "5":
            search_student()

        elif choice == "6":
            occupancy_report()

        elif choice == "7":
            fee_defaulters()

        elif choice == "8":
            view_all_students()

        elif choice == "9":
            save_data()

        elif choice == "0":
            save_data()
            print("Thank you for using the Hostel Management System.")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")


def main():
    load_data()
    show_occupancy()
    menu()


if __name__ == "__main__":
    main()
