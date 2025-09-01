from tkinter import messagebox
from datetime import datetime
def update_employee(cur, conn, selected_id, fields, photo_data, clear_fields, view_all):
    if not selected_id:
        messagebox.showwarning("No Selection", "Please select an employee to update.")
        return
    try:
        # Read individual fields safely
        name = fields["Name"].get().strip().title()
        age_str = fields["Age"].get().strip()
        dob_str = fields["DOB"].get().strip()
        sex = fields["Sex"].get()
        education = fields["Education"].get().strip()
        marital = fields["Marital Status"].get()
        blood = fields["Blood Type"].get()
        phone = fields["Phone"].get().strip()
        email = fields["Email"].get().strip()
        address = fields["Address"].get().strip()

        # Validate and convert age
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

        cur.execute("""
            UPDATE employees SET photo=%s, name=%s, age=%s, dob=%s, sex=%s, education_background=%s,
            marital_status=%s, blood_type=%s, phone=%s, email=%s, address=%s
            WHERE employee_id=%s
        """, (photo_data, name, age, dob, sex, education, marital, blood, phone, email, address, selected_id))

        conn.commit()
        messagebox.showinfo("Updated", "Employee updated successfully.")
        clear_fields()
        view_all()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to update employee.\n{str(e)}")
