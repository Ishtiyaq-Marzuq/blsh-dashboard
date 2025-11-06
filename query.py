import duckdb
import pandas as pd
import datetime
from datetime import datetime

# --- Home Tab Queries ---

def today_sales(df):
    """Calculate total sales for today."""
    query = """
        SELECT SUM("Bill Amount") AS total_sales_today
        FROM df
        WHERE DATE(Timestamp) = DATE(CURRENT_DATE)
    """
    return duckdb.query(query).df()


def today_customer_count(df):
    """Count of distinct customers visited today."""
    query = """
        SELECT COUNT(DISTINCT Name) AS customers_today
        FROM df
        WHERE DATE(Timestamp) = DATE(CURRENT_DATE)
    """
    return duckdb.query(query).df()

# ========== 🧾 TIME-BASED SERVICE QUERIES ==========

def weekly_service_sales(df):
    """Total service sales for the current week."""
    query = """
        SELECT SUM("Bill Amount") AS weekly_sales
        FROM df
        WHERE strftime('%W', Timestamp) = strftime('%W', CURRENT_DATE)
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()

def weekly_service_count(df):
    """Total number of distinct services (visits) for the current week."""
    query = """
        SELECT COUNT(DISTINCT "Phone Number" || DATE(Timestamp)) AS weekly_service_count
        FROM df
        WHERE strftime('%W', Timestamp) = strftime('%W', CURRENT_DATE)
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()


def monthly_service_sales(df):
    """Total service sales for the current month."""
    query = """
        SELECT SUM("Bill Amount") AS monthly_sales
        FROM df
        WHERE strftime('%m', Timestamp) = strftime('%m', CURRENT_DATE)
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()

def monthly_service_count(df):
    """Total number of distinct services (visits) for the current month."""
    query = """
        SELECT COUNT(DISTINCT "Phone Number" || DATE(Timestamp)) AS monthly_service_count
        FROM df
        WHERE strftime('%m', Timestamp) = strftime('%m', CURRENT_DATE)
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()


def prev_week_service_sales(df):
    """Total service sales for the previous week."""
    query = """
        SELECT SUM("Bill Amount") AS prev_week_sales
        FROM df
        WHERE strftime('%W', Timestamp) = CAST(strftime('%W', CURRENT_DATE) AS INTEGER) - 1
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()

def prev_week_service_count(df):
    """Total number of distinct services (visits) for the previous week."""
    query = """
        SELECT COUNT(DISTINCT "Phone Number" || DATE(Timestamp)) AS prev_week_service_count
        FROM df
        WHERE strftime('%W', Timestamp) = CAST(strftime('%W', CURRENT_DATE) AS INTEGER) - 1
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()


