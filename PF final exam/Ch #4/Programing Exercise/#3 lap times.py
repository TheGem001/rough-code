# 3. Lap Times
# Write a program that asks the user to enter the number of times that they have run around 
# a racetrack, and then uses a loop to prompt them to enter the lap time for each of their laps. 
# When the loop finishes, the program should display the time of their fastest lap, the time of 
# their slowest lap, and their average lap time.

total_laps = int(input("Enter the number of laps you have run: "))
for x in range(total_laps):
    lap_time = float(input(f"Enter the time for lap {x + 1}: "))
    if x == 0:
        fastest_lap = lap_time
        slowest_lap = lap_time
        total_time = lap_time
    else:
        if lap_time < fastest_lap:
            fastest_lap = lap_time
        if lap_time > slowest_lap:
            slowest_lap = lap_time
        total_time += lap_time

print(f"Fastest lap time: {fastest_lap}")
print(f"Slowest lap time: {slowest_lap}")
average_time = total_time / total_laps
print(f"Average lap time: {average_time}")