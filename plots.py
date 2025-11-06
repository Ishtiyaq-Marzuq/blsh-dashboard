import plotly.express as px
import pandas as pd
import streamlit as st

# plots.py (Home tab - optional)
import streamlit as st

def display_home_metrics(total_sales, customer_count):
    col1, col2 = st.columns(2)
    col1.metric("💰 Today's Sales", f"₹{total_sales:,.2f}")
    col2.metric("👥 Customers Visited Today", f"{customer_count}")

def display_home_metrics(total_sales, customer_count, new_clients, repeated_clients):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Today's Sales", f"₹{total_sales:,.2f}")
    col2.metric("👥 Customers Visited Today", f"{customer_count}")
    col3.metric("🆕 New Clients", f"{new_clients}")
    col4.metric("🔁 Repeated Clients", f"{repeated_clients}")

def plot_annual_incentives(df):
    fig = px.bar(df, x="employee", y="total_incentive", color="year",
                 barmode="group", text="total_incentive",
                 title="Annual Incentives (Service + Product)")
    fig.update_layout(xaxis_title="Employee", yaxis_title="Incentive (₹)")
    return fig



#-----------------------------------------Tab-2----------------------------------------------------------------

import plotly.express as px
import streamlit as st

def plot_peak_hours(df):
    fig = px.bar(df, x="hour", y="visit_count",  text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_weekday_visit_counts(df):
    """Plot bar chart of visits per weekday (Mon–Sun)."""
    df["is_weekend"] = df["weekday"].isin(["Saturday", "Sunday"])

    fig = px.bar(
        df,
        x="weekday",
        y="visit_count",
        color="is_weekend",
        text_auto=True,
        title="Customer Visits by Weekday",
        color_discrete_map={True: "#ff7f0e", False: "#1f77b4"}
    )

    fig.update_layout(
        xaxis_title="Weekday",
        yaxis_title="Number of Visits",
        showlegend=False,
        title_x=0.5,
        bargap=0.2
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_service_counts(df):
    fig = px.bar(df, x="Service", y="count",  text_auto=True)
    st.plotly_chart(fig, use_container_width=True)


def plot_spend_vs_visits(df):
    fig = px.scatter(
        df, x="visits", y="total_spent", size="avg_spend_per_visit",
        hover_name="Name", 
    )
    st.plotly_chart(fig, use_container_width=True)


# def plot_employee_performance(df1, df2):
#     col1, col2 = st.columns(2)
#     with col1:
#         fig1 = px.bar(df1, x="employee", y="service_count", text_auto=True)
#         st.plotly_chart(fig1, use_container_width=True)
#     with col2:
#         fig2 = px.bar(df2, x="employee", y="total_revenue",  text_auto=True)
#         st.plotly_chart(fig2, use_container_width=True)

import plotly.express as px
import streamlit as st

def plot_employee_performance(df1, df2):
    """Show employee rankings: by service count and revenue side-by-side."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Services Rendered by employee")
        fig1 = px.bar(df1, x="employee", y="service_count", text_auto=True,
                      title=None)
        fig1.update_layout(xaxis_title=None, yaxis_title="Services", title_x=0.5)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### By Revenue Generated employee")
        fig2 = px.bar(df2, x="employee", y="total_revenue", text_auto=True,
                      title=None)
        fig2.update_layout(xaxis_title=None, yaxis_title="Revenue (₹)", title_x=0.5)
        st.plotly_chart(fig2, use_container_width=True)

#------------------------------------------Tab-3----------------------------------------------------------------
def plot_sales_by_day(df: pd.DataFrame):
    """Line chart: total sales by weekday"""
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=weekday_order, ordered=True)
    df = df.sort_values("day_of_week")

    fig = px.line(
        df,
        x="day_of_week",
        y="total_sold",
        markers=True,
        title="🗓️ Sales Trend by Day of Week",
        text="total_sold"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Total Sales (₹)",
        title_x=0.5,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_top_products(df: pd.DataFrame):
    """Bar chart: most frequently sold products"""
    fig = px.bar(
        df.head(10),
        x="product",
        y="sold_count",
        title="🏆 Top 10 Best-Selling Products",
        text_auto=True
    )
    fig.update_layout(
        xaxis_title="Product Name",
        yaxis_title="Units Sold",
        title_x=0.5,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_employee_revenue(df: pd.DataFrame):
    """Bar chart: employee-wise total revenue"""
    fig = px.bar(
        df,
        x="employee",
        y="total_revenue",
        title="💼 Employee Revenue Performance",
        text_auto=True
    )
    fig.update_layout(
        xaxis_title="Employee",
        yaxis_title="Total Revenue (₹)",
        title_x=0.5,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_employee_sales(df: pd.DataFrame):
    """Bar chart: employee-wise total number of products sold"""
    fig = px.bar(
        df,
        x="employee",
        y="total_products_sold",
        title="👥 Employee Product Sales Count",
        text_auto=True,
        color="total_products_sold",
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        xaxis_title="Employee",
        yaxis_title="Total Products Sold",
        title_x=0.5,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st

def plot_incentive_by_employee(df):
    """Display incentives earned by each employee as a sortable table."""
    
    st.markdown("### 💼 Employee Incentives Leaderboard (Current Year)")
    
    # Format the incentive column for better readability
    df_display = df.copy()
    df_display["incentive_amount"] = df_display["incentive_amount"].map("₹{:,.2f}".format)

    # Display the table
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

#--------------------------------------------------------------------------------------------------------------------------------------------------