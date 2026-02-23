import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import os
import time

# Configuration
RAMADAN_START_DATE = datetime(2026, 2, 19)
TOTAL_DAYS = 30
JSON_FILE_PATH = "cities.json"
INPUT_FILE_PATH = "input_cities.txt"

def adjust_time(time_str, offset_minutes):
    """Adjusts the given HH:MM time by a specific number of minutes."""
    if not time_str or offset_minutes == 0:
        return time_str
    
    time_obj = datetime.strptime(time_str, "%H:%M")
    adjusted_time = time_obj + timedelta(minutes=offset_minutes)
    return adjusted_time.strftime("%H:%M")

def fetch_month_data(year, month, lat, lon):
    """Fetches prayer timings for a specific month using the Aladhan API (Karachi Method)."""
    url = f"http://api.aladhan.com/v1/calendar/{year}/{month}?latitude={lat}&longitude={lon}&method=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('data', [])
    except urllib.error.URLError as e:
        print(f"  [!] Failed to connect to the API: {e}")
        return []

def generate_city_schedule(lat, lon, sehr_offset=0, iftar_offset=0):
    """Generates the 30-day schedule and applies any manual minute offsets."""
    feb_data = fetch_month_data(2026, 2, lat, lon)
    mar_data = fetch_month_data(2026, 3, lat, lon)
    all_data = feb_data + mar_data
    
    if not all_data:
        return None

    schedule = []
    
    for i in range(TOTAL_DAYS):
        current_date = RAMADAN_START_DATE + timedelta(days=i)
        target_gregorian = current_date.strftime("%d-%m-%Y")
        target_iso = current_date.strftime("%Y-%m-%d")
        
        day_info = next((d for d in all_data if d['date']['gregorian']['date'] == target_gregorian), None)
        
        if day_info:
            base_sehr = day_info['timings']['Fajr'].split(' ')[0]
            base_iftar = day_info['timings']['Maghrib'].split(' ')[0]
            
            final_sehr = adjust_time(base_sehr, sehr_offset)
            final_iftar = adjust_time(base_iftar, iftar_offset)
            
            schedule.append({
                "day": i + 1,
                "date": target_iso,
                "sehr": final_sehr,
                "iftar": final_iftar
            })
            
    return schedule

def update_json_file(city_name, schedule_data):
    """Saves the generated data to the JSON file in a single-line format."""
    data = {}
    
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            pass
            
    data[city_name] = schedule_data
    
    # Save with custom inline formatting
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write('{\n')
        cities = list(data.keys())
        for i, city in enumerate(cities):
            f.write(f'  "{city}": [\n')
            days = data[city]
            for j, day in enumerate(days):
                day_str = f'    {{ "day": {day["day"]}, "date": "{day["date"]}", "sehr": "{day["sehr"]}", "iftar": "{day["iftar"]}" }}'
                if j < len(days) - 1:
                    day_str += ','
                f.write(day_str + '\n')
            
            if i < len(cities) - 1:
                f.write('  ],\n')
            else:
                f.write('  ]\n')
        f.write('}\n')

def main():
    print("🌙 Roza Siyam - BATCH City Automator 🌙")
    print("-" * 50)
    
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"❌ Could not find '{INPUT_FILE_PATH}'. Please create it in the same folder.")
        return

    # Read the input file
    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    success_count = 0
    total_cities = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue # Skip empty lines or comments
            
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 3:
            print(f"⏭️ Skipping invalid line: {line}")
            continue
            
        total_cities += 1
        city_name = parts[0]
        
        try:
            lat = float(parts[1])
            lon = float(parts[2])
            sehr_offset = int(parts[3]) if len(parts) > 3 else 0
            iftar_offset = int(parts[4]) if len(parts) > 4 else 0
        except ValueError:
            print(f"⏭️ Skipping {city_name} - invalid numbers.")
            continue

        print(f"[{total_cities}] Processing {city_name}...", end=" ", flush=True)
        
        schedule = generate_city_schedule(lat, lon, sehr_offset, iftar_offset)
        
        if schedule and len(schedule) == 30:
            update_json_file(city_name, schedule)
            print("✅ Done!")
            success_count += 1
        else:
            print("❌ Failed.")
            
        # Pause for 1.5 seconds to avoid overloading the API
        time.sleep(1.5)

    print("-" * 50)
    print(f"🎉 Batch Process Complete! Successfully saved {success_count} out of {total_cities} cities to {JSON_FILE_PATH}.")

if __name__ == "__main__":
    main()