def prev_month_service_sales(df):
    """Total service sales for the previous month."""
    query = """
        SELECT SUM("Bill Amount") AS prev_month_sales
        FROM df
        WHERE strftime('%m', Timestamp) = CAST(strftime('%m', CURRENT_DATE) AS INTEGER) - 1
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()

def prev_month_service_count(df):
    """Total number of distinct services (visits) for the previous month."""
    query = """
        SELECT COUNT(DISTINCT "Phone Number" || DATE(Timestamp)) AS prev_month_service_count
        FROM df
        WHERE strftime('%m', Timestamp) = CAST(strftime('%m', CURRENT_DATE) AS INTEGER) - 1
          AND strftime('%Y', Timestamp) = strftime('%Y', CURRENT_DATE)
    """
    return duckdb.query(query).df()

def total_service_count(df):
    """Total number of services completed overall."""
    query = """
        SELECT COUNT(*) AS total_services
        FROM df
        WHERE "Bill Amount" IS NOT NULL
    """
    return duckdb.query(query).df()

# --- Home Tab: New vs Repeated Clients ---
def new_and_repeated_clients(df):
    """
    Returns count of new clients and repeated clients for today.
    New clients: first-time visits (phone number not seen before today)
    Repeated clients: have previous visits before today
    """
    df['Date_only'] = df['Timestamp'].dt.date
    today = pd.Timestamp.now().date()

    # All records before today
    past_df = df[df['Date_only'] < today]

    # Today's records
    today_df = df[df['Date_only'] == today]

    # New clients: phone numbers not in past records
    new_clients = today_df[~today_df['Phone Number'].isin(past_df['Phone Number'].unique())]

    # Repeated clients: phone numbers exist in past records
    repeated_clients = today_df[today_df['Phone Number'].isin(past_df['Phone Number'].unique())]

    return len(new_clients), len(repeated_clients)



#-----------------------------------------------Tab-2--------------------------------------------------------------------------------------

def preprocess_data(df):
    """Convert Timestamp string to datetime and add useful columns."""
    if df.empty:
        return df

    # Convert string to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d/%m/%Y %H:%M:%S", errors="coerce")

    # Extract Date, Month, Week, Year
    df["Date"] = df["Timestamp"].dt.date
    df["Month"] = df["Timestamp"].dt.month_name()
    df["Week"] = df["Timestamp"].dt.isocalendar().week
    df["Year"] = df["Timestamp"].dt.year

    return df



def cumulative_sales(df):
    """Cumulative sales for current month and YTD."""
    query = """
        SELECT
            SUM(CASE WHEN strftime('%m', Timestamp) = strftime('%m', current_timestamp) THEN "Bill Amount" ELSE 0 END) AS month_sales,
            SUM(CASE WHEN strftime('%Y', Timestamp) = strftime('%Y', current_timestamp) THEN "Bill Amount" ELSE 0 END) AS year_sales
        FROM df
    """
    return duckdb.query(query).df()


def incentive_table(df):
    """Employee incentive (1% of bill)."""
    query = """
        SELECT "Service done by" AS employee,
               SUM("Bill Amount") AS total_sales,
               ROUND(SUM("Bill Amount") * 0.01, 2) AS incentive
        FROM df
        GROUP BY employee
        ORDER BY total_sales DESC
    """
    return duckdb.query(query).df()


def performance_table(df, selected_month=None):
    """Weekly customer count for past 3 months with month filter."""
    if selected_month and selected_month != "All months":
        df = df[df["Month"] == selected_month]

    query = """
        SELECT 
            Year,
            Month,
            Week,
            COUNT(DISTINCT Name) AS customer_visits
        FROM df
        WHERE CAST(Timestamp AS TIMESTAMP) >= (CURRENT_TIMESTAMP - INTERVAL '3 months')
        GROUP BY Year, Month, Week
        ORDER BY Year DESC, Month DESC, Week
    """
    return duckdb.query(query).df()



def peak_hours(df):
    """Find busiest hours."""
    query = """
        SELECT strftime('%H', Timestamp) AS hour, COUNT(*) AS visit_count
        FROM df
        GROUP BY hour
        ORDER BY visit_count DESC
    """
    return duckdb.query(query).df()


def weekday_visit_counts(df):
    """Return visit counts for each weekday (ordered Monday → Sunday)."""
    query = """
        SELECT 
            strftime('%A', Timestamp) AS weekday,
            COUNT(*) AS visit_count,
            CASE 
                WHEN strftime('%w', Timestamp) = '0' THEN 7  -- Sunday as 7
                ELSE CAST(strftime('%w', Timestamp) AS INTEGER)
            END AS weekday_num
        FROM df
        GROUP BY weekday, weekday_num
        ORDER BY weekday_num
    """
    result = duckdb.query(query).df()
    return result[["weekday", "visit_count"]]


def service_count(df, selected_month=None):
    """Service-wise usage count."""
    if selected_month and selected_month != "All months":
        df = df[df["Month"] == selected_month]
    melted = df.melt(
        id_vars=["Name", "Timestamp"],
        value_vars=["Waxing", "Facial", "De-tan", "Pedicure", "Manicure",
                    "Bleaching", "Wash", "Massage", "Threading", "Hair Cut"],
        var_name="Service",
        value_name="Used"
    )
    melted = melted[melted["Used"].astype(str).str.strip() != ""]
    query = """
        SELECT Service, COUNT(*) AS count
        FROM melted
        GROUP BY Service
        ORDER BY count DESC
    """
    return duckdb.query(query).df()


# def top_clients(df):
#     """Top 20 clients by visits."""
#     query = """
#         SELECT Name, COUNT(*) AS visits
#         FROM df
#         GROUP BY Name
#         ORDER BY visits DESC
#         LIMIT 20
#     """
#     return duckdb.query(query).df()


# def top_spenders(df):
#     """Top 10 customers by spending."""
#     query = """
#         SELECT Name, SUM("Bill Amount") AS total_spent
#         FROM df
#         GROUP BY Name
#         ORDER BY total_spent DESC
#         LIMIT 10
#     """
#     return duckdb.query(query).df()


# def top_clients_spend_visits(df):
#     """Top 20 clients by total spending with their visit counts."""
#     query = """
#         SELECT 
#             Name,
#             COUNT(*) AS visits,
#             SUM("Bill Amount") AS total_spent
#         FROM df
#         GROUP BY Name
#         ORDER BY total_spent DESC
#         LIMIT 20
#     """
#     result = duckdb.query(query).df()
#     return result


