
from pathlib import Path
import pandas as pd

# Project folders
DATA_FOLDER = Path(__file__).parent / "data"
CLEAN_FOLDER = DATA_FOLDER / "cleaned"
CLEAN_FOLDER.mkdir(parents=True, exist_ok=True)

# ---------- EXTRACT ----------
downloads = pd.read_excel(DATA_FOLDER / "digital_downloads.xlsx")
bookings = pd.read_csv(DATA_FOLDER / "study_room_bookings.csv")

# ---------- TRANSFORM: CLEAN DOWNLOADS ----------

# Remove extra spaces from text fields
downloads["student_number"] = (
    downloads["student_number"].astype("string").str.strip()
)
downloads["resource_title"] = (
    downloads["resource_title"].astype("string").str.strip()
)

# Standardize dates
downloads["download_date"] = pd.to_datetime(
    downloads["download_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# Convert download counts to numbers
downloads["download_count"] = pd.to_numeric(
    downloads["download_count"], errors="coerce"
)

# Identify invalid or missing values
invalid_downloads = (
    downloads["student_number"].isna()
    | downloads["student_number"].eq("")
    | downloads["resource_title"].isna()
    | downloads["resource_title"].eq("")
    | downloads["download_date"].isna()
    | downloads["download_count"].isna()
    | downloads["download_count"].le(0)
)

# ---------- TRANSFORM: CLEAN BOOKINGS ----------

bookings["student_number"] = (
    bookings["student_number"].astype("string").str.strip()
)
bookings["room_name"] = (
    bookings["room_name"].astype("string").str.strip()
)

bookings["booking_date"] = pd.to_datetime(
    bookings["booking_date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# Standardize time values
bookings["start_time"] = pd.to_datetime(
    bookings["start_time"], format="%H:%M", errors="coerce"
).dt.strftime("%H:%M:%S")

bookings["end_time"] = pd.to_datetime(
    bookings["end_time"], format="%H:%M", errors="coerce"
).dt.strftime("%H:%M:%S")

invalid_bookings = (
    bookings["student_number"].isna()
    | bookings["student_number"].eq("")
    | bookings["room_name"].isna()
    | bookings["room_name"].eq("")
    | bookings["booking_date"].isna()
    | bookings["start_time"].isna()
    | bookings["end_time"].isna()
    | (bookings["start_time"] >= bookings["end_time"])
)

# Report problems rather than silently deleting records
print("========== CLEANING REPORT ==========")
print("Download records:", len(downloads))
print("Invalid download records:", int(invalid_downloads.sum()))
print("Booking records:", len(bookings))
print("Invalid booking records:", int(invalid_bookings.sum()))

# Save cleaned records, including invalid rows for review
downloads.to_csv(
    CLEAN_FOLDER / "cleaned_downloads.csv", index=False
)
bookings.to_csv(
    CLEAN_FOLDER / "cleaned_bookings.csv", index=False
)

# Save invalid records separately so they can be investigated
downloads.loc[invalid_downloads].to_csv(
    CLEAN_FOLDER / "invalid_downloads.csv", index=False
)
bookings.loc[invalid_bookings].to_csv(
    CLEAN_FOLDER / "invalid_bookings.csv", index=False
)

print("\nCleaned files saved in:", CLEAN_FOLDER)
print("Cleaning completed!")
