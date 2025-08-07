from tkinter import messagebox
from datetime import datetime

def create_employee(cur, conn, fields, photo_data, clear_fields, view_all):
    try:
        # Read individual fields
        name = fields["Name"].get().strip()
        age_str = fields["Age"].get().strip()
        dob_str = fields["DOB"].get().strip()
        sex = fields["Sex"].get()
        education = fields["Education"].get().strip()
        marital = fields["Marital Status"].get()
        blood = fields["Blood Type"].get()
        phone = fields["Phone"].get().strip()
        email = fields["Email"].get().strip()
        address = fields["Address"].get().strip()

        # Validate and convert Age
        try:
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Age must be a number.")
            return

        # Validate and convert DOB
        try:
            dob = datetime.strptime(dob_str, "%d.%m.%Y").date()
        except ValueError:
            messagebox.showerror("Invalid Date", "DOB must be in DD.MM.YYYY format.")
            return

        # Insert into database
        cur.execute("""
            INSERT INTO employees (photo, name, age, dob, sex, education_background,
                marital_status, blood_type, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (photo_data, name, age, dob, sex, education, marital, blood, phone, email, address))

        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully.")
        clear_fields()
        view_all()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to add employee.\n{str(e)}")
