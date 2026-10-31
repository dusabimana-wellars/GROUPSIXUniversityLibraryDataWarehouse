# University Library Analytics
## Dimensional Model Documentation

### 1. Introduction

The University Library Analytics Data Warehouse integrates library data from book checkouts, digital downloads, and study-room bookings. It supports reporting and analysis to help the university understand library resource usage.

### 2. Dimensional Modeling Approach

The project uses a dimensional model with three fact tables and three dimension tables. The design follows a shared-dimension approach, similar to a Fact Constellation (Galaxy) Schema, because multiple fact tables share common dimensions.

### 3. Dimension Tables

**3.1 dim_date**

Purpose: Stores calendar information for analyzing library activities over time.

Attributes:
- date_id — Primary key
- full_date
- day_number
- month_number
- month_name
- year_number

**3.2 dim_book**

Purpose: Stores information about books available for checkout analysis.

Attributes:
- book_id — Primary key
- title
- author
- category
- publication_year

**3.3 dim_student**

Purpose: Stores student information for analyzing library usage by department and study level.

Attributes:
- student_id — Primary key
- student_number
- department
- study_level

### 4. Fact Tables

**4.1 fact_checkout**

Purpose: Records book checkout activities.

Attributes:
- checkout_id — Primary key
- date_id — Foreign key to dim_date
- book_id — Foreign key to dim_book
- student_id — Foreign key to dim_student
- checkout_date
- return_date

**4.2 fact_download**

Purpose: Records digital resource downloads.

Attributes:
- download_id — Primary key
- date_id — Foreign key to dim_date
- student_id — Foreign key to dim_student
- resource_title
- download_date
- download_count

**4.3 fact_room_booking**

Purpose: Records study-room reservations.

Attributes:
- booking_id — Primary key
- date_id — Foreign key to dim_date
- student_id — Foreign key to dim_student
- room_name
- booking_date
- start_time
- end_time

### 5. Relationships

- dim_date connects to fact_checkout through date_id.
- dim_book connects to fact_checkout through book_id.
- dim_student connects to fact_checkout through student_id.
- dim_date connects to fact_download through date_id.
- dim_student connects to fact_download through student_id.
- dim_date connects to fact_room_booking through date_id.
- dim_student connects to fact_room_booking through student_id.

### 6. Analytical Benefits

The model supports:
- Book checkouts by category and date.
- Digital downloads by date and student department.
- Study-room bookings by room and date.
- Comparisons of library activity across departments and time periods.

### 7. Conclusion

The dimensional model provides a structured foundation for the University Library Analytics project. Shared dimensions enable consistent analysis across the three library activities, while the fact tables store the records needed for reporting and dashboards.