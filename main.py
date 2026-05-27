import mysql.connector
from fastapi import FastAPI

conn_obj = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="Nani@2703",
    database="expenses"
)

cursor_obj = conn_obj.cursor(dictionary=True, buffered=True)

app = FastAPI()

@app.post("/expenses")
def add_expenses(expenses_data:dict):
    title = expenses_data["title"]
    amount = expenses_data["amount"]
    category = expenses_data["category"]
    spent_at = expenses_data["spent_at"]


    query = "insert into expense(title, amount, category, spent_at) values(%s, %s, %s, %s)"
    values = (expenses_data["title"], expenses_data["amount"], expenses_data["category"], expenses_data["spent_at"])
    cursor_obj.execute(query, values)
    conn_obj.commit()
    return {"message": "Expenses Added Successfully"}

@app.get("/get_expenses")
def get_expenses():
    query = "select * from expense"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()
    return {"expenses":data}

@app.get("/get_expenses_single/{expenses_id}")
def get_e(expenses_id: int):

    query = "SELECT * FROM expense WHERE exp_id=%s"

    cursor_obj.execute(query, (expenses_id,))
    dataa = cursor_obj.fetchone()

    if dataa:
        return {"expenses_data": dataa}

    return {"expenses_data": None}
    
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

@app.delete("/delete_expenses/{expense_id}")
def delete_expense(expense_id: int):

    query = "DELETE FROM expense WHERE exp_id=%s"

    cursor_obj.execute(query, (expense_id,))
    conn_obj.commit()

    return {"message": "Expense deleted successfully"}

@app.get("/search_expenses")
def search_expense(search_text:str):

    query = "select * from expense where category like %s or title like %s"
 
    cursor_obj.execute(query ,(f"%{search_text}%", f"%{search_text}%"))
    data = cursor_obj.fetchall()


    return {"expenses": data}

@app.get("/sort_expenses")
def sort_expenses(sort_by:str, order_by:str):

    query = f"select * from expense order by {sort_by} {order_by}"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"Expenses" : data}

@app.get("/filter_expenses/{Filter_by}")
def filter_expensess(Filter_by:str):

    query = "select * from expense where category = %s"
    cursor_obj.execute(query,(Filter_by,))
    data = cursor_obj.fetchall()

    return {"message": data}

@app.get("/analyze_expenses/{Analyze_by}")
def analyze_expenses(Analyze_by:str):
    query = f"select {Analyze_by}, sum(amount) from expense group by {Analyze_by}"
    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return {"message": data}