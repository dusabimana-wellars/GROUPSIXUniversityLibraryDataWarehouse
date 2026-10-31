
import os
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="University Library Data Warehouse",
    page_icon="",
    layout="wide"
)

st.title("University Library Data Warehouse")
st.write(
    "Dashboard for analyzing book checkouts, digital downloads, "
    "and study room bookings."
)

st.divider()


# ==================================================
# 2. LOAD DATA FROM MYSQL
# ==================================================

@st.cache_data(ttl=60)
def load_data():

    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        raise ValueError(
            "MYSQL_PASSWORD is not set. Set your MySQL password "
            "in PowerShell before starting Streamlit."
        )

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="university_library"
    )

    try:

        downloads = pd.read_sql(
            """
            SELECT
                download_date,
                download_count
            FROM fact_download
            """,
            connection
        )

        rooms = pd.read_sql(
            """
            SELECT
                booking_id,
                room_name,
                booking_date,
                start_time,
                end_time
            FROM fact_room_booking
            """,
            connection
        )

        checkouts = pd.read_sql(
            """
            SELECT
                f.checkout_id,
                f.checkout_date,
                b.title,
                b.category
            FROM fact_checkout AS f
            JOIN dim_book AS b
                ON f.book_id = b.book_id
            """,
            connection
        )

        olap_data = pd.read_sql(
            """
            SELECT
                d.full_date,
                d.year_number,
                d.month_number,
                d.month_name,
                d.day_number,
                s.student_number,
                s.department,
                f.download_count
            FROM fact_download AS f
            JOIN dim_date AS d
                ON f.date_id = d.date_id
            JOIN dim_student AS s
                ON f.student_id = s.student_id
            """,
            connection
        )

        return downloads, rooms, checkouts, olap_data

    finally:
        connection.close()


# ==================================================
# 3. DISPLAY DASHBOARD
# ==================================================

