
from pathlib import Path
import pandas as pd

# Location of the data folder
DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(exist_ok=True)

# Sample study-room booking records
bookings = [
    {
        "student_number": "ST001",
        "room_name": "Room A",
        "booking_date": "2026-10-20",
        "start_time": "09:00",
        "end_time": "10:00"
    },
    {
        "student_number": "ST002",
        "room_name": "Room B",
        "booking_date": "2026-10-20",
        "start_time": "10:00",
        "end_time": "11:00"
    },
    {
        "student_number": "ST003",
        "room_name": "Room A",
        "booking_date": "2026-10-21",
        "start_time": "13:00",
        "end_time": "15:00"
    },
    {
        "student_number": "ST001",
        "room_name": "Room C",
        "booking_date": "2026-10-22",
        "start_time": "08:00",
        "end_time": "09:00"
    },
    {
        "student_number": "ST004",
        "room_name": "Room B",
        "booking_date": "2026-10-23",
        "start_time": "14:00",
        "end_time": "16:00"
    },
    {
        "student_number": "ST002",
        "room_name": "Room A",
        "booking_date": "2026-10-23",
        "start_time": "11:00",
        "end_time": "12:00"
    }
]

df = pd.DataFrame(bookings)

# Save as a CSV file
output_file = DATA_FOLDER / "study_room_bookings.csv"
df.to_csv(output_file, index=False)

print("CSV sample data created successfully!")
print(f"File location: {output_file}")
print("\nSample records:")
print(df)