def top_clients_spend_visits(df):
    """Top 20 clients by total spending with their visit counts (unique by phone number)."""
    query = """
        SELECT 
            "Phone Number" AS phone_number,
            ANY_VALUE(Name) AS name,          -- Pick any one representative name for display
            COUNT(*) AS visits,
            SUM("Bill Amount") AS total_spent
        FROM df
        WHERE "Phone Number" IS NOT NULL
        GROUP BY "Phone Number"
        ORDER BY total_spent DESC
        LIMIT 20
    """
    result = duckdb.query(query).df()
    return result[["phone_number", "name", "visits", "total_spent"]]

import duckdb

def least_clients_spend_visits(df):
    """Bottom 20 clients by total spending with their visit counts (unique by phone number)."""
    query = """
        SELECT 
            "Phone Number" AS phone_number,
            ANY_VALUE(Name) AS name,          -- representative customer name
            COUNT(*) AS visits,
            SUM("Bill Amount") AS total_spent
        FROM df
        WHERE "Phone Number" IS NOT NULL
        GROUP BY "Phone Number"
        HAVING total_spent IS NOT NULL
        ORDER BY total_spent ASC
        LIMIT 20
    """
    result = duckdb.query(query).df()
    return result[["phone_number", "name", "visits", "total_spent"]]


def spend_vs_visits(df):
    """Customer spend vs visits."""
    query = """
        SELECT Name,
               COUNT(*) AS visits,
               SUM("Bill Amount") AS total_spent,
               ROUND(SUM("Bill Amount") / COUNT(*), 2) AS avg_spend_per_visit
        FROM df
        GROUP BY Name
        ORDER BY total_spent DESC
    """
    return duckdb.query(query).df()


# def days_since_last_visit(df):
#     """Days since customer's last visit."""
#     latest = df.groupby("Name")["Timestamp"].max().reset_index()
#     latest["Days Since Last Visit"] = (pd.Timestamp.now() - latest["Timestamp"]).dt.days
#     latest = latest.rename(columns={"Timestamp": "Last Visit Date"})
#     return latest.sort_values(by="Days Since Last Visit", ascending=False)

def days_since_last_visit(df):
    """
    Days since customer's last visit (unique by phone number + date).
    Keeps only the latest bill per day and per customer.
    """
    query = """
        WITH cleaned AS (
            SELECT 
                TRIM(REPLACE(REPLACE(REPLACE(CAST("Phone Number" AS VARCHAR), ' ', ''), '+91', ''), '-', '')) AS phone_clean,
                Name,
                Timestamp
            FROM df
            WHERE "Phone Number" IS NOT NULL
        ),
        ranked_bills AS (
            SELECT 
                phone_clean AS "Phone Number",
                Name AS Customer_Name,
                DATE(Timestamp) AS visit_date,
                Timestamp,
                ROW_NUMBER() OVER (
                    PARTITION BY phone_clean, DATE(Timestamp)
                    ORDER BY Timestamp DESC
                ) AS rn
            FROM cleaned
        ),
        latest_daily_bill AS (
            SELECT 
                "Phone Number",
                Customer_Name,
                visit_date,
                Timestamp AS Last_Bill_Time
            FROM ranked_bills
            WHERE rn = 1
        ),
        latest_visit_per_customer AS (
            SELECT 
                "Phone Number",
                ANY_VALUE(Customer_Name) AS Customer_Name,
                MAX(visit_date) AS Last_Visit_Date
            FROM latest_daily_bill
            GROUP BY "Phone Number"
        )
        SELECT 
            "Phone Number",
            Customer_Name,
            Last_Visit_Date,
            DATE_DIFF('day', Last_Visit_Date, NOW()) AS "Days Since Last Visit"
        FROM latest_visit_per_customer
        ORDER BY "Days Since Last Visit" DESC
    """
    result = duckdb.query(query).df()
    return result

def employee_service_ranking(df):
    """Employee by number of services."""
    query = """
        SELECT "Service done by" AS employee, COUNT(*) AS service_count
        FROM df
        GROUP BY employee
        ORDER BY service_count DESC
    """
    return duckdb.query(query).df()


def employee_revenue_ranking(df):
    """Employee by total revenue."""
    query = """
        SELECT "Service done by" AS employee, SUM("Bill Amount") AS total_revenue
        FROM df
        GROUP BY employee
        ORDER BY total_revenue DESC
    """
    return duckdb.query(query).df()


def unique_service_counts(df, selected_month=None):
    """Unique service types."""
    return service_count(df, selected_month)

