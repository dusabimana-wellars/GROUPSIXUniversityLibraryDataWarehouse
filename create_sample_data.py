
from pathlib import Path
import pandas as pd

# Create the data folder
DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(exist_ok=True)

# Sample digital library downloads
downloads = [
    {
        "student_number": "ST001",
        "resource_title": "Introduction to Python",
        "download_date": "2026-10-20",
        "download_count": 1
    },
    {
        "student_number": "ST002",
        "resource_title": "Database Systems",
        "download_date": "2026-10-21",
        "download_count": 1
    },
    {
        "student_number": "ST003",
        "resource_title": "Data Analytics",
        "download_date": "2026-10-21",
        "download_count": 2
    },
    {
        "student_number": "ST001",
        "resource_title": "Web Development",
        "download_date": "2026-10-22",
        "download_count": 1
    },
    {
        "student_number": "ST004",
        "resource_title": "Computer Networks",
        "download_date": "2026-10-23",
        "download_count": 1
    },
    {
        "student_number": "ST002",
        "resource_title": "Introduction to Python",
        "download_date": "2026-10-23",
        "download_count": 1
    }
]

# Convert records to a DataFrame
df = pd.DataFrame(downloads)

# Save the Excel file
output_file = DATA_FOLDER / "digital_downloads.xlsx"
df.to_excel(output_file, index=False)

print("Excel sample data created successfully!")
print(f"File location: {output_file}")
print("\nSample records:")
print(df)
