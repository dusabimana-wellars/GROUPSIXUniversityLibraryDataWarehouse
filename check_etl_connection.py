
from pathlib import Path
import os
import mysql.connector
import pandas as pd

PROJECT_FOLDER = Path(__file__).parent
DATA_FOLDER = PROJECT_FOLDER / "data" / "cleaned"

try:
    # Check that the cleaned files exist and can be read
    downloads = pd.read_csv(DATA_FOLDER / "cleaned_downloads.csv")
    bookings = pd.read_csv(DATA_FOLDER / "cleaned_bookings.csv")

    print("Cleaned download records:", len(downloads))
    print("Cleaned booking records:", len(bookings))

    # Connect to MySQL using environment variables
    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        raise ValueError(
            "MYSQL_PASSWORD is not set. Set it in the terminal first."
        )

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="university_library",
        port=3306
    )

    cursor = connection.cursor()

    print("\nMySQL connection successful!")
    print("\nExisting table record counts:")

    for table in [
        "dim_student",
        "dim_book",
        "dim_date",
        "fact_checkout",
        "fact_download",
        "fact_room_booking"
    ]:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")

    cursor.close()
    connection.close()

except Exception as error:
    print("Check failed:", error)
