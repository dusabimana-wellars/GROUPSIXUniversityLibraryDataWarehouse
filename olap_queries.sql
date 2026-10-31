
USE university_library;

-- OLAP 1: DRILL-DOWN
-- View downloads by year, month, and day.
SELECT
    YEAR(download_date) AS download_year,
    MONTH(download_date) AS download_month,
    DAY(download_date) AS download_day,
    SUM(download_count) AS total_downloads
FROM fact_download
GROUP BY
    YEAR(download_date),
    MONTH(download_date),
    DAY(download_date)
ORDER BY
    download_year,
    download_month,
    download_day;

-- OLAP 2: ROLL-UP
-- Summarize downloads by year and month.
SELECT
    YEAR(download_date) AS download_year,
    MONTH(download_date) AS download_month,
    SUM(download_count) AS total_downloads
FROM fact_download
GROUP BY
    YEAR(download_date),
    MONTH(download_date)
ORDER BY
    download_year,
    download_month;

-- OLAP 3: SLICE
-- View downloads for one year.
SELECT
    download_date,
    SUM(download_count) AS total_downloads
FROM fact_download
WHERE YEAR(download_date) = 2026
GROUP BY download_date
ORDER BY download_date;

-- OLAP 4: DICE
-- View downloads for selected departments and dates.
SELECT
    s.department,
    f.download_date,
    SUM(f.download_count) AS total_downloads
FROM fact_download f
JOIN dim_student s
    ON f.student_id = s.student_id
WHERE s.department IN ('Computer Science', 'Data Science')
  AND f.download_date BETWEEN '2026-10-20' AND '2026-10-23'
GROUP BY s.department, f.download_date
ORDER BY s.department, f.download_date;

-- OLAP 5: PIVOT
-- Compare downloads across departments and months.
SELECT
    s.department,
    SUM(
        CASE WHEN MONTH(f.download_date) = 10
        THEN f.download_count ELSE 0 END
    ) AS october_downloads,
    SUM(
        CASE WHEN MONTH(f.download_date) = 11
        THEN f.download_count ELSE 0 END
    ) AS november_downloads
FROM fact_download f
JOIN dim_student s
    ON f.student_id = s.student_id
GROUP BY s.department
ORDER BY s.department;
