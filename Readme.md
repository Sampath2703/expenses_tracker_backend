````md
# Expense Tracker Management System

An Expense Tracker Management System built using Streamlit, FastAPI, and MySQL.

---

# Project Overview

This project helps users manage daily expenses digitally. Users can:

- Add Expenses
- View Expenses
- Update Expenses
- Delete Expenses
- Search Expenses
- Sort Expenses
- Filter Expenses
- Analyze Expenses

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Streamlit | Frontend |
| FastAPI | Backend |
| MySQL | Database |
| Pandas | Data Handling |
| Requests | API Communication |
| Uvicorn | FastAPI Server |

---

# Project Structure

```text
Expense-Tracker/
│
├── frontend.py
├── backend.py
├── requirements.txt
├── .env
└── README.md
````

---

# Frontend Explanation

The frontend is developed using Streamlit.

## Frontend Features

* Add Expenses
* View Expenses
* Update Expenses
* Delete Expenses
* Search Expenses
* Sort Expenses
* Filter Expenses
* Analyze Expenses

## Streamlit Components Used

| Component         | Purpose            |
| ----------------- | ------------------ |
| st.title()        | Display Title      |
| st.header()       | Section Heading    |
| st.text_input()   | Text Input         |
| st.number_input() | Number Input       |
| st.selectbox()    | Dropdown Selection |
| st.date_input()   | Date Selection     |
| st.button()       | Button Actions     |
| st.dataframe()    | Display Table      |
| st.success()      | Success Message    |
| st.error()        | Error Message      |

---

# Backend Explanation

The backend is developed using FastAPI.

## Backend Features

* REST API Development
* CRUD Operations
* MySQL Database Connection
* Search API
* Sort API
* Filter API
* Analyze API

---

# API Endpoints

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| POST   | /expenses                      | Add Expense        |
| GET    | /get_expenses                  | Get All Expenses   |
| GET    | /get_expenses_single/{id}      | Get Single Expense |
| PUT    | /update_expenses/{id}          | Update Expense     |
| DELETE | /delete_expense/{id}           | Delete Expense     |
| GET    | /search_expenses               | Search Expenses    |
| GET    | /sort_expenses                 | Sort Expenses      |
| GET    | /filter_expenses/{filter_by}   | Filter Expenses    |
| GET    | /analyze_expenses/{analyze_by} | Analyze Expenses   |

---

# Database Setup

## Create Database

```sql
CREATE DATABASE expenses_db;
```

## Create Table

```sql
CREATE TABLE expenses1 (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    spent_at DATE NOT NULL
);
```

---

# Installation

## Step 1: Clone Repository

```bash
git clone <repository_link>
```

---

## Step 2: Install Packages

```bash
pip install -r requirements.txt
```

---

# Requirements.txt

```txt
streamlit
fastapi
uvicorn
mysql-connector-python
python-dotenv
pandas
requests
```

---

# Environment Variables (.env)

```env
db_host=localhost
db_user=root
db_password=your_password
db_database=expenses_db
db_port=3306
```

---

# Run Backend Server

```bash
uvicorn backend:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# Run Frontend Application

```bash
streamlit run frontend.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# Project Workflow

```text
User
   ↓
Streamlit Frontend
   ↓ API Requests
FastAPI Backend
   ↓ SQL Queries
MySQL Database
```

---

# Advantages

* User Friendly
* Fast Expense Management
* Easy Data Analysis
* Full Stack Python Project

---

# Future Enhancements

* User Authentication
* Expense Charts
* PDF/Excel Export
* Budget Planning

---

# Author

Sampath Kumar

---

# License

This project is developed for educational purposes.

```
```
