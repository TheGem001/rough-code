import os
import json

# ---------------- CONFIGURATION ----------------
DATA_FILE = "patients_data.json"
patients = []
next_id = 1

# ---------------- PERSISTENCE FUNCTIONS ----------------
def save_data():
    """Saves the current patient list and next_id to a JSON file."""
    data = {
        "next_id": next_id,
        "patients": patients
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    """Loads data from the JSON file if it exists."""
    global patients, next_id
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                patients = data.get("patients", [])
                next_id = data.get("next_id", 1)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read data file. Starting fresh.")

# ---------------- UTILITY FUNCTIONS ----------------
def clear_screen():
    """Clears the terminal screen based on the OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_patient_by_id(pid):
    for patient in patients:
        if patient["id"] == pid:
            return patient
    return None

# ---------------- PATIENT FUNCTIONS ----------------
def add_patient():
    global next_id
    clear_screen()
    print("--- Add New Patient ---")
    
    try:
        name = input("Name: ").strip()
        age = int(input("Age: "))
        if age <= 0:
            print("Error: Age must be a positive number.")
            return

        gender = input("Gender (Male/Female): ").strip().capitalize()
        if gender not in ["Male", "Female"]:
            print("Error: Invalid gender.")
            return

        disease = input("Disease: ").strip()
        # Allows letters and spaces
        if not all(x.isalpha() or x.isspace() for x in disease):
            print("Error: Disease name should only contain letters.")
            return

        patient = {
            "id": next_id,
            "name": name,
            "age": age,
            "gender": gender,
            "disease": disease,
            "status": "Admitted"
        }

        patients.append(patient)
        next_id += 1
        save_data()
        print("\nPatient added successfully!")
    except ValueError:
        print("Error: Invalid input. Please enter numbers for age.")

def view_all_patients():
    clear_screen()
    print("--- Patient List ---")
    if not patients:
        print("No records found.")
    else:
        # Table-like formatting for better readability
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Status':<12} {'Disease'}")
        print("-" * 60)
        for p in patients:
            print(f"{p['id']:<5} {p['name']:<20} {p['age']:<5} {p['status']:<12} {p['disease']}")
    
    input("\nPress Enter to return to menu...")

def update_patient():
    try:
        pid = int(input("Enter Patient ID to update: "))
        patient = find_patient_by_id(pid)

        if not patient:
            print("Patient not found!")
            return

        new_disease = input("New Disease (Leave blank to keep current): ").strip()
        if new_disease:
            patient["disease"] = new_disease
            save_data()
            print("Patient updated successfully!")
    except ValueError:
        print("Error: Please enter a valid numerical ID.")

def discharge_patient():
    try:
        pid = int(input("Enter Patient ID to discharge: "))
        patient = find_patient_by_id(pid)

        if not patient:
            print("Patient not found!")
        elif patient["status"] == "Discharged":
            print("Patient is already discharged!")
        else:
            patient["status"] = "Discharged"
            save_data()
            print("Status updated to Discharged.")
    except ValueError:
        print("Error: Please enter a valid numerical ID.")

# ---------------- MAIN MENU ----------------
def main_menu():
    load_data()
    while True:
        clear_screen()
        print("===== Patient Management System =====")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Update Patient")
        print("4. Discharge Patient")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_all_patients()
        elif choice == "3":
            update_patient()
        elif choice == "4":
            discharge_patient()
        elif choice == "5":
            print("Saving data and exiting...")
            break
        else:
            print("Invalid choice! Press Enter to try again.")
            input()

if __name__ == "__main__":
    main_menu()