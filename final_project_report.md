# UNIVERSITY LIBRARY DATA WAREHOUSE PROJECT

## 1. Introduction

A university library manages different types of information, including book checkouts, digital resource downloads, and study room bookings. Analyzing this information helps the university understand how students use library services.

This project develops a University Library Data Warehouse to organize library data, support analytical queries, and present useful information through an interactive dashboard. The system uses MySQL for data storage, Python for data processing and ETL, and Streamlit for data visualization.

## 2. Project Objectives

The main objectives of this project are:

1. To design and implement a dimensional data warehouse for university library data.
2. To organize library information using dimension tables and fact tables.
3. To develop an ETL process for loading data into the data warehouse.
4. To analyze book checkouts, digital downloads, and study room bookings.
5. To implement OLAP operations, including drill-down, roll-up, slice, dice, and pivot.
6. To develop an interactive dashboard for displaying library performance indicators and charts.
7. To validate the data warehouse using SQL queries and functional tests.

## 3. Technologies Used

- **MySQL:** Database management and data storage.
- **Python:** Data processing and ETL development.
- **Streamlit:** Interactive dashboard development.
- **Pandas:** Data manipulation and analysis.
- **VS Code:** Project development environment.
## 4. System Architecture and Dimensional Model

### 4.1 System Architecture

The University Library Data Warehouse follows an ETL-based architecture. Data is prepared and loaded into a MySQL database, where it can be analyzed and presented through a Streamlit dashboard.

The main components are:

1. **Source data:** Sample library data containing book checkouts, digital downloads, and study room bookings.
2. **ETL process:** Python scripts extract, transform, validate, and load data into the database.
3. **Data warehouse:** MySQL stores the data in dimension and fact tables.
4. **Analytical processing:** SQL queries and OLAP operations support data analysis.
5. **Visualization:** The Streamlit dashboard displays key performance indicators, charts, and interactive analytical results.

### 4.2 Dimensional Model

The data warehouse uses a dimensional model consisting of three dimension tables and three fact tables.

**Dimension tables**

- **DIM_STUDENT:** Stores student information, including student number, department, and study level.
- **DIM_BOOK:** Stores book information, including title, author, category, and publication year.
- **DIM_DATE:** Stores calendar information, including the full date, day, month, and year.

**Fact tables**

- **FACT_CHECKOUT:** Records book checkout activities and links students, books, and dates.
- **FACT_DOWNLOAD:** Records digital resource downloads, including the resource title, download date, student, and download count.
- **FACT_ROOM_BOOKING:** Records study room bookings, including the student, booking date, room name, start time, and end time.

The dimension tables provide descriptive information, while the fact tables store library activities and measurable values.

### 4.3 Relationships Between Tables

The fact tables use foreign keys to connect library activities to the appropriate dimensions.

- DIM_STUDENT connects to all three fact tables.
- DIM_DATE connects to all three fact tables.
- DIM_BOOK connects to FACT_CHECKOUT.

These relationships support analysis by student, date, book, and library activity.

## 5. Database Implementation and ETL Process

### 5.1 Database Implementation

The data warehouse was implemented using MySQL. The database named `university_library` was created to store both dimension tables and fact tables.

The implemented tables are:

| Table | Purpose |
|-------|---------|
| `dim_student` | Stores student information |
| `dim_book` | Stores book information |
| `dim_date` | Stores calendar information |
| `fact_checkout` | Stores book checkout transactions |
| `fact_download` | Stores digital download transactions |
| `fact_room_booking` | Stores study room booking transactions |

Primary keys uniquely identify each record, while foreign keys connect fact tables with their related dimensions.

### 5.2 ETL Process

The ETL (Extract, Transform, Load) process was developed using Python.

#### Extract

Sample library data was generated and prepared using Python scripts.

Example datasets included:

- Student records
- Book records
- Digital download records
- Study room booking records

#### Transform

During transformation:

- Student numbers were validated.
- Dates were standardized.
- Invalid records were checked.
- Download counts were prepared for analysis.

