# <!-- 4. Distance Traveled
# The distance a vehicle travels can be calculated as follows:
# distance 5 speed 3 time
# For example, if a train travels 40 miles per hour for three hours, the distance traveled is 
# 120 miles. Write a program that asks the user for the speed of a vehicle (in miles per hour) 
# and the number of hours it has traveled. It should then use a loop to display the distance 
# the vehicle has traveled for each hour of that time period. Here is an example of the desired 
# output:
# What is the speed of the vehicle in mph? 40 Enter
# How many hours has it traveled? 3 Enter
# Hour         Distance Traveled
# 1                    40
# 2                    80
# 3                   120 -->

speed_of_vehicle = int(input("What is the speed of the vehicle in mph? "))
hours_traveled = int(input("How many hours has it traveled? "))

print("Hour         Distance Traveled")
for hour in range(1, hours_traveled + 1):
    distance = speed_of_vehicle * hour
    print(f"{hour}                    {distance}")