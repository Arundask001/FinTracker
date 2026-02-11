# =====================================
# FINTRACK PRO - CLI FINANCE MANAGER
# =====================================

# ---------- IMPORTS ----------
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ---------- DATABASE CONNECTION ----------
# Step 1: Create Engine
engine = create_engine("sqlite:///fintrack.db", echo=True)
Base = declarative_base()

# Step 2: Session Setup
Session = sessionmaker(bind=engine)
session = Session()


# ---------- TABLE DEFINITIONS ----------

# 1. categories(id, name)
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship: Category 1 ---- N Expenses
    expenses = relationship("Expense", back_populates="category")


# 2. expenses(id, title, amount, date, category_id)
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)
    date = Column(String)  # YYYY-MM-DD
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="expenses")


# 3. subscriptions(id, name, amount, next_date)
class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    next_date = Column(String)


# 4. budgets(id, month, limit)
class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    month = Column(String)  # YYYY-MM
    limit = Column(Float)


# Create all tables
Base.metadata.create_all(engine)


# ---------- FUNCTIONS (CRUD & ANALYTICS) ----------

def add_expense():
    title = input("Expense Title: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    cat_id = int(input("Category ID: "))

    new_expense = Expense(title=title, amount=amount, date=date, category_id=cat_id)
    session.add(new_expense)
    session.commit()
    print("Expense added successfully!")


def update_expense():
    eid = int(input("Enter Expense ID to update: "))
    expense = session.query(Expense).filter(Expense.id == eid).first()
    if expense:
        expense.amount = float(input("New Amount: "))
        session.commit()
        print("Expense updated!")
    else:
        print("Expense not found")


def delete_expense():
    eid = int(input("Enter Expense ID to delete: "))
    expense = session.query(Expense).filter(Expense.id == eid).first()
    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted!")
    else:
        print("Expense not found")


def search_by_date():
    date = input("Enter date (YYYY-MM-DD): ")
    # Using SQL query as per module D
    results = session.query(Expense).filter(Expense.date == date).all()
    for e in results:
        print(f"{e.id} | {e.title} | {e.amount} | {e.category.name}")


def category_analytics():
    # Raw SQL Join & Group By as per documentation requirements
    sql = """
    SELECT c.name, SUM(e.amount)
    FROM categories c
    JOIN expenses e ON c.id = e.category_id
    GROUP BY c.name
    """
    result = session.execute(text(sql))
    print("\nCATEGORY WISE TOTALS")
    for row in result:
        print(f"{row[0]} -> {row[1]}")


def budget_alert():
    month = input("Enter month (YYYY-MM): ")
    # Raw SQL for aggregation
    total_spent = session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar() or 0

    budget = session.query(Budget).filter(Budget.month == month).first()

    if budget:
        print(f"Spent: {total_spent} / Limit: {budget.limit}")
        if total_spent > budget.limit:
            print("ALERT: Monthly budget exceeded!")
        else:
            print("Within budget.")
    else:
        print("No budget set for this month.")


# ---------- CLI MENU ----------

while True:
    print(f"\n{'=' * 10} FINTRACK PRO {'=' * 10}")
    print("1. Add Expense\n2. Update Expense\n3. Delete Expense")
    print("4. Search by Date\n5. Category Analytics\n6. Budget Alert")
    print("7. Add Category\n8. Set Budget\n9. Exit")

    choice = input("Select Option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        update_expense()
    elif choice == "3":
        delete_expense()
    elif choice == "4":
        search_by_date()
    elif choice == "5":
        category_analytics()
    elif choice == "6":
        budget_alert()
    elif choice == "7":
        name = input("Category Name: ")
        session.add(Category(name=name))
        session.commit()
    elif choice == "8":
        m = input("Month (YYYY-MM): ")
        l = float(input("Limit: "))
        session.add(Budget(month=m, limit=l))
        session.commit()
    elif choice == "9":
        break
    else:
        print("Invalid Choice!")