import tkinter as tk
from tkinter import messagebox
from data_manager import save_data, load_data


class Employee:
    def __init__(self, name, emp_id, department, job_title, basic_salary, manager_id=None):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.manager_id = manager_id

    def display_details(self):
        return f"Name: {self.name}, ID: {self.emp_id}, Department: {self.department}, Job Title: {self.job_title}, Basic Salary: {self.basic_salary}, Manager ID: {self.manager_id}"


def add_employee():
    name = name_entry.get()
    emp_id = emp_id_entry.get()
    department = department_entry.get()
    job_title = job_title_entry.get()
    basic_salary = basic_salary_entry.get()
    manager_id = manager_id_entry.get()

    employee = Employee(name, emp_id, department, job_title, basic_salary, manager_id)
    employees.append(employee)
    save_data("employees.bin", employees)
    messagebox.showinfo("Success", "Employee added successfully.")


def delete_employee():
    emp_id = emp_id_entry.get()
    for employee in employees:
        if employee.emp_id == emp_id:
            employees.remove(employee)
            save_data("employees.bin", employees)
            messagebox.showinfo("Success", "Employee deleted successfully.")
            return
    messagebox.showerror("Error", "Employee not found.")


def display_employee():
    emp_id = emp_id_entry.get()
    for employee in employees:
        if employee.emp_id == emp_id:
            messagebox.showinfo("Employee Details", employee.display_details())
            return
    messagebox.showerror("Error", "Employee not found.")


def main():
    global name_entry, emp_id_entry, department_entry, job_title_entry, basic_salary_entry, manager_id_entry, employees

    # Load existing employee data
    employees = load_data("employees.bin")

    root = tk.Tk()
    root.title("Event Management System")

    # Labels
    tk.Label(root, text="Name:").grid(row=0, column=0)
    tk.Label(root, text="Employee ID:").grid(row=1, column=0)
    tk.Label(root, text="Department:").grid(row=2, column=0)
    tk.Label(root, text="Job Title:").grid(row=3, column=0)
    tk.Label(root, text="Basic Salary:").grid(row=4, column=0)
    tk.Label(root, text="Manager ID:").grid(row=5, column=0)

    # Entry fields
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1)
    emp_id_entry = tk.Entry(root)
    emp_id_entry.grid(row=1, column=1)
    department_entry = tk.Entry(root)
    department_entry.grid(row=2, column=1)
    job_title_entry = tk.Entry(root)
    job_title_entry.grid(row=3, column=1)
    basic_salary_entry = tk.Entry(root)
    basic_salary_entry.grid(row=4, column=1)
    manager_id_entry = tk.Entry(root)
    manager_id_entry.grid(row=5, column=1)

    # Buttons
    add_button = tk.Button(root, text="Add Employee", command=add_employee)
    add_button.grid(row=6, column=0, columnspan=2, pady=10)
    delete_button = tk.Button(root, text="Delete Employee", command=delete_employee)
    delete_button.grid(row=7, column=0, columnspan=2, pady=10)
    display_button = tk.Button(root, text="Display Employee", command=display_employee)
    display_button.grid(row=8, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()