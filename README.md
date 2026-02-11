
FINTRACK PRO – CLI FINANCE MANAGER
Project Documentation

1. Introduction
FinTrack Pro is a command line based personal finance management system developed using Python, SQLite and SQLAlchemy ORM. 
The project helps users to manage daily expenses, track subscriptions, search records, maintain monthly budgets and generate analytics using raw SQL queries.

2. Objectives
• To understand ORM based database interaction  
• To use SQLite with Python  
• To implement CRUD operations  
• To write raw SQL for analytics  
• To design modular architecture  
• To build interview oriented project

3. Technologies Used
• Python  
• SQLite Database  
• SQLAlchemy ORM  
• Raw SQL Queries  
• CLI Interface

4. System Features
• Add Expense  
• Update Expense  
• Delete Expense  
• Search by Date  
• Category Analytics  
• Monthly Budget Alert  
• Persistent Storage

5. Database Design

Tables:
1. categories(id, name)  
2. expenses(id, title, amount, date, category_id)  
3. subscriptions(id, name, amount, next_date)  
4. budgets(id, month, limit)

Relationships:
Category 1 ---- N Expenses

6. Modules Description

a) Expense Module
- Add new expense  
- Update existing expense  
- Delete expense  
- ORM based operations

b) Report Module
- Category wise total  
- Aggregation using GROUP BY  
- Raw SQL joins

c) Budget Module
- Set monthly limit  
- Compare with spending  
- Alert when exceeded

d) Search Module
- Find expenses by date using SQL query

7. Sample SQL Used

SELECT c.name, SUM(e.amount)
FROM categories c
JOIN expenses e
ON c.id = e.category_id
GROUP BY c.name;

8. Learning Outcomes
• ORM concepts  
• SQL joins & aggregation  
• Modular programming  
• Exception handling  
• CLI application design

9. Future Enhancements
• CSV Export  
• Flask UI  
• Authentication  
• Charts integration

10. Conclusion
This project demonstrates practical use of Python with databases and SQL. 
It is suitable for resume showcase and interview explanation.

# FinTracker
