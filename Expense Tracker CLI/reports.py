import pandas as pd
import matplotlib.pyplot as plt
import os
from database import get_connection

EXPORT_FOLDER = "exports"
CHART_FOLDER = "charts"

os.makedirs(EXPORT_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)


class Reports:

    # ======================================
    # Monthly Summary
    # ======================================
    def monthly_summary(self, month):

        conn = get_connection()

        query = """
        SELECT * FROM transactions
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        if df.empty:
            print("No data found.")
            return

        df["date"] = pd.to_datetime(df["date"])

        filtered = df[
            df["date"].dt.strftime("%Y-%m") == month
        ]

        if filtered.empty:
            print("No transactions for this month.")
            return

        income = filtered[
            filtered["type"] == "income"
        ]["amount"].sum()

        expense = filtered[
            filtered["type"] == "expense"
        ]["amount"].sum()

        balance = income - expense

        print(f"\nSummary for {month}")
        print("-" * 30)
        print(f"Income : ₹{income}")
        print(f"Expense: ₹{expense}")
        print(f"Balance: ₹{balance}")

    # ======================================
    # Export Excel
    # ======================================
    def export_excel(self):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM transactions",
            conn
        )

        conn.close()

        path = os.path.join(
            EXPORT_FOLDER,
            "expenses.xlsx"
        )

        df.to_excel(path, index=False)

        print(f"Excel exported to: {path}")

    # ======================================
    # Generate Chart
    # ======================================
    def generate_chart(self, month):

        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM transactions",
            conn
        )

        conn.close()

        if df.empty:
            print("No data found.")
            return

        df["date"] = pd.to_datetime(df["date"])

        filtered = df[
            (df["date"].dt.strftime("%Y-%m") == month)
            & (df["type"] == "expense")
        ]

        category_summary = (
            filtered.groupby("category")["amount"]
            .sum()
        )

        plt.figure(figsize=(8, 5))

        category_summary.plot(kind="bar")

        plt.title(f"Expenses by Category ({month})")

        chart_path = os.path.join(
            CHART_FOLDER,
            f"{month}_chart.png"
        )

        plt.tight_layout()

        plt.savefig(chart_path)

        print(f"Chart saved to: {chart_path}")