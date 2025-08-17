from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image as PilImage, ImageTk
from database.db import get_connection
from create.upload_photo import load_photo
from create.create_employee import create_employee
from update.update_employee import update_employee
from delete.delete_employee import delete_employee
from export.export_pdf import export_pdf
import io
import re

# Database setup
conn = get_connection()
cur = conn.cursor()

# Root Window
root = Tk()
root.title("Employee Manager")
root.geometry("900x650")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# Data Fields
fields = {
    "Employee ID": StringVar(),
    "Name": StringVar(),
    "Age": StringVar(),
    "DOB": StringVar(),
    "Sex": StringVar(value="Male"),  # Default to Male
    "Education": StringVar(),
    "Marital Status": StringVar(value=""),
    "Blood Type": StringVar(value=""),
    "Phone": StringVar(),
    "Email": StringVar(),
    "Address": StringVar()
}

marital_options = ["", "Single", "Married", "Divorced", "Widowed"]
blood_options = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

photo_data = None
selected_id = None

# Default blank image (white 80x100)
blank_img = PilImage.new("RGB", (80, 100), color="white")
blank_tk = ImageTk.PhotoImage(blank_img)

# --- Validation Function ---
def validate_fields():
    name = fields["Name"].get().strip()
    age = fields["Age"].get().strip()
    dob = fields["DOB"].get().strip()
    phone = fields["Phone"].get().strip()
    email = fields["Email"].get().strip()

    if not all(v.get().strip() for k, v in fields.items() if k != "Employee ID"):
        messagebox.showerror("Validation Error", "All fields must be filled.")
        return False

    if not photo_data:
        messagebox.showerror("Validation Error", "Photo is required.")
        return False

    if not age.isdigit():
        messagebox.showerror("Validation Error", "Age must be a number.")
        return False

    if not re.match(r"^\d{2}[-./]\d{2}[-./]\d{4}$", dob):
        messagebox.showerror("Validation Error", "DOB must be in format dd.mm.yyyy")
        return False

    if not re.match(r"^09\d{9}$", phone):
        messagebox.showerror("Validation Error", "Phone must start with 09 and be 11 digits long.")
        return False

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        messagebox.showerror("Validation Error", "Invalid email format.")
        return False
    return True

# Functions
def view_all():
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT employee_id, name FROM employees ORDER BY employee_id")
    for row in cur.fetchall():
        tree.insert("", "end", values=(row[0], row[1]))

def search_by_name():
    name_query = search_var.get().strip()
    for row in tree.get_children():
        tree.delete(row)

    if name_query == "":
        view_all()
        return

    cur.execute("SELECT employee_id, name FROM employees WHERE name ILIKE %s", (f"%{name_query}%",))
    results = cur.fetchall()
    if results:
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))
    else:
        messagebox.showinfo("No Results", f"No employee found with name '{name_query}'.")

def load_selected(event):
    global selected_id, photo_data
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if not values:
        return
    emp_id = int(values[0])
    selected_id = emp_id
    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (emp_id,))
    row = cur.fetchone()
    if row:
        employee_id, photo_data, name, age, dob, sex, edu, marital, blood, phone, email, addr = row
        fields["Employee ID"].set(str(employee_id))
        fields["Name"].set(name)
        fields["Age"].set(str(age))
        fields["DOB"].set(dob.strftime("%d.%m.%Y"))
        fields["Sex"].set(sex)
        fields["Education"].set(edu)
        fields["Marital Status"].set(marital)
        fields["Blood Type"].set(blood)
        fields["Phone"].set(phone)
        fields["Email"].set(email)
        fields["Address"].set(addr)
        if photo_data:
            img = PilImage.open(io.BytesIO(photo_data)).resize((80, 100))
            photo_label.img = ImageTk.PhotoImage(img)
            photo_label.configure(image=photo_label.img)

def clear_fields():
    global selected_id, photo_data
    for var in fields.values():
        var.set("")
    selected_id = None
    photo_data = None
    fields["Sex"].set("Male")
    photo_label.configure(image=blank_tk)
    photo_label.img = blank_tk

def set_photo(data):
    global photo_data
    photo_data = data
    if data:
        img = PilImage.open(io.BytesIO(data)).resize((80, 100))
        photo_label.img = ImageTk.PhotoImage(img)
        photo_label.configure(image=photo_label.img)

