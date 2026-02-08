# 2. Calories Burned
# Running on a particular treadmill you burn 4.2 calories per minute. Write a program that 
# uses a loop to display the number of calories burned after 10, 15, 20, 25, and 30 minutes.

calories_per_minute = 4.2
for minutes in [10, 15, 20, 25, 30]:
    calories_burned = calories_per_minute * minutes
    print(f"Calories burned after {minutes} minutes: {calories_burned}")