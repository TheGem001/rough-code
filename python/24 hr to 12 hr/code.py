import json
from datetime import datetime
import os

def convert_to_12hr_format(time_str):
    """
    Converts a 24-hour time string (e.g., '17:56') to a 12-hour format without AM/PM (e.g., '05:56').
    """
    try:
        # Parse the string into a datetime object using 24-hour format (%H:%M)
        time_obj = datetime.strptime(time_str, "%H:%M")
        # Format the datetime object back into a string using 12-hour format (%I:%M) without AM/PM
        return time_obj.strftime("%I:%M")
    except ValueError:
        # If the time is invalid or already converted, return it as is to avoid crashing
        return time_str

def main():
    input_filename = 'cities.json'
    output_filename = 'cities_12hr.json'

    # 1. Check if the input file exists
    if not os.path.exists(input_filename):
        print(f"Error: The file '{input_filename}' was not found in the current directory.")
        return

    # 2. Load the JSON data
    print(f"Loading data from '{input_filename}'...")
    with open(input_filename, 'r', encoding='utf-8') as file:
        cities_data = json.load(file)

    # 3. Iterate through the cities and their daily timings to convert the times
    print("Converting times to 12-hour format...")
    for city, timings in cities_data.items():
        for day in timings:
            # Check and convert 'sehr'
            if 'sehr' in day:
                day['sehr'] = convert_to_12hr_format(day['sehr'])
            
            # Check and convert 'iftar'
            if 'iftar' in day:
                day['iftar'] = convert_to_12hr_format(day['iftar'])

    # 4. Save the modified data to a new JSON file
    print(f"Saving updated data to '{output_filename}'...")
    with open(output_filename, 'w', encoding='utf-8') as file:
        # indent=2 makes the JSON file nicely formatted and readable
        json.dump(cities_data, file, indent=2)

    print("Conversion complete! Your new file is ready.")

if __name__ == "__main__":
    main()