# Title
title_label = Label(root, text="Employee Manager", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#333")
title_label.pack(pady=10)

# Search Box
search_frame = ttk.Frame(root, padding=(10, 5))
search_frame.pack(fill=X, padx=10)

search_var = StringVar()
ttk.Label(search_frame, text="Search by Name:").pack(side=LEFT, padx=(0, 5))
ttk.Entry(search_frame, textvariable=search_var, width=30).pack(side=LEFT)
ttk.Button(search_frame, text="Search", command=search_by_name).pack(side=LEFT, padx=(5, 10))
ttk.Button(search_frame, text="Show All", command=view_all).pack(side=LEFT)

# Main Layout
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=BOTH, expand=True)
main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)

# Form Frame
form_frame = ttk.LabelFrame(main_frame, text="Employee Information", padding=10)
form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
form_frame.columnconfigure(1, weight=1)

# Photo
photo_label = Label(form_frame, bg="white", width=80, height=100, relief=SOLID, bd=1)
photo_label.grid(row=0, column=2, rowspan=2, sticky=N, padx=(10, 0), pady=(0, 5))
photo_label.configure(image=blank_tk)
photo_label.img = blank_tk
(ttk.Button(form_frame, text="Load Photo", command=lambda: set_photo(load_photo(photo_label)))
 .grid(row=2, column=2, sticky=N))

# Form Fields
row_idx = 0
for label, var in fields.items():
    if label == "Sex":
        ttk.Label(form_frame, text="Sex:").grid(row=row_idx, column=0, sticky=W, pady=5, padx=(0, 10))
        sex_frame = Frame(form_frame)
        sex_frame.grid(row=row_idx, column=1, sticky=W)
        Radiobutton(sex_frame, text="Male", variable=fields["Sex"], value="Male").pack(side=LEFT, padx=5)
        Radiobutton(sex_frame, text="Female", variable=fields["Sex"], value="Female").pack(side=LEFT, padx=5)
        row_idx += 1
        continue

    ttk.Label(form_frame, text=label + ":").grid(row=row_idx, column=0, sticky=W, pady=5, padx=(0, 10))
    if label in ["Marital Status", "Blood Type"]:
        options = marital_options if label == "Marital Status" else blood_options
        (ttk.Combobox(form_frame, textvariable=var, values=options, width=28, state="readonly")
         .grid(row=row_idx, column=1, sticky=W))
    elif label == "Employee ID":
        ttk.Entry(form_frame, textvariable=var, width=30, state="readonly").grid(row=row_idx, column=1, sticky=W)
    else:
        ttk.Entry(form_frame, textvariable=var, width=30).grid(row=row_idx, column=1, sticky=W)
    row_idx += 1

# Treeview Frame
tree_frame = ttk.LabelFrame(main_frame, text="Employee List", padding=10)
tree_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name"), show="headings", height=20)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.column("ID", width=50, anchor="center")
tree.column("Name", width=180)
tree.pack(fill=BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", load_selected)

# Buttons Frame
btn_frame = ttk.Frame(main_frame, padding=10)
btn_frame.grid(row=1, column=0, columnspan=2)

ttk.Button(btn_frame, text="Create", width=15,
           command=lambda: create_employee(cur, conn, fields, photo_data, clear_fields, view_all)
           if validate_fields() else None).grid(row=0, column=0, padx=5)

ttk.Button(btn_frame, text="Update", width=15,
           command=lambda: update_employee(cur, conn, selected_id, fields, photo_data, clear_fields, view_all)
           if validate_fields() else None).grid(row=0, column=1, padx=5)

(ttk.Button(btn_frame, text="Delete", width=15,
           command=lambda: delete_employee(cur, conn, selected_id, clear_fields, view_all))
 .grid(row=0, column=2, padx=5))

ttk.Button(btn_frame, text="Export PDF", width=15,
           command=lambda: export_pdf(cur)).grid(row=0, column=3, padx=5)

ttk.Button(btn_frame, text="Clear Fields", width=15,
           command=clear_fields).grid(row=0, column=4, padx=5)

if __name__ == "__main__":
    view_all()
    root.mainloop()
