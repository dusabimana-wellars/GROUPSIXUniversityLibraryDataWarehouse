
from pathlib import Path
import os
import pandas as pd
import mysql.connector

PROJECT_FOLDER = Path(__file__).parent
DATA_FOLDER = PROJECT_FOLDER / "data" / "cleaned"

downloads = pd.read_csv(DATA_FOLDER / "cleaned_downloads.csv")
bookings = pd.read_csv(DATA_FOLDER / "cleaned_bookings.csv")

password = os.getenv("MYSQL_PASSWORD")
if not password:
    raise ValueError(
        "MYSQL_PASSWORD is missing. Set it in your terminal first."
    )

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="university_library",
    port=3306
)

cursor = connection.cursor()
downloaded_count = 0
booked_count = 0
skipped_count = 0

try:
    connection.start_transaction()

    # Load digital download records
    for _, row in downloads.iterrows():
        student_number = str(row["student_number"]).strip()
        resource_title = str(row["resource_title"]).strip()
        download_date = row["download_date"]
        count = pd.to_numeric(row["download_count"], errors="coerce")

        if (
            not student_number
            or not resource_title
            or pd.isna(download_date)
            or pd.isna(count)
            or count <= 0
        ):
            skipped_count += 1
            continue

        student_date = pd.to_datetime(download_date, errors="coerce")
        if pd.isna(student_date):
            skipped_count += 1
            continue

        download_date = student_date.strftime("%Y-%m-%d")

        cursor.execute(
            "SELECT student_id FROM dim_student "
            "WHERE student_number = %s",
            (student_number,)
        )
        student = cursor.fetchone()

        cursor.execute(
            "SELECT date_id FROM dim_date WHERE full_date = %s",
            (download_date,)
        )
        date = cursor.fetchone()

        if not student or not date:
            print("Skipping download: student/date not found:",
                  student_number, download_date)
            skipped_count += 1
            continue

        student_id = student[0]
        date_id = date[0]
        count = int(count)

        cursor.execute(
            """
            SELECT download_id FROM fact_download
            WHERE date_id = %s
              AND student_id = %s
              AND resource_title = %s
              AND download_date = %s
              AND download_count = %s
            """,
            (date_id, student_id, resource_title, download_date, count)
        )

        if cursor.fetchone():
            continue

        cursor.execute(
            """
            INSERT INTO fact_download
            (date_id, student_id, resource_title,
             download_date, download_count)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (date_id, student_id, resource_title, download_date, count)
        )
        downloaded_count += 1

    # Load study-room booking records
    for _, row in bookings.iterrows():
        student_number = str(row["student_number"]).strip()
        room_name = str(row["room_name"]).strip()

        booking_date = pd.to_datetime(
            row["booking_date"], errors="coerce"
        )

        start_time = str(row["start_time"]).strip()
        end_time = str(row["end_time"]).strip()

        if (
            not student_number
            or not room_name
            or pd.isna(booking_date)
            or pd.isna(start_time)
            or pd.isna(end_time)
            or start_time >= end_time
        ):
            skipped_count += 1
            continue

        booking_date = booking_date.strftime("%Y-%m-%d")

        cursor.execute(
            "SELECT student_id FROM dim_student "
            "WHERE student_number = %s",
            (student_number,)
        )
        student = cursor.fetchone()

        cursor.execute(
            "SELECT date_id FROM dim_date WHERE full_date = %s",
            (booking_date,)
        )
        date = cursor.fetchone()

        if not student or not date:
            print("Skipping booking: student/date not found:",
                  student_number, booking_date)
            skipped_count += 1
            continue

        student_id = student[0]
        date_id = date[0]

        cursor.execute(
            """
            SELECT booking_id FROM fact_room_booking
            WHERE date_id = %s
              AND student_id = %s
              AND room_name = %s
              AND booking_date = %s
              AND start_time = %s
              AND end_time = %s
            """,
            (date_id, student_id, room_name, booking_date,
             start_time, end_time)
        )

        if cursor.fetchone():
            continue

        cursor.execute(
            """
            INSERT INTO fact_room_booking
            (date_id, student_id, room_name, booking_date,
             start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (date_id, student_id, room_name, booking_date,
             start_time, end_time)
        )
        booked_count += 1

    connection.commit()

    print("\n========== ETL LOAD REPORT ==========")
    print("New download records loaded:", downloaded_count)
    print("New booking records loaded:", booked_count)
    print("Invalid or unmatched records skipped:", skipped_count)

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()

print("ETL loading process finished.")
