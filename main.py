from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL Connection
conn_obj = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_database"),
    port=int(os.getenv("db_port", 3306))
)

cursor_obj = conn_obj.cursor(dictionary=True, buffered=True)
cursor_obj.execute("""
CREATE TABLE expense (
    exp_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    spent_at DATE NOT NULL
);
""")

conn_obj.commit()

@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }


@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }

# Add Expense
@app.post("/expenses")
def add_expenses(expenses_data: dict):

    query = """
    INSERT INTO expense(title, amount, category, spent_at)
    VALUES(%s, %s, %s, %s)
    """

    values = (
        expenses_data["title"],
        expenses_data["amount"],
        expenses_data["category"],
        expenses_data["spent_at"]
    )

    cursor_obj.execute(query, values)
    conn_obj.commit()

    return {"message": "Expense Added Successfully"}

# Get All Expenses
@app.get("/get_expenses")
def get_expenses():

    query = "SELECT * FROM expense"

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"expenses": data}

# Get Single Expense
@app.get("/get_expenses_single/{expenses_id}")
def get_single_expense(expenses_id: int):

    query = "SELECT * FROM expense WHERE exp_id=%s"

    cursor_obj.execute(query, (expenses_id,))
    data = cursor_obj.fetchone()

    if data:
        return {"expense_data": data}

    return {"expense_data": None}

# Update Expense
@app.put("/update_expenses/{expenses_id}")
def update_expenses(expenses_id: int, updated_expenses_data: dict):

    query = """
    UPDATE expense
    SET title=%s,
        amount=%s,
        category=%s,
        spent_at=%s
    WHERE exp_id=%s
    """

    values = (
        updated_expenses_data["title"],
        updated_expenses_data["amount"],
        updated_expenses_data["category"],
        updated_expenses_data["spent_at"],
        expenses_id
    )

    cursor_obj.execute(query, values)
    conn_obj.commit()

    return {"message": "Expense Updated Successfully"}

# Delete Expense
@app.delete("/delete_expenses/{expense_id}")
def delete_expense(expense_id: int):

    query = "DELETE FROM expense WHERE exp_id=%s"

    cursor_obj.execute(query, (expense_id,))
    conn_obj.commit()

    return {"message": "Expense Deleted Successfully"}

# Search Expenses
@app.get("/search_expenses")
def search_expense(search_text: str):

    query = """
    SELECT * FROM expense
    WHERE category LIKE %s OR title LIKE %s
    """

    cursor_obj.execute(
        query,
        (f"%{search_text}%", f"%{search_text}%")
    )

    data = cursor_obj.fetchall()

    return {"expenses": data}

# Sort Expenses
@app.get("/sort_expenses")
def sort_expenses(sort_by: str, order_by: str):

    allowed_columns = ["title", "amount", "category", "spent_at"]
    allowed_order = ["asc", "desc"]

    if sort_by.lower() not in allowed_columns:
        return {"error": "Invalid sort column"}

    if order_by.lower() not in allowed_order:
        return {"error": "Invalid order"}

    query = f"""
    SELECT * FROM expense
    ORDER BY {sort_by} {order_by.upper()}
    """

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"expenses": data}

# Filter Expenses
@app.get("/filter_expenses/{filter_by}")
def filter_expenses(filter_by: str):

    query = "SELECT * FROM expense WHERE category=%s"

    cursor_obj.execute(query, (filter_by,))
    data = cursor_obj.fetchall()

    return {"expenses": data}

# Analyze Expenses
@app.get("/analyze_expenses/{analyze_by}")
def analyze_expenses(analyze_by: str):

    allowed_columns = ["category", "spent_at"]

    if analyze_by.lower() not in allowed_columns:
        return {"error": "Invalid analyze column"}

    query = f"""
    SELECT {analyze_by}, SUM(amount) AS total_amount
    FROM expense
    GROUP BY {analyze_by}
    """

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"analysis": data}