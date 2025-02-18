import pandas as pd

# Define weekly plan structure
weeks = list(range(13, 33))  # From Week 13 post-surgery to race week

# Initialize columns
training_plan = {
    "Week": weeks,
    "Focus": [
        "Strength & Mobility" if w < 17 else
        "Walk-Jog Progression" if w < 21 else
        "Building Running Volume" if w < 25 else
        "Half Marathon Prep" if w < 31 else
        "Race Tapering"
        for w in weeks
    ],
    "Running Workouts": [
        "No running, focus on walking and PT exercises" if w < 17 else
        "Walk 3-4x per week, introduce 1-2 min jog intervals" if w < 21 else
        "Jog 3-4x per week, increase distance weekly" if w < 25 else
        "Run 3-4x per week, long runs up to 10-11 miles" if w < 31 else
        "Reduce mileage, taper for race"
        for w in weeks
    ],
    "Strength & Mobility": [
        "Calf raises, balance work, stretching (daily)" for _ in weeks
    ],
    "Cross-Training": [
        "Cycling/Swimming 2-3x per week" if w < 17 else
        "Cross-train 1-2x per week as needed" for w in weeks
    ],
    "Long Run Distance (miles)": [
        "N/A" if w < 17 else
        "2-4 miles (walk/jog mix)" if w < 21 else
        "4-7 miles" if w < 25 else
        "8-11 miles" if w < 31 else
        "Reduce mileage (6-8 miles max)"
        for w in weeks
    ]
}

# Convert to DataFrame
df = pd.DataFrame(training_plan)

# Save to Excel file
file_path = "/mnt/data/achilles_half_marathon_plan.xlsx"
df.to_excel(file_path, index=False)

file_path
