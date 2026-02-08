import json
import pyttsx3
import os
import datetime

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Text-to-speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main Menu
def main_menu():
    clear_screen()
    print("Welcome to the Application")
    print("1. Add Amount")
    print("2. Add Expense")
    print("4. Get Report")
    print("5. turn on/off voice assistant")
    print("6. Logout")
    speak("Welcome to the Application")
    choice = input("Please select an option: ")
    return choice


if __name__ == "__main__":
    main_menu()