#### Load

The cleaned data was loaded into MySQL.

The ETL execution successfully loaded:

- **6 new digital download records**
- **6 new room booking records**
- **0 invalid records skipped**

This confirmed that the ETL process completed successfully.

### 5.3 Database Validation

SQL validation queries were executed to verify that the stored data matched the dashboard.

| Validation Test | Result | Status |
|-----------------|-------:|--------|
| Total Downloads | 7 | PASS |
| Total Room Bookings | 6 | PASS |
| Total Book Checkouts | 5 | PASS |

The SQL results matched the dashboard metrics, confirming that the database and dashboard were synchronized.
## 6. Dashboard and OLAP Analysis

### 6.1 Dashboard Implementation

An interactive dashboard was developed using Streamlit and connected to the MySQL data warehouse. It provides a simple interface for monitoring and analyzing university library activities.

The dashboard displays the following key performance indicators (KPIs):

- Total digital downloads.
- Total study room bookings.
- Total book checkouts.

It also includes visualizations showing downloads over time, bookings by room, and book checkouts by category.

### 6.2 OLAP Operations

Online Analytical Processing (OLAP) operations allow users to explore data from different perspectives.

The dashboard implements five OLAP operations:

**1. Drill-down**

Drill-down allows users to move from summarized information to more detailed information, such as moving from yearly downloads to monthly downloads.

**2. Roll-up**

Roll-up summarizes detailed information into higher-level groups, such as combining monthly downloads into yearly totals.

**3. Slice**

Slice filters the data using one selected dimension value, such as analyzing downloads for a particular year.

**4. Dice**

Dice filters data using multiple conditions, such as selecting a particular year and department for analysis.

**5. Pivot**

Pivot changes how data is arranged in a report to compare different dimensions and measures.

These operations help users investigate library usage patterns and generate useful analytical insights.

### 6.3 Dashboard Screenshots

Insert screenshots of the completed dashboard in this section.

- **Figure 1:** Main dashboard showing the KPI metrics and charts.
- **Figure 2:** Drill-down operation results.
- **Figure 3:** Roll-up operation results.
- **Figure 4:** Slice and dice operation results.
- **Figure 5:** Pivot operation results.

Each screenshot should clearly show the relevant dashboard section and its results.

### 6.4 Benefits of the Dashboard

The dashboard provides a convenient way to monitor library activities, compare usage patterns, and explore data interactively. It reduces the need to inspect raw database records manually and makes analytical results easier to understand.
## 7. Testing and Validation

### 7.1 Database Testing

SQL queries were used to validate the data stored in the MySQL data warehouse.

| Test | Expected Result | Actual Result | Status |
|---|---:|---:|---|
| Total downloads | 7 | 7 | PASS |
| Total room bookings | 6 | 6 | PASS |
| Total book checkouts | 5 | 5 | PASS |

The three database validation tests passed.

### 7.2 ETL Testing

The ETL process was executed successfully. Six new download records and six new room booking records were loaded, and zero invalid or unmatched records were skipped during that execution.

### 7.3 Dashboard and OLAP Testing

The Streamlit dashboard was launched successfully. It displays key performance indicators and charts for library activities.

The five implemented OLAP operations—drill-down, roll-up, slice, dice, and pivot—were reported to work during functional testing.

Further testing should confirm that each operation returns the correct results for different selections and that dashboard totals remain consistent with the database.

## 8. Challenges and Solutions

During development, several technical challenges were encountered, including database connectivity, Python environment configuration, and dashboard code errors.

These challenges were addressed by installing and configuring the required software, testing the MySQL connection, correcting the Python environment, and updating the dashboard code.

## 9. Conclusion

The University Library Data Warehouse project demonstrates how library data can be organized, processed, analyzed, and visualized using MySQL, Python, and Streamlit.

The project includes dimension and fact tables, an ETL process, an interactive dashboard, and five OLAP operations. Database validation confirmed totals