#------------------------------------------Tab-2--------------------------------------------------------------------------------------

def preprocess_data(df):
    """Convert timestamp and add useful columns."""
    if df.empty:
        return df

    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d/%m/%Y %H:%M:%S", errors="coerce")

    # Extract Date, Month, Week, and Year
    df["Date"] = df["Timestamp"].dt.date
    df["Month"] = df["Timestamp"].dt.month_name()
    df["Week"] = df["Timestamp"].dt.isocalendar().week
    df["Year"] = df["Timestamp"].dt.year

    return df


def cumulative_sales(df):
    """Cumulative sales for current month and YTD."""
    query = """
        SELECT
            SUM(CASE WHEN strftime(CAST(Timestamp AS TIMESTAMP), '%m') = strftime(current_timestamp, '%m') THEN "Bill Amount" ELSE 0 END) AS month_sales,
            SUM(CASE WHEN strftime(CAST(Timestamp AS TIMESTAMP), '%Y') = strftime(current_timestamp, '%Y') THEN "Bill Amount" ELSE 0 END) AS year_sales
        FROM df
    """
    return duckdb.query(query).df()



def incentive_table(df):
    """Employee incentive (1% of bill)."""
    query = """
        SELECT "Service done by" AS employee,
               SUM("Bill Amount") AS total_sales,
               ROUND(SUM("Bill Amount") * 0.01, 2) AS incentive
        FROM df
        GROUP BY employee
        ORDER BY total_sales DESC
    """
    return duckdb.query(query).df()

def performance_table(df, selected_month=None):
    """Weekly customer count for past 3 months with month filter."""
    if selected_month and selected_month != "All months":
        df = df[df["Month"] == selected_month]

    query = """
        SELECT 
            Year, 
            Month, 
            Week, 
            COUNT(DISTINCT Name) AS customer_visits
        FROM df
        WHERE CAST(Timestamp AS TIMESTAMP WITH TIME ZONE) >= (current_timestamp - INTERVAL '3 months')
        GROUP BY Year, Month, Week
        ORDER BY Year DESC, Month DESC, Week
    """
    return duckdb.query(query).df()




def peak_hours(df):
    """Find busiest hours."""
    query = """
        SELECT strftime('%H', Timestamp) AS hour, COUNT(*) AS visit_count
        FROM df
        GROUP BY hour
        ORDER BY visit_count DESC
    """
    return duckdb.query(query).df()


def weekday_visits(df):
    """Visits per weekday."""
    query = """
        SELECT strftime('%A', Timestamp) AS weekday, COUNT(*) AS visits
        FROM df
        GROUP BY weekday
        ORDER BY visits DESC
    """
    return duckdb.query(query).df()


def service_count(df, selected_month=None):
    """Service-wise usage count."""
    if selected_month and selected_month != "All months":
        df = df[df["Month"] == selected_month]
    melted = df.melt(
        id_vars=["Name", "Timestamp"],
        value_vars=["Waxing", "Facial", "De-tan", "Pedicure", "Manicure",
                    "Bleaching", "Wash", "Massage", "Threading", "Hair Cut"],
        var_name="Service",
        value_name="Used"
    )
    melted = melted[melted["Used"].astype(str).str.strip() != ""]
    query = """
        SELECT Service, COUNT(*) AS count
        FROM melted
        GROUP BY Service
        ORDER BY count DESC
    """
    return duckdb.query(query).df()


def top_clients(df):
    """Top 20 clients by visits."""
    query = """
        SELECT Name, COUNT(*) AS visits
        FROM df
        GROUP BY Name
        ORDER BY visits DESC
        LIMIT 20
    """
    return duckdb.query(query).df()


def top_spenders(df):
    """Top 10 customers by spending."""
    query = """
        SELECT Name, SUM("Bill Amount") AS total_spent
        FROM df
        GROUP BY Name
        ORDER BY total_spent DESC
        LIMIT 10
    """
    return duckdb.query(query).df()


def spend_vs_visits(df):
    """Customer spend vs visits."""
    query = """
        SELECT Name,
               COUNT(*) AS visits,
               SUM("Bill Amount") AS total_spent,
               ROUND(SUM("Bill Amount") / COUNT(*), 2) AS avg_spend_per_visit
        FROM df
        GROUP BY Name
        ORDER BY total_spent DESC
    """
    return duckdb.query(query).df()


