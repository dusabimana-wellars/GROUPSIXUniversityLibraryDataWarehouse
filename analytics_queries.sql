
USE university_library;

-- QUERY 1: Digital downloads by date
SELECT
    download_date,
    COUNT(*) AS download_transactions,
    SUM(download_count) AS total_downloads
FROM fact_download
GROUP BY download_date
ORDER BY download_date;


-- QUERY 2: Most-used study rooms
SELECT
    room_name,
    COUNT(*) AS total_bookings,
    SUM(
        TIMESTAMPDIFF(MINUTE, start_time, end_time)
    ) AS total_minutes_booked
FROM fact_room_booking
GROUP BY room_name
ORDER BY total_bookings DESC;


-- QUERY 3: Book checkouts by category
SELECT
    b.category,
    COUNT(*) AS total_checkouts
FROM fact_checkout f
JOIN dim_book b
    ON f.book_id = b.book_id
GROUP BY b.category
ORDER BY total_checkouts DESC;


-- QUERY 4: Downloads by student department
SELECT
    s.department,
    SUM(f.download_count) AS total_downloads
FROM fact_download f
JOIN dim_student s
    ON f.student_id = s.student_id
GROUP BY s.department
ORDER BY total_downloads DESC;
