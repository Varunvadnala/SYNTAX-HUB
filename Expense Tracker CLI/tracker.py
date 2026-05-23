from database import get_connection
from transaction import Transaction


class ExpenseTracker:

    def add_transaction(self, transaction):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transactions
        (date, type, category, amount, description)
        VALUES (?, ?, ?, ?, ?)
        """, (
            transaction.date,
            transaction.trans_type,
            transaction.category,
            transaction.amount,
            transaction.description
        ))

        conn.commit()
        conn.close()

        print("Transaction added successfully.")

    # ======================================
    # View Transactions
    # ======================================
    def view_transactions(self, category=None):
        conn = get_connection()
        cursor = conn.cursor()

        if category:
            cursor.execute("""
            SELECT * FROM transactions
            WHERE category=?
            """, (category,))
        else:
            cursor.execute("""
            SELECT * FROM transactions
            """)

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            print("No transactions found.")
            return

        for row in rows:
            print(row)

    # ======================================
    # Delete Transaction
    # ======================================
    def delete_transaction(self, transaction_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM transactions
        WHERE id=?
        """, (transaction_id,))

        conn.commit()
        conn.close()

        print("Transaction deleted successfully.")

    # ======================================
    # Update Transaction
    # ======================================
    def update_transaction(
        self,
        transaction_id,
        category=None,
        amount=None,
        description=None
    ):
        conn = get_connection()
        cursor = conn.cursor()

        if category:
            cursor.execute("""
            UPDATE transactions
            SET category=?
            WHERE id=?
            """, (category, transaction_id))

        if amount is not None:
            cursor.execute("""
            UPDATE transactions
            SET amount=?
            WHERE id=?
            """, (amount, transaction_id))

        if description:
            cursor.execute("""
            UPDATE transactions
            SET description=?
            WHERE id=?
            """, (description, transaction_id))

        conn.commit()
        conn.close()

        print("Transaction updated successfully.")