def days_since_last_visit(df):
    """Days since customer's last visit."""
    latest = df.groupby("Name")["Timestamp"].max().reset_index()
    latest["Days Since Last Visit"] = (pd.Timestamp.now() - latest["Timestamp"]).dt.days
    latest = latest.rename(columns={"Timestamp": "Last Visit Date"})
    return latest.sort_values(by="Days Since Last Visit", ascending=False)


def employee_service_ranking(df):
    """Employee by number of services."""
    query = """
        SELECT "Service done by" AS employee, COUNT(*) AS service_count
        FROM df
        GROUP BY employee
        ORDER BY service_count DESC
    """
    return duckdb.query(query).df()


def employee_revenue_ranking(df):
    """Employee by total revenue."""
    query = """
        SELECT "Service done by" AS employee, SUM("Bill Amount") AS total_revenue
        FROM df
        GROUP BY employee
        ORDER BY total_revenue DESC
    """
    return duckdb.query(query).df()


def unique_service_counts(df, selected_month=None):
    """Unique service types."""
    return service_count(df, selected_month)

#------------------------------------------Tab-3----------------------------------------------------------------
def get_employee_sales(df: pd.DataFrame):
    """Employee ranking by number of products sold"""
    query = """
        SELECT "Sold by" AS employee, COUNT(*) AS total_products_sold
        FROM df
        GROUP BY employee
        ORDER BY total_products_sold DESC
    """
    return duckdb.query(query).to_df()


def get_employee_revenue(df: pd.DataFrame):
    """Employee ranking by total bill amount"""
    query = """
        SELECT "Sold by" AS employee, SUM("Bill Amount") AS total_revenue
        FROM df
        GROUP BY employee
        ORDER BY total_revenue DESC
    """
    return duckdb.query(query).to_df()


def get_revenue_summary(df: pd.DataFrame):
    """Today's, weekly, and monthly revenue + count"""
    query = """
        SELECT
            SUM("Bill Amount") AS total_revenue,
            COUNT(*) AS total_sales
        FROM df
    """
    return duckdb.query(query).to_df().iloc[0]


def get_top_products(df: pd.DataFrame):
    """Product frequency count"""
    query = """
        SELECT "Product Name" AS product, COUNT(*) AS sold_count
        FROM df
        GROUP BY product
        ORDER BY sold_count DESC
    """
    return duckdb.query(query).to_df()


def get_sales_by_day(df: pd.DataFrame):
    """Total sales and orders grouped by weekday"""
    query = """
        SELECT 
            strftime('%A', strptime("Date", '%d-%b-%Y')) AS day_of_week,
            SUM("Bill Amount") AS total_sold,
            COUNT(*) AS total_orders
        FROM df
        GROUP BY day_of_week
        ORDER BY min(strptime("Date", '%d-%b-%Y'))
    """
    return duckdb.query(query).to_df()


def get_incentive_by_employee(df: pd.DataFrame):
    """Calculate yearly incentive (1% of total bill amount) per employee."""

    # Get current year
    current_year = datetime.now().year

    # Convert date column to proper datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Filter only current year's records
    df_year = df[df["Date"].dt.year == current_year]

    query = """
        SELECT 
            "Sold by" AS employee,
            SUM("Bill Amount") * 0.01 AS incentive_amount
        FROM df_year
        GROUP BY employee
        ORDER BY incentive_amount DESC
    """

    return duckdb.query(query).to_df()

# =========================
# 📦 PRODUCT SALES QUERIES
# =========================

def total_product_sales(df):
    """Total revenue from all product sales."""
    query = """
        SELECT SUM("Bill Amount") AS total_product_revenue
        FROM df
    """
    return duckdb.query(query).df()


def total_products_sold(df):
    """Total number of products sold."""
    query = """
        SELECT COUNT(*) AS total_products_sold
        FROM df
    """
    return duckdb.query(query).df()


def products_sold_today(df):
    """Products sold today."""
    query = """
        SELECT COUNT(*) AS products_sold_today
        FROM df
        WHERE DATE(Timestamp) = DATE(CURRENT_DATE)
    """
    return duckdb.query(query).df()


def products_sold_last_week(df):
    """Products sold in the last 7 days."""
    query = """
        SELECT COUNT(*) AS products_sold_last_week
        FROM df
        WHERE DATE(Timestamp) >= DATE(CURRENT_DATE) - INTERVAL 7 DAY
    """
    return duckdb.query(query).df()


def products_sold_last_month(df):
    """Products sold in the last 30 days."""
    query = """
        SELECT COUNT(*) AS products_sold_last_month
        FROM df
        WHERE DATE(Timestamp) >= DATE(CURRENT_DATE) - INTERVAL 30 DAY
    """
    return duckdb.query(query).df()