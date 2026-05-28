from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
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
CREATE TABLE if not exists expenses1 (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    payment_method varchar(50) Not Null,
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




# Add Expense
@app.post("/expenses")
def add_expenses(expenses_data: dict):

    try:
        query = """
        INSERT INTO expenses1
        (title, payment_method, amount, category, spent_at)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            expenses_data.get("title"),
            expenses_data.get("payment_method"),
            expenses_data.get("amount"),
            expenses_data.get("category"),
            expenses_data.get("spent_at")
        )

        cursor_obj.execute(query, values)
        conn_obj.commit()

        return {"message": "Expenses Added Successfully"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/get_expenses")
def get_expenses():
    query = "select * from expenses1"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()
    return {"expenses":data}

@app.get("/get_expenses_single/{expenses_id}")
def get_e(expenses_id: int):

    query = "SELECT * FROM expenses1 WHERE expense_id=%s"

    cursor_obj.execute(query, (expenses_id,))
    data = cursor_obj.fetchone()

    if not data:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"expenses_data": data}


    
@app.put("/update_expenses/{expenses_id}")
def update_expenses(expenses_id: int, updated_expenses_data: dict):

    try:

        query = """
        UPDATE expenses1
        SET
            title=%s,
            amount=%s,
            category=%s,
            payment_method=%s,
            spent_at=%s
        WHERE expense_id=%s
        """

        values = (
            updated_expenses_data["title"],
            updated_expenses_data["amount"],
            updated_expenses_data["category"],
            updated_expenses_data["payment_method"],
            updated_expenses_data["spent_at"],
            expenses_id
        )

        cursor_obj.execute(query, values)
        conn_obj.commit()

        if cursor_obj.rowcount == 0:
            return {"message": "Expense Not Found"}

        return {
            "message": "Expense Updated Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: int):

    try:
        cursor_obj.execute(
            "DELETE FROM expenses1 WHERE expense_id=%s",
            (expense_id,)
        )

        conn_obj.commit()

        if cursor_obj.rowcount == 0:
            return {"message": "Expense not found"}

        return {"message": "Expense deleted successfully"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/search_expenses")
def search_expense(search_text:str):

    query = "select * from expenses1 where category like %s or title like %s"
    cursor_obj.execute(query ,(f"%{search_text}%", f"%{search_text}%"))
    data = cursor_obj.fetchall()


    return {"expenses": data}

@app.get("/sort_expenses")
def sort_expenses(sort_by: str, order_by: str):

    allowed_columns = ["payment_method", "amount", "category", "spent_at"]
    allowed_order = ["asc", "desc"]

    if sort_by not in allowed_columns or order_by not in allowed_order:
        return {"error": "Invalid parameters"}

    query = f"SELECT * FROM expenses1 ORDER BY {sort_by} {order_by}"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"expenses": data}

@app.get("/filter_expenses/{filter_by}")
def filter_expenses(filter_by: str):

    cursor_obj.execute(
        "SELECT * FROM expenses1 WHERE category=%s",
        (filter_by,)
    )

    data = cursor_obj.fetchall()

    return {"expenses": data}

@app.get("/analyze_expenses/{analyze_by}")
def analyze_expenses(analyze_by: str):

    allowed = ["category", "payment_method", "spent_at"]

    if analyze_by not in allowed:
        return {"error": "Invalid field"}

    query = f"""
        SELECT {analyze_by}, SUM(amount) as total
        FROM expenses1
        GROUP BY {analyze_by}
    """

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"expenses": data}