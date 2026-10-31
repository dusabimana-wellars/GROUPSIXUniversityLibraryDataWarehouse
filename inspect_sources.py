
from pathlib import Path
import pandas as pd

# Find the project data folder
DATA_FOLDER = Path(__file__).parent / "data"

excel_file = DATA_FOLDER / "digital_downloads.xlsx"
csv_file = DATA_FOLDER / "study_room_bookings.csv"

# Extract data from Excel
downloads = pd.read_excel(excel_file)

# Extract data from CSV
bookings = pd.read_csv(csv_file)

print("\n========== DIGITAL DOWNLOADS ==========")
print(downloads.to_string(index=False))

print("\n========== STUDY ROOM BOOKINGS ==========")
print(bookings.to_string(index=False))

print("\n========== SOURCE SUMMARY ==========")
print("Number of download records:", len(downloads))
print("Number of booking records:", len(bookings))

print("\nColumn names:")
print("Downloads:", downloads.columns.tolist())
print("Bookings:", bookings.columns.tolist())
