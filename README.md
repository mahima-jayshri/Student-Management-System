# 📚 Student Management System (Python + MySQL)

A fully functional **command-line Student Management System** built using **Python** and **MySQL**.
Supports operations like **Add, Update, Delete, View, Search, and Count Students**, with robust error handling and automatic database/table creation.

---

## 🚀 Features

### ✅ **Database Features**

* Automatic MySQL database connection setup
* Auto-creates `student_db` database if not present
* Auto-creates `students` table
* Graceful handling of MySQL errors

### 🧑‍🎓 **Student Operations**

| Feature              | Description                         |
| -------------------- | ----------------------------------- |
| ➕ Add Student        | Name, age, class, marks             |
| ✏️ Update Student    | Update selective fields dynamically |
| ❌ Delete Student     | Delete using ID                     |
| 👥 View All Students | Shows a formatted table             |
| 🔍 Search by Name    | Supports partial search             |
| 🔎 Search by ID      | Fetch a specific student            |
| 📊 Student Count     | Total number of records             |

### 🛡️ **Error Handling**

* Invalid input handling
* MySQL connection failure guidance
* Keyboard interrupt handling
* Clean closing of DB connections even on crash

---

## 🛠️ Installation & Setup

### **1️⃣ Install Dependencies**

Make sure Python is installed (3.x recommended).
Install MySQL connector:

```bash
pip install mysql-connector-python
```

### **2️⃣ Install & Start MySQL Server**

Ensure MySQL server is running locally.

### **3️⃣ Create Database (Optional)**

The script auto-creates the DB/table, but you can manually create:

```sql
CREATE DATABASE student_db;
```

### **4️⃣ Run the Program**

Run the main Python script:

```bash
python main.py
```

---

## ⚙️ How It Works

### **Automatic Database Setup**

The script tries multiple default configurations:

```
localhost: root / (no password)
localhost: root / root
127.0.0.1: root / (no password)
```

If all fail, user is asked to enter MySQL credentials manually.

### **Table Structure**

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    class VARCHAR(50) NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 📸 App Menu Preview

```
==============================================
📚 STUDENT MANAGEMENT SYSTEM
==============================================
1. ➕ Add New Student
2. ✏️  Update Student Information
3. ❌ Delete Student
4. 👥 View All Students
5. 🔍 Search Student by Name
6. 🔎 Search Student by ID
7. 📊 Display Student Count
8. 🚪 Exit
==============================================
```

---

## 🧩 Project Structure

```
student-management/
│
├── main.py                # Main program
├── README.md              # Documentation
└── requirements.txt       # (Optional) Dependencies
```

---

## 📦 Optional: requirements.txt

Add this file if needed:

```
mysql-connector-python
```

---


## 👨‍💻 Author

**Mahima**
Python & MySQL based academic project.

---

