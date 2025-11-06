import streamlit as st
from utils.sheets_connector import get_sheet_data
import query
import plots

# ---------------------------------------------------
# 🧭 PAGE CONFIG (must be first Streamlit command)
# ---------------------------------------------------
st.set_page_config(page_title="BLSH Dashboard", layout="wide")

import streamlit as st
from utils.sheets_connector import get_sheet_data
import query
import plots

# --- Tabs ---
tabs = st.tabs(["🏠 Home", "🛠 Service Data", "📦 Product Data"])

# ========================= Home Tab =========================

# -------------------------------
# ✅ HOME DASHBOARD SECTION
# -------------------------------
with tabs[0]:
    st.header("🏠 Home Dashboard")

    # --- Load Data ---
    df = get_sheet_data("Client Data")
    df = query.preprocess_data(df)

    if df.empty:
        st.warning("No data found in Client Data sheet.")
        st.stop()

    # --- Metrics Queries ---
    sales_today_df = query.today_sales(df)
    customers_today_df = query.today_customer_count(df)
    new_clients, repeated_clients = query.new_and_repeated_clients(df)

    weekly_sales_df = query.weekly_service_sales(df)
    weekly_count_df = query.weekly_service_count(df)

    monthly_sales_df = query.monthly_service_sales(df)
    monthly_count_df = query.monthly_service_count(df)

    prev_week_sales_df = query.prev_week_service_sales(df)
    prev_week_count_df = query.prev_week_service_count(df)

    prev_month_sales_df = query.prev_month_service_sales(df)
    prev_month_count_df = query.prev_month_service_count(df)
    total_services_df = query.total_service_count(df)
    revenue_summary = query.get_revenue_summary(df)

    # --- Extract Values Safely ---
    def safe_value(df, col):
        return df[col][0] if col in df.columns and not df.empty else 0

    sales_today = safe_value(sales_today_df, "total_sales_today")
    customers_today = safe_value(customers_today_df, "customers_today")
    weekly_sales = safe_value(weekly_sales_df, "weekly_sales")
    weekly_count = safe_value(weekly_count_df, "weekly_service_count")
    monthly_sales = safe_value(monthly_sales_df, "monthly_sales")
    monthly_count = safe_value(monthly_count_df, "monthly_service_count")
    prev_week_sales = safe_value(prev_week_sales_df, "prev_week_sales")
    prev_week_count = safe_value(prev_week_count_df, "prev_week_service_count")
    prev_month_sales = safe_value(prev_month_sales_df, "prev_month_sales")
    prev_month_count = safe_value(prev_month_count_df, "prev_month_service_count")
    total_services = safe_value(total_services_df, "total_services")

    # --- KPI Card Function (Neutral Design) ---
    def kpi_box(title, value):
        st.markdown(
            f"""
            <div style="
                background-color: rgba(240, 240, 240, 0.05);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(128,128,128,0.2);
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                transition: all 0.3s ease;
            ">
                <div style="font-size: 13px; color: rgba(130,130,130,0.9); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
                    {title}
                </div>
                <div style="font-size: 22px; font-weight: 600; color: rgba(230,230,230,0.95);">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Performance Indicators - Service ")

    # --- Row 1: Today's KPIs ---
    col1, col2, col3, col4,col5 = st.columns(5)
    with col1:
        kpi_box("Today's Sales", f"₹{sales_today:,.2f}")
    with col2:
        kpi_box("Customers Today", f"{int(customers_today)}")
    with col3:
        kpi_box("New Clients", f"{int(new_clients)}")
    with col4:
        kpi_box("Repeated Clients", f"{int(repeated_clients)}")
    with col5:
        kpi_box("Total Services", f"{int(total_services)}")  # 👈 NEW KPI

    st.markdown("---")

    # --- Row 2: Current Week/Month KPIs ---
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        kpi_box("Weekly Sales", f"₹{weekly_sales:,.2f}")
    with col6:
        kpi_box("Weekly Visits", f"{int(weekly_count)}")
    with col7:
        kpi_box("Monthly Sales", f"₹{monthly_sales:,.2f}")
    with col8:
        kpi_box("Monthly Visits", f"{int(monthly_count)}")

    st.markdown("---")

    # --- Row 3: Previous Week/Month KPIs ---
    col9, col10, col11, col12 = st.columns(4)
    with col9:
        kpi_box("Prev Week Sales", f"₹{prev_week_sales:,.2f}")
    with col10:
        kpi_box("Prev Week Visits", f"{int(prev_week_count)}")
    with col11:
        kpi_box("Prev Month Sales", f"₹{prev_month_sales:,.2f}")
    with col12:
        kpi_box("Prev Month Visits", f"{int(prev_month_count)}")


    # =========================
    # 📦 PRODUCT SALES KPIs
    # =========================
    st.markdown("### Product Sales Overview")

    # --- Load Product Data ---
    product_df = get_sheet_data("Product Sale")
    product_df = query.preprocess_data(product_df)

    if not product_df.empty:
        total_prod_sales_df = query.total_product_sales(product_df)
        total_products_df = query.total_products_sold(product_df)
        prod_today_df = query.products_sold_today(product_df)
        prod_week_df = query.products_sold_last_week(product_df)
        prod_month_df = query.products_sold_last_month(product_df)

        total_product_sales = safe_value(total_prod_sales_df, "total_product_revenue")
        total_products_sold = safe_value(total_products_df, "total_products_sold")
        products_today = safe_value(prod_today_df, "products_sold_today")
        products_week = safe_value(prod_week_df, "products_sold_last_week")
        products_month = safe_value(prod_month_df, "products_sold_last_month")

        # --- KPI Boxes (Neutral Design) ---
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            kpi_box("Total Product Revenue", f"₹{total_product_sales:,.2f}")
        with col2:
            kpi_box("Total Products Sold", f"{int(total_products_sold)}")
        with col3:
            kpi_box("Products Sold Today", f"{int(products_today)}")
        with col4:
            kpi_box("Products Sold Last Week", f"{int(products_week)}")
        with col5:
            kpi_box("Products Sold Last Month", f"{int(products_month)}")

    else:
        st.warning("No data found in Product Sale sheet.")


# ---------------------------------------------------
# 🛠 SERVICE DATA TAB
# ---------------------------------------------------
with tabs[1]:
    st.header("💇‍♀️ Service Data Dashboard")

    # === Load Live Data ===
    df = get_sheet_data("Client Data")
    df = query.preprocess_data(df)

    if df.empty:
        st.warning("No data found in Client Data sheet.")
        st.stop()

    # === 1️⃣ Cumulative Sales ===
    sales = query.cumulative_sales(df)
    col1, col2 = st.columns(2)
    col1.metric("📅 Current Month Sales", f"₹{sales['month_sales'][0]:,.2f}")
    col2.metric("📆 Year-to-Date Sales", f"₹{sales['year_sales'][0]:,.2f}")

    st.divider()

    # === 2️⃣ Incentive Table ===
    st.subheader("💸 Incentive Table (1% of Total Bill)")
    incentive_df = query.incentive_table(df).reset_index(drop=True)
    incentive_df.index = incentive_df.index + 1  # Start from 1
    st.dataframe(incentive_df, use_container_width=True, height=250)

    # === 3️⃣ Performance Table (Weekwise) ===
    st.subheader("📊 Weekly Performance (Past 3 Months)")
    month_options = ["All months"] + sorted(df["Month"].unique().tolist())
    selected_month = st.selectbox("Select Month", month_options)
    performance_df = query.performance_table(df, selected_month).reset_index(drop=True)
    performance_df.index = performance_df.index + 1  # Start from 1
    st.dataframe(performance_df, use_container_width=True, height=250)
    
    # === 4️⃣ Peak Hours ===
    st.subheader("⏰ Peak Customer Arrival Times")
    plots.plot_peak_hours(query.peak_hours(df))

    # === 5️⃣ Weekday Visits ===
    st.subheader("📅 Customer Visits by Weekday")
    weekday_visits_df = query.weekday_visit_counts(df)
    plots.plot_weekday_visit_counts(weekday_visits_df)

    # === 6️⃣ Service Count Visualization ===
    st.subheader("💇‍♀️ Service Count by Type")
    selected_month_service = st.selectbox("Select Month for Service Count", month_options, key="service_month")
    plots.plot_service_counts(query.service_count(df, selected_month_service))

    # # === 7️⃣ Top 20 Clients ===
    # st.subheader("🏅 Top 20 Clients by Visits")
    # top_clients_df = query.top_clients(df).reset_index(drop=True)
    # top_clients_df.index = top_clients_df.index + 1  # Start index from 1
    # st.dataframe(top_clients_df, use_container_width=True, height=250)



    # # === 9️⃣ Top 20 Clients: Spending and Visits ===
    # st.subheader("💎 Top 20 Clients: Spending and Visits")

    # top_clients_df = query.top_clients_spend_visits(df).reset_index(drop=True)
    # top_clients_df.index = top_clients_df.index + 1  # Start index from 1

    # st.dataframe(top_clients_df, use_container_width=True, height=400)

    # === 9️⃣ Top 20 Clients (By Spend & Visits, Unique by Phone) ===
    st.subheader("💎 Top 20 Clients: Spending and Visits (Unique by Phone)")

    top_clients_df = query.top_clients_spend_visits(df).reset_index(drop=True)
    top_clients_df.index = top_clients_df.index + 1  # Start index from 1

    st.dataframe(top_clients_df, use_container_width=True, height=400)

    # === 🔟 Least 20 Clients (By Spend & Visits, Unique by Phone) ===
    st.subheader("📉 Least 20 Clients: Spending and Visits (Unique by Phone)")

    least_clients_df = query.least_clients_spend_visits(df).reset_index(drop=True)
    least_clients_df.index = least_clients_df.index + 1  # Start index from 1

    st.dataframe(least_clients_df, use_container_width=True, height=400)

    # # === 10️⃣ Least 20 Clients: Spending and Visits ===
    # st.subheader("📉 Least 20 Clients: Spending and Visits")

    # least_clients_df = query.least_clients_spend_visits(df).reset_index(drop=True)
    # least_clients_df.index = least_clients_df.index + 1  # Start index from 1

    # st.dataframe(least_clients_df, use_container_width=True, height=400)

    # # === 8️⃣ Top 10 Spenders ===
    # st.subheader("💰 Top 10 Customers by Spend")
    # top_spenders_df = query.top_spenders(df).reset_index(drop=True)
    # top_spenders_df.index = top_spenders_df.index + 1  # Start index from 1
    # st.dataframe(top_spenders_df, use_container_width=True, height=250)

    # === 9️⃣ Spend vs Visits ===
    st.subheader("📈 Customer Spend vs Visit Ratio")
    plots.plot_spend_vs_visits(query.spend_vs_visits(df))

    # # === 🔟 Days Since Last Visit ===
    # st.subheader("📆 Days Since Last Visit")

    # days_since_df = query.days_since_last_visit(df).reset_index(drop=True)
    # days_since_df.index = days_since_df.index + 1  # Start index from 1

    # st.dataframe(days_since_df, use_container_width=True, height=250)
    # === 🔟 Days Since Last Visit ===
    st.subheader("📆 Days Since Last Visit (Latest Bill Per Day, Cleaned Phones)")

    days_df = query.days_since_last_visit(df).reset_index(drop=True)
    days_df.index = days_df.index + 1
    st.dataframe(days_df, use_container_width=True, height=400)

    # === 11️⃣ Employee Rankings ===
    #st.subheader("Employee Rankings")
    plots.plot_employee_performance(query.employee_service_ranking(df), query.employee_revenue_ranking(df))

    # # === 11️⃣ Employee Rankings by Services ===
    # st.subheader("Services Rendered by employees")
    # plots.plot_employee_service(query.employee_service_ranking(df))

    # # === 12️⃣ Employee Rankings by Revenue ===
    # st.subheader("Revenue Generated by employees")
    # plots.plot_employee_revenue(query.employee_revenue_ranking(df))

    # === 12️⃣ Unique Service Counts ===
    st.subheader("✨ Unique Service Counts")
    selected_month_unique = st.selectbox("Select Month for Unique Service", month_options, key="unique_month")

    unique_service_df = query.unique_service_counts(df, selected_month_unique).reset_index(drop=True)
    unique_service_df.index = unique_service_df.index + 1  # Start index from 1

    st.dataframe(unique_service_df, use_container_width=True, height=250)


# ---------------------------------------------------
# 📦 PRODUCT DATA TAB
# ---------------------------------------------------
with tabs[2]:
    st.header("📦 Product Sales Insights")

    df = get_sheet_data("Product Sale")
    

    if df.empty:
        st.warning("No data found in Product Sale sheet.")
        st.stop()

    #st.success(f" Live data loaded: {len(df)} records")

    # --- Queries ---
    emp_sales = query.get_employee_sales(df)
    emp_rev = query.get_employee_revenue(df)
    top_products = query.get_top_products(df)
    sales_by_day = query.get_sales_by_day(df)
    revenue_summary = query.get_revenue_summary(df)
    incentives = query.get_incentive_by_employee(df)

    # --- KPI Boxes ---
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"₹{revenue_summary['total_revenue']:.2f}")
    col2.metric("Total Sales", f"{int(revenue_summary['total_sales'])}")

    plots.plot_incentive_by_employee(incentives)

    # --- Charts ---
    plots.plot_employee_sales(emp_sales)
    plots.plot_employee_revenue(emp_rev)
    plots.plot_top_products(top_products)
    plots.plot_sales_by_day(sales_by_day)
