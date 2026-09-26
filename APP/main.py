import sqlite3
def create_connection():
     connection = sqlite3.connect("finance_tracker.db")
     return connection
def create_table():
     connection = create_connection()
     cursor = connection.cursor()
     cursor.execute("""
         CREATE TABLE IF NOT EXISTS transactions (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         description TEXT NOT NULL,
         amount REAL NOT NULL,
         type TEXT NOT NULL,
         category TEXT
         )
     """)
     connection.commit()
     connection.close()
def insert_transacion(description, amount, transaction_type, category):
     connection = create_connection()
     cursor = connection.cursor()
     cursor.execute("""
        INSERT INTO transactions (description, amount, type, category)
        VALUES (?, ?, ?, ?)
    """, (description, amount, transaction_type, category))

     connection.commit()
     connection.close()
def get_sqlite_transaction():
     connection = create_connection()
     cursor = connection.cursor()

     cursor.execute("""
        SELECT id, description, amount, type, category
        FROM transactions
    """)
     rows = cursor.fetchall()
     connection.close()
     return rows
def add_transaction():
            description = input("Description: ")
            while True:
                   try:
                          amount = float(input("How much you want to add: "))
                          if amount <= 0:
                                 print("Amount must be greater than 0.")
                          else:
                                break
                   except ValueError:
                          print("Please enter a valid number.")

            while True:
                  transaction_type = input("Expenses or Income?: ").strip().lower()
                  if transaction_type == "income" or transaction_type == "expenses":
                     break
                  else:
                      print("Please enter Income or Expenses.")
            category = input("What category is this?: ")
            transaction = {
                   "type": transaction_type,
                   "amount": amount,
                   "category": category,
                   "description": description
            }
            insert_transacion(description, amount, transaction_type, category)
            print("Transaction Added Sucessfully")
def view_transaction():
     print("--- View Transaction ---")
     db_transaction = get_sqlite_transaction()
     if not db_transaction:
          print("No Transaction Found.")
          return
     for transaction in db_transaction:
          transaction_id, description, amount, transaction_type, category = transaction
          print(
               f"{transaction_id}. {description} | "
               f"{transaction_type.title()} | "
               f"₱{amount:,.2f} | "
               f"{category}"
          )
def financial_summary():
    print("Your Financial Summary")
    db_transactions = get_sqlite_transaction()
    total_income = 0
    total_expenses = 0
    for transaction in db_transactions:
        transaction_id, description, amount, transaction_type, category = transaction

        if transaction_type.strip().lower() == "income":
            total_income += amount
        elif transaction_type.strip().lower() == "expenses":
            total_expenses += amount
    print("-------------------------")
    print(f"Total Income:   ₱{total_income:,.2f}")
    print(f"Total Expenses: ₱{total_expenses:,.2f}")
    print(f"Balance:        ₱{total_income - total_expenses:,.2f}")  
def delete_transaction():
    print("--- Delete Transaction ---")

    db_transactions = get_sqlite_transaction()

    if not db_transactions:
        print("No transactions to delete.")
        return

    for index, transaction in enumerate(db_transactions, start=1):
        transaction_id, description, amount, transaction_type, category = transaction

        print(
            f"{index}. {description} | "
            f"{transaction_type.title()} | "
            f"₱{amount:,.2f} | "
            f"{category}"
        )
    try:
        choice = int(input("Enter transaction number to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    if choice < 1 or choice > len(db_transactions):
        print("Transaction number not found.")
        return
    selected_transaction = db_transactions[choice - 1]
    transaction_id, description, amount, transaction_type, category = selected_transaction
    confirm = input(
        f"Are you sure you want to delete '{description}'? (y/n): "
    ).strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    connection.commit()
    connection.close()
    print(f"Deleted: {description}")
def edit_transaction():
    print("--- Edit Transaction ---")
    db_transactions = get_sqlite_transaction()
    if not db_transactions:
        print("No transactions to edit.")
        return
    for index, transaction in enumerate(db_transactions, start=1):
        transaction_id, description, amount, transaction_type, category = transaction
        print(
            f"{index}. {description} | "
            f"{transaction_type.title()} | "
            f"₱{amount:,.2f} | "
            f"{category}"
        )
    try:
        choice = int(input("Enter transaction number to edit: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    if choice < 1 or choice > len(db_transactions):
        print("Transaction number not found.")
        return
    selected_transaction = db_transactions[choice - 1]
    transaction_id, old_description, old_amount, old_type, old_category = selected_transaction
    print("--- Enter Updated Details ---")
    new_description = input("New description: ")
    while True:
        try:
            new_amount = float(input("New amount: "))
            if new_amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    while True:
        new_type = input("New type (Income or Expenses): ").strip().lower()
        if new_type == "income" or new_type == "expenses":
            break
        else:
            print("Please enter Income or Expenses.")
    new_category = input("New category: ")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE transactions
        SET description = ?, amount = ?, type = ?, category = ?
        WHERE id = ?
    """, (new_description, new_amount, new_type, new_category, transaction_id))
    connection.commit()
    connection.close()

    print("Transaction Updated Successfully!")
create_table()
while True:
    print("================================")
    print("  SMART PERSONAL FINANCE TRACKER")
    print("================================")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. View Financial Summary")
    print("4. Delete Transaction")
    print("5. Edit Transaction")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_transaction()
    elif choice == "2":
        view_transaction()
    elif choice == "3":
        financial_summary()
    elif choice == "4":
          delete_transaction()
    elif choice == "5":
          edit_transaction()
    elif choice == "6":
          print("Goodbye!")
          break
    else:
        print("Invalid option. Try again.")