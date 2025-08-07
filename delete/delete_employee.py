from tkinter import messagebox

def delete_employee(cur, conn, selected_id, clear_fields, view_all):
    if not selected_id:
        return
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (selected_id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Employee deleted.")
    clear_fields()
    view_all()


