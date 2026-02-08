# An Expense Tracker Application
import json
import os
from datetime import datetime
from pkgutil import get_data
import pyttsx3

DATA_FILE = "expense_data.json"
 
# Function for clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function To load data from file 
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data
    except(json.JSONDecodeError, IOError):
        return {"users": {}}
    
# Function to save data to file
def save_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

# Sign Up function 
def sign_up(data):
    clear_screen()
    print("Sign Up")
    pyttsx3.speak("Please enter your details to sign up.")
    username = input("Enter your username: ").strip().lower()
    if username in data["users"]:
        print("Username already exists. Please try logging in.")
        pyttsx3.speak("Username already exists. Please try logging in.")
        main_menu()
    password = input("Enter your password: ").strip()
    if not password:
        print("Password cannot be empty.")
        pyttsx3.speak("Password cannot be empty.")
        main_menu()
    # Initialize user structure
    data["users"][username] = {
        "password": password,
        "balance": 0.0,
        "transactions": [] 
    }
    save_data(data)
    print("Sign up successful!")
    pyttsx3.speak("Sign up successful! please log in.")
    print("Please log in now.")
    print("Press enter to continue.")
    pyttsx3.speak("Press enter to continue.")
    input()
    return None

# Function for log-in
def log_in(data):
    username = None
    current_user = username
    clear_screen()
    print("Log In")
    pyttsx3.speak("Please enter your login details.")
    username = input("Enter your username: ").strip().lower()
    if username not in data["users"]:
        print("User not found.")
        pyttsx3.speak("User not found. Sign up first.")
        main_menu()
    else:
        password = input("Enter your password: ")
        if password not in data['users'][username]['password']:
            print("Incorrect password.")
            pyttsx3.speak("Incorrect password.")
            main_menu()
        else:
            if data["users"][username]["password"] == password:
                print("Login successful!")
                pyttsx3.speak("Login successful!")
                print("Press enter to continue.")
    pyttsx3.speak("Press enter to continue.")
    input()
    return username

# Function for log out
def log_out():
    clear_screen()
    print("Logging out...")
    pyttsx3.speak("Logging out. Goodbye!")
    main_menu()

# Function for expense
def add_expense(data):
    clear_screen()
    print("Add Expense")
    pyttsx3.speak("Please enter the expense details.")
    try:
        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            print("Amount must be positive. Press enter.")
            pyttsx3.speak("Amount must be positive.")
            input()
            return
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        pyttsx3.speak("Invalid amount. Please enter a valid number.")
        input()
        return

    if get_data["balance"] < amount:
        print("Insufficient balance for this expense.")
        pyttsx3.speak("Insufficient balance for this expense.")
        print("Press enter to return to main menu.")
        pyttsx3.speak("Press enter")
        input()
        return
    category = input("Enter expense category: ")
    data = data["users"][data["current_user"]]
    data["balance"] -= amount

    date = datetime.now()
    expense = {
        "type": "expense",
        "amount": amount,
        "category": category,
        "date": date.strftime("%Y-%m-%d %H:%M:%S")
    }

    data["transactions"].append(expense)

    save_data(data)
    print("Expense added successfully! current balance:", data["balance"])
    print("Expense added successfully!")
    pyttsx3.speak("Expense added successfully!")
    print("Press enter to return to main menu.")
    pyttsx3.speak("Press enter")
    input()
    main_menu()


# Updated function signature to accept current_user
def add_amount(data, current_user):
    clear_screen()
    print("Add Income")
    pyttsx3.speak("Please enter the income details.")
    
    try:
        amount = float(input("Enter income amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            input("Press enter to continue.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press enter to continue.")
        return

    source = input("Enter income source: ")
    
    # Correctly access the user's specific dictionary within the main data object
    user_records = data["users"][current_user]
    user_records["balance"] += amount
    
    date = datetime.now()
    income = {
        "type": "income",
        "amount": amount,
        "source": source,
        "date": date.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    user_records["transactions"].append(income)
    
    # Save the entire data dictionary back to the file
    save_data(data)
    
    print(f"Income added successfully! Current balance: {user_records['balance']}")
    pyttsx3.speak("Income added successfully!")
    print("Press enter to return to main menu.")
    input()

# Updated Main Menu in e.py
def main_menu():
    data = load_data()
    current_user = None  # This starts as None

    while True:
        clear_screen()
        if current_user is None:
            print("1. Log In")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                current_user = log_in(data) # current_user gets assigned here
            elif choice == '2':
                sign_up(data)
            elif choice == '3':
                break
        else:
            # Authenticated Menu
            print(f"Expense Tracker for {current_user}")
            print("1. Add Expense")
            print("2. Add Income")
            print("3. View Transactions (Not Implemented)")
            print("4. View Balance (Not Implemented)")
            print("5. About")
            print("6. Log Out")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                add_expense(data, current_user) # Pass current_user
            elif choice == '2':
                add_amount(data, current_user)  # Pass current_user
            elif choice == '5':
                about()
            elif choice == '6':
                current_user = None # Log out by resetting to None
            
            # REMOVED: return choice (This was exiting the loop)
# Function for about
def about():
    clear_screen()
    print("----------- About This Project -----------")
    print("Project Name: Finance / Expense Tracker")
    print("Purpose: To help university students manage their finances effectively")
    print("by providing a digital and organized way to track income and expenditures.")
    
    print("\n--- Project Team ---")
    print("1. M. Umair Mehboob (F25BSEEN1M01198)")
    print("2. M. Saqib Zahid    (F25BSEEN1M01186)")
    print("3. M. Junaid         (F25BSEEN1M01191)")
    
    print("\n--- System Details ---")
    print("Course: Programming Fundamentals")
    print("Language: Python 3.14")
    print("Environment: VS Code / PyCharm")
    
    print("\n------------------------------------------")
    pyttsx3.speak("This is a Finance Tracker project developed for Programming Fundamentals course.")
    
    print("Press enter to return to the main menu.")
    input()
    main_menu()

main_menu()