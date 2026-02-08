import os
import pyttsx3
import json
from datetime import datetime

DB_FILE = "finance_data.json"

def speak(text):
    print(f"🎙️ AI: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Sound Error: {e}")

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"users": {"admin": {"password": "123", "expenses": []}}}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()
current_user = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def auth_menu():
    global current_user
    while True:
        clear_screen()
        print("=== WELCOME TO FINANCE AI ===")
        print("1. Login\n2. Sign Up\n3. Exit")
        choice = input("\nChoose: ")
        if choice == '1':
            u, p = input("Username: "), input("Password: ")
            if u in data["users"] and data["users"][u]["password"] == p:
                current_user = u
                speak(f"Access granted. Welcome {u}.")
                main_dashboard()
            else: 
                speak("Incorrect credentials.")
                input("Press Enter to try again...")
        elif choice == '2':
            new_u, new_p = input("New Username: "), input("New Password: ")
            if not new_u or not new_p:
                speak("Username/Password cannot be empty.")
                input("Press Enter...")
            elif new_u in data["users"]: 
                speak("User already exists.")
                input("Press Enter...")
            else:
                data["users"][new_u] = {"password": new_p, "expenses": []}
                save_data(data)
                speak("Account created!")
                input("Press Enter to continue...")
        elif choice == '3': break

def add_expense():
    clear_screen()
    item = input("Item Name: ")
    try:
        cost = float(input("Amount (Rs.): "))
        exps = data["users"][current_user]["expenses"]
        # Generate ID based on Max ID + 1 to avoid duplicates
        new_id = max([e["id"] for e in exps], default=0) + 1
        entry = {"id": new_id, "item": item, "cost": cost, "date": datetime.now().strftime("%Y-%m-%d")}
        data["users"][current_user]["expenses"].append(entry)
        save_data(data)
        speak("Recorded.")
    except ValueError: 
        speak("Invalid number.")
        input("Press Enter...")

def update_expense():
    view_history(pause=False)
    try:
        target = int(input("\nEnter ID to update: "))
        for e in data["users"][current_user]["expenses"]:
            if e["id"] == target:
                e["item"] = input(f"New name ({e.get('item', e.get('name'))}): ") or e.get('item', e.get('name'))
                new_cost = input(f"New cost ({e['cost']}): ")
                if new_cost: # Only try to convert if user typed something
                    e["cost"] = float(new_cost)
                save_data(data)
                speak("Updated successfully.")
                return
        speak("ID not found.")
        input("Press Enter...")
    except ValueError: 
        speak("Invalid input.")
        input("Press Enter...")

def delete_expense():
    view_history(pause=False)
    try:
        target = int(input("\nEnter ID to delete: "))
        orig_len = len(data["users"][current_user]["expenses"])
        data["users"][current_user]["expenses"] = [e for e in data["users"][current_user]["expenses"] if e["id"] != target]
        if len(data["users"][current_user]["expenses"]) < orig_len:
            save_data(data)
            speak("Deleted.")
        else: 
            speak("ID not found.")
            input("Press Enter...")
    except ValueError: 
        speak("Invalid input.")
        input("Press Enter...")

def view_history(pause=True):
    clear_screen()
    exps = data["users"][current_user]["expenses"]
    if not exps: 
        speak("History is empty.")
    else:
        print(f"{'ID':<4} | {'Item':<15} | {'Cost':<10}")
        print("-" * 35)
        for e in exps: 
            name = e.get('item') or e.get('name') # Compatibility with GUI keys
            print(f"{e['id']:<4} | {name:<15} | Rs.{e['cost']:,.2f}")
    if pause: input("\nPress Enter to return...")

def main_dashboard():
    while True:
        clear_screen()
        total = sum(e["cost"] for e in data["users"][current_user]["expenses"])
        print(f"=== {current_user.upper()}'S DASHBOARD ===\n💰 TOTAL: Rs.{total:,.2f}\n" + "-"*25)
        print("1. Add\n2. View\n3. Update\n4. Delete\n5. Logout")
        choice = input("\nChoose: ")
        if choice == '1': add_expense()
        elif choice == '2': view_history()
        elif choice == '3': update_expense()
        elif choice == '4': delete_expense()
        elif choice == '5': break

if __name__ == "__main__":
    auth_menu()