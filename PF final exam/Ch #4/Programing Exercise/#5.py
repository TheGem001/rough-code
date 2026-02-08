# 5. Average Rainfall
# Write a program that uses nested loops to collect data and calculate the average rainfall over 
# a period of years. The program should first ask for the number of years. The outer loop will 
# iterate once for each year. The inner loop will iterate twelve times, once for each month. 
# Each iteration of the inner loop will ask the user for the inches of rainfall for that month. 
# After all iterations, the program should display the number of months, the total inches of 
# rainfall, and the average rainfall per month for the entire period.

total_years = int(input("Enter the number of years: "))
total_months = total_years * 12
total_rainfall = 0.0
for year in range(1, total_years + 1):
    print(f"Year {year}:")
    for month in range(1, 13):
        monthly_rainfall = float(input(f"  Enter the inches of rainfall for month {month}: "))
        total_rainfall += monthly_rainfall
average_rainfall = total_rainfall / total_months
print(f"\nNumber of months: {total_months}")
print(f"Total inches of rainfall: {total_rainfall}")
print(f"Average rainfall per month: {average_rainfall}")