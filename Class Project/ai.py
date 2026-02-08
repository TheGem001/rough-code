import json
import os
from datetime import datetime
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Helper function to handle text-to-speech."""
    print(text)  # Also print to console for visibility
    engine.say(text)
    engine.runAndWait()

DATA_FILE = "expense_data.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {"users": {}}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        speak(f"Error saving data: {e}")

# --- Authentication ---
def sign_up(data):
    clear_screen()
    speak("Sign Up. Please enter a new username.")
    username = input("Username: ").strip().lower()
    if username in data["users"]:
        speak("Username already exists. Please try logging in.")
        input("Press Enter...")
        return
    
    password = input("Enter a new password: ").strip()
    data["users"][username] = {"password": password, "balance": 0.0, "transactions": []}
    save_data(data)
    speak("Sign up successful! You can now log in.")
    input("Press Enter to continue...")

def log_in(data):
    clear_screen()
    speak("Log In. Please enter your username.")
    username = input("Username: ").strip().lower()
    if username not in data["users"]:
        speak("User not found. Please sign up first.")
        input("Press Enter...")
        return None
    
    password = input("Enter password: ")
    if data["users"][username]["password"] == password:
        speak(f"Welcome back, {username}!")
        return username
    else:
        speak("Incorrect password.")
        input("Press Enter...")
        return None

# --- Features ---
def add_income(data, current_user):
    clear_screen()
    speak("Add Income. Enter the amount.")
    try:
        amount = float(input("Amount: "))
        source = input("Enter income source: ")
        user_ref = data["users"][current_user]
        user_ref["balance"] += amount
        user_ref["transactions"].append({
            "type": "income", "amount": amount, "source": source, 
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_data(data)
        speak(f"Income of {amount} added successfully.")
    except ValueError:
        speak("Invalid input. Please enter a number.")
    input("Press Enter to continue...")

def add_expense(data, current_user):
    clear_screen()
    speak("Add Expense. Enter the amount.")
    try:
        amount = float(input("Amount: "))
        user_ref = data["users"][current_user]
        if user_ref["balance"] < amount:
            speak("Insufficient balance for this expense.")
        else:
            category = input("Enter expense category: ")
            user_ref["balance"] -= amount
            user_ref["transactions"].append({
                "type": "expense", "amount": amount, "category": category, 
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_data(data)
            speak(f"Expense of {amount} recorded.")
    except ValueError:
        speak("Invalid amount entered.")
    input("Press Enter to continue...")

def view_transactions(data, current_user):
    clear_screen()
    speak(f"Viewing all transactions for {current_user}.")
    transactions = data["users"][current_user]["transactions"]
    if not transactions:
        speak("No records found.")
    else:
        print(f"{'ID':<4} | {'Type':<8} | {'Amount':<10} | {'Category/Source':<20} | {'Date'}")
        print("-" * 75)
        for i, t in enumerate(transactions):
            detail = t.get("category") if t["type"] == "expense" else t.get("source")
            print(f"{i:<4} | {t['type']:<8} | {t['amount']:<10.2f} | {detail:<20} | {t['date']}")
    
    current_bal = data["users"][current_user]["balance"]
    speak(f"Your current balance is {current_bal}.")
    input("\nPress Enter to return to menu...")

def delete_transaction(data, current_user):
    clear_screen()
    speak("Delete Transaction. Select an ID to remove.")
    transactions = data["users"][current_user]["transactions"]
    if not transactions:
        speak("There are no transactions to delete.")
        input("Press Enter...")
        return

    for i, t in enumerate(transactions):
        print(f"{i}. {t['type']} - {t['amount']} ({t['date']})")
    
    try:
        idx = int(input("\nEnter the ID number to delete: "))
        if 0 <= idx < len(transactions):
            removed = transactions.pop(idx)
            # Re-adjust balance based on deleted type
            if removed["type"] == "income":
                data["users"][current_user]["balance"] -= removed["amount"]
            else:
                data["users"][current_user]["balance"] += removed["amount"]
            
            save_data(data)
            speak("Transaction deleted and balance updated successfully.")
        else:
            speak("That is an invalid ID.")
    except ValueError:
        speak("Please enter a valid number.")
    input("Press Enter to continue...")

def main_menu():
    data = load_data()
    current_user = None

    while True:
        clear_screen()
        if current_user is None:
            print("1. Log In\n2. Sign Up\n3. Exit")
            speak("Welcome. Choose log in, sign up, or exit.")
            choice = input("Choice: ")
            if choice == '1': current_user = log_in(data)
            elif choice == '2': sign_up(data)
            elif choice == '3': 
                speak("Goodbye!")
                break
        else:
            print(f"--- Main Menu ({current_user}) ---")
            print("1. Add Income\n2. Add Expense\n3. View All Transactions\n4. Delete Transaction\n5. Log Out")
            speak("Select an option from the menu.")
            choice = input("Choice: ")
            
            if choice == '1': add_income(data, current_user)
            elif choice == '2': add_expense(data, current_user)
            elif choice == '3': view_transactions(data, current_user)
            elif choice == '4': delete_transaction(data, current_user)
            elif choice == '5': 
                speak("Logging out.")
                current_user = None

if __name__ == "__main__":
    main_menu()