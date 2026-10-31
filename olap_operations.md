# University Library Analytics
## OLAP Operations Documentation

### 1. Introduction

Online Analytical Processing (OLAP) allows users to analyze data from different perspectives. This project uses MySQL queries to demonstrate five OLAP operations on library digital-download data.

### 2. Drill-down

Drill-down displays more detailed data. In this project, downloads are grouped by year, month, and day to show daily activity.

### 3. Roll-up

Roll-up summarizes detailed data into a higher level. In this project, daily downloads are summarized by year and month. The October 2026 sample data contains 7 downloads.

### 4. Slice

Slice filters the data using one selected value. In this project, the query selects download records for the year 2026.

### 5. Dice

Dice filters data using multiple conditions. In this project, the query selects downloads for the Computer Science and Data Science departments within a specified date range.

### 6. Pivot

Pivot rearranges data to support comparisons across categories. In this project, conditional aggregation creates separate October and November download columns for each student department.

### 7. Conclusion

The five OLAP operations demonstrate how the University Library Analytics Data Warehouse can support detailed analysis, summaries, filtering, and comparisons of library digital-resource usage.