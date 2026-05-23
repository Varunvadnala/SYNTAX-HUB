from datetime import datetime

from database import create_table
from transaction import Transaction
from tracker import ExpenseTracker
from reports import Reports


tracker = ExpenseTracker()
reports = Reports()


# ==========================================
# Add Transaction
# ==========================================
def add_transaction_menu():

    date = input("Enter date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    trans_type = input("Enter type (income/expense): ")

    if trans_type not in ["income", "expense"]:
        print("Invalid type.")
        return

    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be positive.")
            return

    except ValueError:
        print("Invalid amount.")
        return

    description = input("Enter description: ")

    transaction = Transaction(
        date,
        trans_type,
        category,
        amount,
        description
    )

    tracker.add_transaction(transaction)


# ==========================================
# View Transactions
# ==========================================
def view_transactions_menu():

    category = input(
        "Enter category filter (leave empty for all): "
    )

    if category.strip() == "":
        category = None

    tracker.view_transactions(category)


# ==========================================
# Delete Transaction
# ==========================================
def delete_transaction_menu():

    try:
        transaction_id = int(
            input("Enter transaction ID: ")
        )

        tracker.delete_transaction(transaction_id)

    except ValueError:
        print("Invalid ID.")


# ==========================================
# Update Transaction
# ==========================================
def update_transaction_menu():

    try:
        transaction_id = int(
            input("Enter transaction ID: ")
        )

    except ValueError:
        print("Invalid ID.")
        return

    category = input(
        "Enter new category (leave blank to skip): "
    )

    amount_input = input(
        "Enter new amount (leave blank to skip): "
    )

    description = input(
        "Enter new description (leave blank to skip): "
    )

    amount = None

    if amount_input.strip() != "":
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid amount.")
            return

    if category.strip() == "":
        category = None

    if description.strip() == "":
        description = None

    tracker.update_transaction(
        transaction_id,
        category,
        amount,
        description
    )


# ==========================================
# Monthly Summary
# ==========================================
def monthly_summary_menu():

    month = input("Enter month (YYYY-MM): ")

    reports.monthly_summary(month)


# ==========================================
# Export Excel
# ==========================================
def export_excel_menu():

    reports.export_excel()


# ==========================================
# Generate Chart
# ==========================================
def generate_chart_menu():

    month = input("Enter month (YYYY-MM): ")

    reports.generate_chart(month)


# ==========================================
# Main Menu
# ==========================================
def main():

    create_table()

    while True:

        print("\n========== Expense Tracker ==========")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Monthly Summary")
        print("6. Export Excel")
        print("7. Generate Chart")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        # ==================================
        # ADD
        # ==================================
        if choice == "1":

            add_transaction_menu()

        # ==================================
        # VIEW
        # ==================================
        elif choice == "2":

            view_transactions_menu()

        # ==================================
        # UPDATE
        # ==================================
        elif choice == "3":

            update_transaction_menu()

        # ==================================
        # DELETE
        # ==================================
        elif choice == "4":

            delete_transaction_menu()

        # ==================================
        # SUMMARY
        # ==================================
        elif choice == "5":

            monthly_summary_menu()

        # ==================================
        # EXPORT
        # ==================================
        elif choice == "6":

            export_excel_menu()

        # ==================================
        # CHART
        # ==================================
        elif choice == "7":

            generate_chart_menu()

        # ==================================
        # EXIT
        # ==================================
        elif choice == "8":

            print("Exiting application.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()