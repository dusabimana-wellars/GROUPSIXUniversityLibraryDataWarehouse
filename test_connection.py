
import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Wellars@500",
        database="university_library",
        port=3306
    )

    if connection.is_connected():
        print("Successfully connected to MySQL!")
        print("Database: university_library")

    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)
