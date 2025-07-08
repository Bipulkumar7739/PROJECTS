import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database creation
def create_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        mobile TEXT,
        email TEXT,
        address TEXT,
        mother TEXT,
        father TEXT,
        father_mobile TEXT,
        admission_time TEXT,
        dob TEXT,
        student_class TEXT,
        gender TEXT,
        entry_time TEXT
    )""")
    conn.commit()
    conn.close()

create_db()

# Add record
def add_student():
    if name_var.get() == "" or roll_var.get() == "":
        messagebox.showerror("Input Error", "Name and Roll No are required!")
        return
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, roll, mobile, email, address, mother, father, father_mobile, admission_time, dob, student_class, gender, entry_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (name_var.get(), roll_var.get(), mobile_var.get(), email_var.get(), address_var.get(), mother_var.get(), father_var.get(), father_mobile_var.get(), admission_time_var.get(), dob_var.get(), class_var.get(), gender_var.get(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student record added!")
    fetch_data()
    clear_fields()

# Fetch records
def fetch_data():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", tk.END, values=row)
    conn.close()

# Clear input fields
def clear_fields():
    for var in [name_var, roll_var, mobile_var, email_var, address_var, mother_var, father_var, father_mobile_var, admission_time_var, dob_var, class_var, gender_var]:
        var.set("")

# Select row
def on_row_select(event):
    selected = student_table.focus()
    values = student_table.item(selected, 'values')
    if values:
        name_var.set(values[1])
        roll_var.set(values[2])
        mobile_var.set(values[3])
        email_var.set(values[4])
        address_var.set(values[5])
        mother_var.set(values[6])
        father_var.set(values[7])
        father_mobile_var.set(values[8])
        admission_time_var.set(values[9])
        dob_var.set(values[10])
        class_var.set(values[11])
        gender_var.set(values[12])

# Update
def update_student():
    selected = student_table.focus()
    if not selected:
        messagebox.showerror("Select Error", "Select a student to update!")
        return
    sid = student_table.item(selected, 'values')[0]
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""UPDATE student SET 
        name=?, roll=?, mobile=?, email=?, address=?, mother=?, father=?, father_mobile=?, admission_time=?, dob=?, student_class=?, gender=?
        WHERE id=?""",
        (name_var.get(), roll_var.get(), mobile_var.get(), email_var.get(), address_var.get(), mother_var.get(), father_var.get(), father_mobile_var.get(), admission_time_var.get(), dob_var.get(), class_var.get(), gender_var.get(), sid))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Record updated successfully!")
    fetch_data()
    clear_fields()

# Delete
def delete_student():
    selected = student_table.focus()
    if not selected:
        messagebox.showerror("Select Error", "Select a student to delete!")
        return
    sid = student_table.item(selected, 'values')[0]
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Record deleted!")
    fetch_data()
    clear_fields()

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("1200x700")
root.configure(bg="#e0f7fa")

title = tk.Label(root, text="🎓 Student Management System", font=("Arial", 24, "bold"), bg="#00796b", fg="white")
title.pack(fill=tk.X)

frame = tk.Frame(root, bg="#b2dfdb")
frame.place(x=20, y=60, width=1160, height=270)

# Variables
name_var = tk.StringVar()
roll_var = tk.StringVar()
mobile_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()
mother_var = tk.StringVar()
father_var = tk.StringVar()
father_mobile_var = tk.StringVar()
admission_time_var = tk.StringVar()
dob_var = tk.StringVar()
class_var = tk.StringVar()
gender_var = tk.StringVar()

# Entry Fields
labels = ["Name", "Roll No", "Mobile", "Email", "Address", "Mother's Name", "Father's Name", "Father's Mobile", "Admission Time", "DOB", "Class", "Gender"]
vars = [name_var, roll_var, mobile_var, email_var, address_var, mother_var, father_var, father_mobile_var, admission_time_var, dob_var, class_var, gender_var]

for idx, (label, var) in enumerate(zip(labels, vars)):
    tk.Label(frame, text=label, bg="#b2dfdb", font=("Arial", 10, "bold")).grid(row=idx//4, column=(idx%4)*2, padx=10, pady=5, sticky="w")
    tk.Entry(frame, textvariable=var, width=25).grid(row=idx//4, column=(idx%4)*2+1, padx=10, pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#004d40")
btn_frame.place(x=20, y=340, width=1160, height=50)

tk.Button(btn_frame, text="Add", width=20, command=add_student).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(btn_frame, text="Update", width=20, command=update_student).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Delete", width=20, command=delete_student).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Clear", width=20, command=clear_fields).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Show All", width=20, command=fetch_data).pack(side=tk.LEFT, padx=10)

# Table
table_frame = tk.Frame(root)
table_frame.place(x=20, y=400, width=1160, height=280)

scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
student_table = ttk.Treeview(table_frame, columns=("id", "name", "roll", "mobile", "email", "address", "mother", "father", "father_mobile", "admission_time", "dob", "class", "gender", "entry_time"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)

student_table.heading("id", text="ID")
student_table.heading("name", text="Name")
student_table.heading("roll", text="Roll No")
student_table.heading("mobile", text="Mobile")
student_table.heading("email", text="Email")
student_table.heading("address", text="Address")
student_table.heading("mother", text="Mother")
student_table.heading("father", text="Father")
student_table.heading("father_mobile", text="Father's Mobile")
student_table.heading("admission_time", text="Admission Time")
student_table.heading("dob", text="DOB")
student_table.heading("class", text="Class")
student_table.heading("gender", text="Gender")
student_table.heading("entry_time", text="Entry Time")

student_table['show'] = 'headings'
student_table.column("id", width=50)
for col in student_table["columns"][1:]:
    student_table.column(col, width=120)

student_table.pack(fill=tk.BOTH, expand=1)
student_table.bind("<ButtonRelease-1>", on_row_select)

fetch_data()
root.mainloop()