try:

    downloads, rooms, checkouts, olap_data = load_data()

    # --------------------------------------------------
    # Convert date columns
    # --------------------------------------------------

    if not downloads.empty:
        downloads["download_date"] = pd.to_datetime(
            downloads["download_date"],
            errors="coerce"
        )

    if not rooms.empty:
        rooms["booking_date"] = pd.to_datetime(
            rooms["booking_date"],
            errors="coerce"
        )

    if not checkouts.empty:
        checkouts["checkout_date"] = pd.to_datetime(
            checkouts["checkout_date"],
            errors="coerce"
        )

    if not olap_data.empty:
        olap_data["full_date"] = pd.to_datetime(
            olap_data["full_date"],
            errors="coerce"
        )

        olap_data["download_count"] = pd.to_numeric(
            olap_data["download_count"],
            errors="coerce"
        ).fillna(0)

    # --------------------------------------------------
    # Calculate KPIs
    # --------------------------------------------------

    total_downloads = (
        pd.to_numeric(
            downloads["download_count"],
            errors="coerce"
        ).fillna(0).sum()
        if not downloads.empty else 0
    )

    total_bookings = len(rooms)
    total_checkouts = len(checkouts)

    # ==================================================
    # 4. HORIZONTAL NAVIGATION TABS
    # ==================================================

    tab_overview, tab_downloads, tab_rooms, tab_checkouts, tab_olap, tab_data = st.tabs(
        [
            "Overview",
            "Downloads",
            "Room Bookings",
            "Checkouts",
            "OLAP Analysis",
            "Data Preview"
        ]
    )

    # ==================================================
    # TAB 1: OVERVIEW
    # ==================================================

    with tab_overview:

        st.header("Dashboard Overview")

        st.write(
            "A summary of university library activities."
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Downloads",
            f"{total_downloads:,.0f}"
        )

        col2.metric(
            "Study Room Bookings",
            f"{total_bookings:,}"
        )

        col3.metric(
            "Book Checkouts",
            f"{total_checkouts:,}"
        )

        st.divider()

        st.subheader("Library Activity Summary")

        summary = pd.DataFrame({
            "Activity": [
                "Digital Downloads",
                "Study Room Bookings",
                "Book Checkouts"
            ],
            "Total Records": [
                total_downloads,
                total_bookings,
                total_checkouts
            ]
        })

        st.dataframe(
            summary,
            hide_index=True,
            width="stretch"
        )

        st.caption(
            "Summary of activities recorded in the library data warehouse."
        )

    # ==================================================
    # TAB 2: DIGITAL DOWNLOADS
    # ==================================================

    with tab_downloads:

        st.header("Digital Downloads")
        st.write(
            "Analyze digital resource downloads over time."
        )

        st.divider()

        st.subheader("Digital Downloads Over Time")

        if not downloads.empty:

            download_chart_data = downloads.dropna(
                subset=["download_date"]
            ).copy()

            if not download_chart_data.empty:

                download_chart_data = (
                    download_chart_data
                    .groupby(
                        "download_date",
                        as_index=False
                    )["download_count"]
                    .sum()
                    .sort_values("download_date")
                )

                fig_downloads = px.line(
                    download_chart_data,
                    x="download_date",
                    y="download_count",
                    markers=True,
                    title="Downloads by Date",
                    labels={
                        "download_date": "Date",
                        "download_count": "Number of Downloads"
                    }
                )

                fig_downloads.update_layout(
                    height=450,
                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig_downloads,
                    width="stretch"
                )

            else:
                st.info("No valid download dates are available.")

        else:
            st.info("No digital download records are available.")

        st.divider()

        st.subheader("Download Records")

        st.dataframe(
            downloads,
            hide_index=True,
            width="stretch"
        )

    # ==================================================
    # TAB 3: ROOM BOOKINGS
    # ==================================================

    with tab_rooms:

        st.header("Study Room Bookings")

        st.write(
            "Analyze the usage of study rooms in the university library."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Room Bookings",
                f"{total_bookings:,}"
            )

        with col2:

            unique_rooms = (
                rooms["room_name"].nunique()
                if not rooms.empty else 0
            )

            st.metric(
                "Number of Rooms Used",
                f"{unique_rooms:,}"
            )

        st.divider()

        st.subheader("Bookings by Room")

        if not rooms.empty:

            room_summary = (
                rooms.groupby("room_name")
                .size()
                .reset_index(name="booking_count")
                .sort_values(
                    "booking_count",
                    ascending=False
                )
            )

            fig_rooms = px.bar(
                room_summary,
                x="room_name",
                y="booking_count",
                text="booking_count",
                title="Study Room Usage",
                labels={
                    "room_name": "Room",
                    "booking_count": "Number of Bookings"
                }
            )

            fig_rooms.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_rooms,
                width="stretch"
            )

        else:
            st.info("No room booking records are available.")

        st.divider()

        st.subheader("Room Booking Records")

        st.dataframe(
            rooms,
            hide_index=True,
            width="stretch"
        )

    # ==================================================
    # TAB 4: BOOK CHECKOUTS
    # ==================================================

    with tab_checkouts:

        st.header("Book Checkouts")

        st.write(
            "Analyze books borrowed by students according to their categories."
        )

        st.divider()

        st.metric(
            "Total Book Checkouts",
            f"{total_checkouts:,}"
        )

        st.divider()

        st.subheader("Checkouts by Category")

        if not checkouts.empty:

            category_summary = (
                checkouts.groupby("category")
                .size()
                .reset_index(name="checkout_count")
                .sort_values(
                    "checkout_count",
                    ascending=False
                )
            )

            fig_categories = px.bar(
                category_summary,
                x="category",
                y="checkout_count",
                text="checkout_count",
                title="Book Checkout Categories",
                labels={
                    "category": "Book Category",
                    "checkout_count": "Number of Checkouts"
                }
            )

            fig_categories.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_categories,
                width="stretch"
            )

        else:
            st.info("No book checkout records are available.")

        st.divider()

        st.subheader("Book Checkout Records")

        st.dataframe(
            checkouts,
            hide_index=True,
            width="stretch"
        )

    # ==================================================
    # TAB 5: OLAP ANALYSIS
    # ==================================================

    with tab_olap:

        st.header("OLAP Analysis")

        st.write(
            "Explore digital download data using five OLAP operations."
        )

        st.divider()

        if olap_data.empty:

            st.warning(
                "No data is available for OLAP analysis. "
                "Check that fact_download contains records and that "
                "its date and student IDs match the dimension tables."
            )

        else:

            operation = st.selectbox(
                "Choose an OLAP operation",
                [
                    "Drill-down",
                    "Roll-up",
                    "Slice",
                    "Dice",
                    "Pivot"
                ]
            )

            st.divider()

            # --------------------------------------------------
            # 5.1 DRILL-DOWN
            # --------------------------------------------------

            if operation == "Drill-down":

                st.subheader("Drill-down: Year → Month → Day")

                years = sorted(
                    olap_data["year_number"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                if years:

                    selected_year = st.selectbox(
                        "Select year",
                        years,
                        key="drill_year"
                    )

                    year_data = olap_data[
                        olap_data["year_number"] == selected_year
                    ]

                    drill_level = st.radio(
                        "Choose detail level",
                        ["Month", "Day"],
                        horizontal=True
                    )

                    if drill_level == "Month":

                        result = (
                            year_data.groupby(
                                ["month_number", "month_name"],
                                as_index=False
                            )["download_count"]
                            .sum()
                            .sort_values("month_number")
                        )

                        st.dataframe(
                            result[
                                ["month_name", "download_count"]
                            ],
                            hide_index=True,
                            width="stretch"
                        )

                    else:

                        result = (
                            year_data.groupby(
                                [
                                    "month_number",
                                    "month_name",
                                    "day_number"
                                ],
                                as_index=False
                            )["download_count"]
                            .sum()
                            .sort_values(
                                ["month_number", "day_number"]
                            )
                        )

                        st.dataframe(
                            result[
                                [
                                    "month_name",
                                    "day_number",
                                    "download_count"
                                ]
                            ],
                            hide_index=True,
                            width="stretch"
                        )

                else:
                    st.info("No year information is available.")

            # --------------------------------------------------
            # 5.2 ROLL-UP
            # --------------------------------------------------

            elif operation == "Roll-up":

                st.subheader("Roll-up: Summarize Downloads")

                rollup_level = st.radio(
                    "Group data by",
                    ["Year", "Month"],
                    horizontal=True
                )

                if rollup_level == "Year":

                    result = (
                        olap_data.groupby(
                            "year_number",
                            as_index=False
                        )["download_count"]
                        .sum()
                        .sort_values("year_number")
                    )

                else:

                    result = (
                        olap_data.groupby(
                            [
                                "year_number",
                                "month_number",
                                "month_name"
                            ],
                            as_index=False
                        )["download_count"]
                        .sum()
                        .sort_values(
                            ["year_number", "month_number"]
                        )
                    )

                st.dataframe(
                    result,
                    hide_index=True,
                    width="stretch"
                )

                st.metric(
                    "Downloads in Selected Dataset",
                    f"{olap_data['download_count'].sum():,.0f}"
                )

            # --------------------------------------------------
            # 5.3 SLICE
            # --------------------------------------------------

            elif operation == "Slice":

                st.subheader("Slice: Analyze One Year")

                years = sorted(
                    olap_data["year_number"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                if years:

                    selected_year = st.selectbox(
                        "Choose a year",
                        years,
                        key="slice_year"
                    )

                    result = olap_data[
                        olap_data["year_number"] == selected_year
                    ]

                    st.write(
                        f"Showing data for {selected_year}."
                    )

                    st.dataframe(
                        result,
                        hide_index=True,
                        width="stretch"
                    )

                    st.metric(
                        "Downloads for This Year",
                        f"{result['download_count'].sum():,.0f}"
                    )

                else:
                    st.info("No year information is available.")

            # --------------------------------------------------
            # 5.4 DICE
            # --------------------------------------------------

            elif operation == "Dice":

                st.subheader(
                    "Dice: Filter Multiple Dimensions"
                )

                departments = sorted(
                    olap_data["department"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_departments = st.multiselect(
                    "Choose departments",
                    departments,
                    default=departments
                )

                valid_dates = olap_data["full_date"].dropna()

                if not valid_dates.empty:

                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()

                    date_range = st.date_input(
                        "Choose date range",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )

                    diced_data = olap_data[
                        olap_data["department"]
                        .astype(str)
                        .isin(selected_departments)
                    ].copy()

                    if isinstance(date_range, (tuple, list)):

                        if len(date_range) == 2:

                            start_date, end_date = date_range

                            diced_data = diced_data[
                                diced_data["full_date"].dt.date.between(
                                    start_date,
                                    end_date
                                )
                            ]

                        elif len(date_range) == 1:

                            diced_data = diced_data[
                                diced_data["full_date"].dt.date
                                == date_range[0]
                            ]

                    st.write("Filtered results:")

                    st.dataframe(
                        diced_data,
                        hide_index=True,
                        width="stretch"
                    )

                    st.metric(
                        "Downloads After Filtering",
                        f"{diced_data['download_count'].sum():,.0f}"
                    )

                else:
                    st.info(
                        "No valid dates are available for filtering."
                    )

            # --------------------------------------------------
            # 5.5 PIVOT
            # --------------------------------------------------

            elif operation == "Pivot":

                st.subheader(
                    "Pivot: Departments vs Months"
                )

                pivot_table = pd.pivot_table(
                    olap_data,
                    values="download_count",
                    index="department",
                    columns="month_name",
                    aggfunc="sum",
                    fill_value=0
                )

                month_order = (
                    olap_data[
                        ["month_number", "month_name"]
                    ]
                    .drop_duplicates()
                    .sort_values("month_number")["month_name"]
                    .tolist()
                )

                pivot_table = pivot_table.reindex(
                    columns=month_order,
                    fill_value=0
                )

                st.dataframe(
                    pivot_table,
                    width="stretch"
                )

                st.caption(
                    "Rows represent departments; columns represent months; "
                    "values represent total downloads."
                )

    # ==================================================
    # TAB 6: DATA PREVIEW
    # ==================================================

    with tab_data:

        st.header("Data Preview")

        st.write(
            "View the raw data retrieved from the MySQL database."
        )

        st.divider()

        with st.expander("Digital Downloads", expanded=True):

            st.dataframe(
                downloads,
                hide_index=True,
                width="stretch"
            )

        with st.expander("Study Room Bookings"):

            st.dataframe(
                rooms,
                hide_index=True,
                width="stretch"
            )

        with st.expander("Book Checkouts"):

            st.dataframe(
                checkouts,
                hide_index=True,
                width="stretch"
            )

        with st.expander("OLAP Download Data"):

            st.dataframe(
                olap_data,
                hide_index=True,
                width="stretch"
            )

    # ==================================================
    # 5. SUCCESS MESSAGE
    # ==================================================

    st.divider()

    st.success("Dashboard data loaded successfully.")

except Exception as error:

    st.error("The dashboard could not load its data.")

    st.exception(error)

    st.info(
        "Check your MySQL connection, MYSQL_PASSWORD environment "
        "variable, database table names, and column names."
    )
