import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import os

# Configuration for Ramadan 2026 as per your cities.json
RAMADAN_START_DATE = datetime(2026, 2, 19)
TOTAL_DAYS = 30
JSON_FILE_PATH = "cities.json"

def fetch_month_data(year, month, lat, lon):
    """Fetches prayer timings for a specific month using the Aladhan API."""
    # Method 1 = University of Islamic Sciences, Karachi (Standard for Pakistan)
    url = f"http://api.aladhan.com/v1/calendar/{year}/{month}?latitude={lat}&longitude={lon}&method=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('data', [])
    except urllib.error.URLError as e:
        print(f"Failed to connect to the API: {e}")
        return []

def generate_city_schedule(lat, lon):
    """Fetches and formats the 30-day schedule for the given coordinates."""
    print("Fetching data from API...")
    
    # We need data for February and March 2026
    feb_data = fetch_month_data(2026, 2, lat, lon)
    mar_data = fetch_month_data(2026, 3, lat, lon)
    all_data = feb_data + mar_data
    
    if not all_data:
        print("Could not retrieve data.")
        return None

    schedule = []
    
    for i in range(TOTAL_DAYS):
        current_date = RAMADAN_START_DATE + timedelta(days=i)
        target_gregorian = current_date.strftime("%d-%m-%Y")
        target_iso = current_date.strftime("%Y-%m-%d")
        
        # Find the matching date in the API response
        day_info = next((d for d in all_data if d['date']['gregorian']['date'] == target_gregorian), None)
        
        if day_info:
            # The API returns time like "05:25 (PKT)", we just need the "05:25" part
            # Sehri ends at Fajr time, Iftar is at Maghrib time
            sehr_time = day_info['timings']['Fajr'].split(' ')[0]
            iftar_time = day_info['timings']['Maghrib'].split(' ')[0]
            
            schedule.append({
                "day": i + 1,
                "date": target_iso,
                "sehr": sehr_time,
                "iftar": iftar_time
            })
            
    return schedule

def update_json_file(city_name, schedule_data):
    """Reads the existing JSON, adds the new city, and saves it with custom inline formatting."""
    data = {}
    
    # Load existing data if the file exists
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Warning: {JSON_FILE_PATH} is empty or corrupted. Creating a new one.")
            
    # Add or update the city
    data[city_name] = schedule_data
    
    # Save back to file using custom formatting to match the compact inline repo style
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write('{\n')
        cities = list(data.keys())
        for i, city in enumerate(cities):
            f.write(f'  "{city}": [\n')
            days = data[city]
            for j, day in enumerate(days):
                # Format each day exactly to the requested single line layout
                day_str = f'    {{ "day": {day["day"]}, "date": "{day["date"]}", "sehr": "{day["sehr"]}", "iftar": "{day["iftar"]}" }}'
                if j < len(days) - 1:
                    day_str += ','
                f.write(day_str + '\n')
            
            if i < len(cities) - 1:
                f.write('  ],\n')
            else:
                f.write('  ]\n')
        f.write('}\n')
        
    print(f"✅ Successfully added/updated '{city_name}' in {JSON_FILE_PATH}!")

def main():
    print("🌙 Roza Siyam - City Data Automator 🌙")
    print("---------------------------------------")
    print("Format: City, Latitude, Longitude")
    print("Example: Multan, 30.1575, 71.5249")
    
    while True:
        user_input = input("\nEnter data (or type 'exit' to quit): ").strip()
        
        if user_input.lower() == 'exit':
            break
            
        if not user_input:
            continue
            
        parts = [p.strip() for p in user_input.split(',')]
        
        if len(parts) != 3:
            print("❌ Invalid format! Please provide City, Latitude, and Longitude separated by commas.")
            continue
            
        city_name = parts[0]
        
        try:
            lat = float(parts[1])
            lon = float(parts[2])
        except ValueError:
            print("❌ Invalid coordinates! Latitude and Longitude must be numerical values.")
            continue
            
        schedule = generate_city_schedule(lat, lon)
        
        if schedule and len(schedule) == 30:
            update_json_file(city_name, schedule)
        else:
            print("❌ Failed to generate a complete 30-day schedule.")

if __name__ == "__main__":
    main()