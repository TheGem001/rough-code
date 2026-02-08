import json
import os
from datetime import datetime, timedelta

# --- Configuration & Data Handling ---
DATA_FILE = "tracker_data.json"

def clear_screen():
    """Clears the terminal screen for a cleaner UI."""
    # Uses 'cls' for Windows, 'clear' for Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    """Loads data from the JSON file. If it doesn't exist, returns a default structure."""
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"users": {}}

def save_data(data):
    """Saves the current data dictionary to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

# --- Authentication System ---

def signup(data):
    clear_screen()
    print("\n--- Sign Up ---")
    username = input("Enter a new username: ").strip().lower()
    if username in data["users"]:
        print("Username already exists! Try logging in.")
        input("Press Enter to continue...")
        return None
    
    password = input("Enter a password: ").strip()
    
    # Initialize user structure
    data["users"][username] = {
        "password": password,
        "balance": 0.0,
        "transactions": [] 
    }
    save_data(data)
    print("Account created successfully! Please log in.")
    input("Press Enter to continue...")
    return None

def login(data):
    clear_screen()
    print("\n--- Log In ---")
    username = input("Enter username: ").strip()
    if username not in data["users"]:
        print("Username not found.")
        input("Press Enter to continue...")
        return None
    
    password = input("Enter password: ").strip()
    if data["users"][username]["password"] == password:
        print(f"Welcome back, {username}!")
        return username
    else:
        print("Incorrect password.")
        input("Press Enter to continue...")
        return None

# --- Core Features ---

def add_amount(username, data):
    """Option 1: Add Amount (Income/Deposit)"""
    clear_screen()
    print("\n--- Add Income ---")
    try:
        amount = float(input("Enter amount to add: "))
        if amount <= 0:
            print("Amount must be positive.")
            input("Press Enter to continue...")
            return

        user_data = data["users"][username]
        user_data["balance"] += amount
        
        # Log transaction
        transaction = {
            "type": "income",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "Added to wallet"
        }
        user_data["transactions"].append(transaction)
        
        save_data(data)
        print(f"Amount added. Current Balance: {user_data['balance']}")
    except ValueError:
        print("Invalid input. Please enter a number.")
    input("Press Enter to continue...")

def give_amount(username, data):
    """Option 2: Give Amount (Withdrawal/Transfer - Not an Expense)"""
    clear_screen()
    print("\n--- Give Amount ---")
    try:
        amount = float(input("Enter amount to give/remove: "))
        if amount <= 0:
            print("Amount must be positive.")
            input("Press Enter to continue...")
            return

        user_data = data["users"][username]
        
        if user_data["balance"] < amount:
            print("Insufficient balance!")
            input("Press Enter to continue...")
            return

        user_data["balance"] -= amount
        
        # Log transaction
        transaction = {
            "type": "withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": "Given/Removed amount"
        }
        user_data["transactions"].append(transaction)
        
        save_data(data)
        print(f"Amount removed. Current Balance: {user_data['balance']}")
    except ValueError:
        print("Invalid input. Please enter a number.")
    input("Press Enter to continue...")

def add_expense(username, data):
    """Option 3: Add Expense (Categorized Spending)"""
    clear_screen()
    print("\n--- Add Expense ---")
    try:
        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            input("Press Enter to continue...")
            return

        user_data = data["users"][username]
        
        if user_data["balance"] < amount:
            print(f"Insufficient balance! Current Balance: {user_data['balance']}")
            input("Press Enter to continue...")
            return

        category = input("Enter expense category (e.g., Food, Travel, Education): ").strip()
        description = input("Enter short description: ").strip()
        
        user_data["balance"] -= amount
        
        # Automatically take current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Log transaction
        transaction = {
            "type": "expense",
            "amount": amount,
            "date": current_date,
            "category": category,
            "description": description
        }
        user_data["transactions"].append(transaction)
        
        save_data(data)
        print(f"Expense recorded. Current Balance: {user_data['balance']}")
    except ValueError:
        print("Invalid input. Please enter a number.")
    input("Press Enter to continue...")

# --- Reporting System ---

def get_report(username, data):
    """Option 4: Get Report (Filters for Expenses only)"""
    clear_screen()
    print("\n--- Expense Report Menu ---")
    print("1. Weekly Report (Last 7 Days)")
    print("2. Monthly Report (Last 30 Days)")
    print("3. Custom Date Range (Date-to-Date)")
    print("4. Back")
    
    choice = input("Select report type (1-3): ")
    if choice == '4':
        return

    user_data = data["users"][username]
    transactions = user_data["transactions"]
    
    # Filter only 'expense' type transactions
    expenses = [t for t in transactions if t["type"] == "expense"]
    
    if not expenses:
        print("No expense records found.")
        input("Press Enter to continue...")
        return

    today = datetime.now()
    start_date = None
    end_date = today

    if choice == '1':
        start_date = today - timedelta(days=7)
        print(f"\n--- Weekly Report (Since {start_date.strftime('%Y-%m-%d')}) ---")
    elif choice == '2':
        start_date = today - timedelta(days=30)
        print(f"\n--- Monthly Report (Since {start_date.strftime('%Y-%m-%d')}) ---")
    elif choice == '3':
        try:
            s_date_str = input("Enter start date (YYYY-MM-DD): ")
            e_date_str = input("Enter end date (YYYY-MM-DD): ")
            start_date = datetime.strptime(s_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(e_date_str, "%Y-%m-%d") + timedelta(days=1) # Include end date
            print(f"\n--- Custom Report ({s_date_str} to {e_date_str}) ---")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            input("Press Enter to continue...")
            return
    else:
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    # Generate Table
    print(f"{'Date':<12} | {'Category':<15} | {'Description':<20} | {'Amount':<10}")
    print("-" * 65)
    
    total_expense = 0
    found_records = False

    for t in expenses:
        t_date = datetime.strptime(t["date"], "%Y-%m-%d")
        
        # Check if transaction date is within range
        if start_date <= t_date <= end_date:
            print(f"{t['date']:<12} | {t['category']:<15} | {t['description']:<20} | {t['amount']:<10.2f}")
            total_expense += t['amount']
            found_records = True

    if not found_records:
        print("No expenses found in this period.")
    else:
        print("-" * 65)
        print(f"{'TOTAL':<50} | {total_expense:<10.2f}")
    
    input("\nPress Enter to return to menu...")

def show_about():
    """Option 5: About Project"""
    clear_screen()
    print("\n" + "="*40)
    print("         PROJECT ABOUT INFO         ")
    print("="*40)
    print("Project Name : Finance/Expense Tracker")
    print("Institution  : The Islamia University of Bahawalpur")
    print("Department   : Software Engineering")
    print("Course       : Programming Fundamentals")
    print("Instructor   : Sir. Gulraiz Javaid")
    print("-" * 40)
    print("Development Team:")
    print("1. M. Umair Mehboob  (F25BSEEN1M01198)")
    print("2. M. Saqib Zahid    (F25BSEEN1M01186)")
    print("3. M. Junaid         (F25BSEEN1M01191)")
    print("="*40)
    print("Description:")
    print("This tool helps students manage finances by tracking")
    print("income, expenses, and generating automated reports.")
    print("="*40)
    input("\nPress Enter to return to menu...")

# --- Main Application Loop ---

def main():
    data = load_data()
    current_user = None

    while True:
        clear_screen()
        if current_user is None:
            print("\n=== EXPENSE TRACKER SYSTEM ===")
            print("1. Log In")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                current_user = login(data)
            elif choice == '2':
                signup(data)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
        else:
            print(f"\n--- Main Menu ({current_user}) ---")
            print(f"Current Balance: {data['users'][current_user]['balance']}")
            print("1. Add Amount (Income)")
            print("2. Give Amount (Withdrawal)")
            print("3. Add Expense")
            print("4. Get Report")
            print("5. About")
            print("6. Logout")
            
            choice = input("Choose an option: ")

            if choice == '1':
                add_amount(current_user, data)
            elif choice == '2':
                give_amount(current_user, data)
            elif choice == '3':
                add_expense(current_user, data)
            elif choice == '4':
                get_report(current_user, data)
            elif choice == '5':
                show_about()
            elif choice == '6':
                print("Logging out...")
                current_user = None
            else:
                print("Invalid option, please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()