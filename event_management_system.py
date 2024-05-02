import tkinter as tk
from tkinter import ttk
import pickle

class Employee:
    """Class to represent details of an employee"""
    def __init__(self, name="", employee_id="", manager_id="", department="", job_title="", basic_salary=""):
        self.name = name
        self.employee_id = employee_id
        self.manager_id = manager_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary

class EmployeeForm():
    '''Class to represent a GUI form to enter employee details.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Employee Form")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.employee_id_label = tk.Label(self.root, text="Employee ID:")
        self.employee_id_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.employee_id_entry = tk.Entry(self.root)
        self.employee_id_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.manager_id_label = tk.Label(self.root, text="Manager ID:")
        self.manager_id_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.manager_id_entry = tk.Entry(self.root)
        self.manager_id_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.department_label = tk.Label(self.root, text="Department:")
        self.department_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.department_entry = tk.Entry(self.root)
        self.department_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.job_title_label = tk.Label(self.root, text="Job Title:")
        self.job_title_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.job_title_entry = tk.Entry(self.root)
        self.job_title_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.basic_salary_label = tk.Label(self.root, text="Basic Salary:")
        self.basic_salary_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.basic_salary_entry = tk.Entry(self.root)
        self.basic_salary_entry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=6, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.name_entry.delete(0, tk.END)
        self.employee_id_entry.delete(0, tk.END)
        self.manager_id_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.job_title_entry.delete(0, tk.END)
        self.basic_salary_entry.delete(0, tk.END)

    def submit(self):
        name = self.name_entry.get()
        employee_id = self.employee_id_entry.get()
        manager_id = self.manager_id_entry.get()
        department = self.department_entry.get()
        job_title = self.job_title_entry.get()
        basic_salary = self.basic_salary_entry.get()
        employee = Employee(name, employee_id, manager_id, department, job_title, basic_salary)
        if employee_id not in allemployees:
            allemployees[employee_id] = employee
            with open("employees.pkl", "ab") as file:
                pickle.dump(employee, file)
            self.clearBoxes()
            print("Employee added successfully. Employee ID: " + employee_id)
        else:
            print("Employee with Employee ID {} already exists.".format(employee_id))

class ListEmployeeForm:
    """Class to represent a GUI form to display all employees"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Employee Details")

        self.table = ttk.Treeview(self.root, columns=('Name', 'Employee ID', 'Manager ID', 'Department', 'Job Title', 'Basic Salary'), show='headings')
        self.table.heading('Name', text='Name')
        self.table.heading('Employee ID', text='Employee ID')
        self.table.heading('Manager ID', text='Manager ID')
        self.table.heading('Department', text='Department')
        self.table.heading('Job Title', text='Job Title')
        self.table.heading('Basic Salary', text='Basic Salary')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Employee ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_employee)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_employee)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_employee)
        self.delete_button.pack(pady=10)

        try:
            with open('employees.pkl', 'rb') as file:
                while True:
                    employee = pickle.load(file)
                    if isinstance(employee, Employee):
                        self.table.insert('', 'end', values=(employee.name, employee.employee_id, employee.manager_id, employee.department, employee.job_title, employee.basic_salary))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_employee(self):
        employee_id = self.search_entry.get()
        if employee_id in allemployees:
            employee = allemployees[employee_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(employee.name, employee.employee_id, employee.manager_id, employee.department, employee.job_title, employee.basic_salary))
        else:
            print("Employee with Employee ID {} not found.".format(employee_id))

    def edit_employee(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        employee_id = self.table.item(selected_item)['values'][1]

        with open("employees.pkl", "rb") as file:
            employees = []
            while True:
                try:
                    employee = pickle.load(file)
                    if isinstance(employee, Employee):
                        if employee.employee_id == employee_id:
                            employees.append(employee)
                        else:
                            employees.append(employee)
                except EOFError:
                    break

        # Open a new window or dialog box for editing employee details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Employee Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Employee ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Manager ID:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Department:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Job Title:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Basic Salary:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        name_var = tk.StringVar(value=employees[0].name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        employee_id_var = tk.StringVar(value=employees[0].employee_id)
        tk.Entry(edit_window, textvariable=employee_id_var, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        manager_id_var = tk.StringVar(value=employees[0].manager_id)
        tk.Entry(edit_window, textvariable=manager_id_var).grid(row=2, column=1, padx=5, pady=5)
        department_var = tk.StringVar(value=employees[0].department)
        tk.Entry(edit_window, textvariable=department_var).grid(row=3, column=1, padx=5, pady=5)
        job_title_var = tk.StringVar(value=employees[0].job_title)
        tk.Entry(edit_window, textvariable=job_title_var).grid(row=4, column=1, padx=5, pady=5)
        basic_salary_var = tk.StringVar(value=employees[0].basic_salary)
        tk.Entry(edit_window, textvariable=basic_salary_var).grid(row=5, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the employee object with the edited details
            employees[0].name = name_var.get()
            employees[0].manager_id = manager_id_var.get()
            employees[0].department = department_var.get()
            employees[0].job_title = job_title_var.get()
            employees[0].basic_salary = basic_salary_var.get()

            # Rewrite the entire employees list to the file with the updated employee details
            with open("employees.pkl", "wb") as file:
                for emp in employees:
                    pickle.dump(emp, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(employees[0].name, employees[0].employee_id, employees[0].manager_id, employees[0].department, employees[0].job_title, employees[0].basic_salary))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_employee(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        employee_id = self.table.item(selected_item)['values'][1]

        with open("employees.pkl", "rb") as file:
            employees = []
            while True:
                try:
                    employee = pickle.load(file)
                    if isinstance(employee, Employee) and employee.employee_id != employee_id:
                        employees.append(employee)
                except EOFError:
                    break

        with open("employees.pkl", "wb") as file:
            for employee in employees:
                pickle.dump(employee, file)

        self.table.delete(selected_item)

# List to save employee details
allemployees = {}

# Create Object of the Employee Form
form = EmployeeForm()

# Create Object of the List Employee Form
showemployee = ListEmployeeForm()

class Event:
    """Class to represent details of an event"""
    def __init__(self, event_id="", event_name="", event_date="", event_location="", event_description=""):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        self.event_description = event_description

class EventForm():
    '''Class to represent a GUI form to enter event details.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Event Form")

        self.event_id_label = tk.Label(self.root, text="Event ID:")
        self.event_id_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.event_id_entry = tk.Entry(self.root)
        self.event_id_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.event_name_label = tk.Label(self.root, text="Event Name:")
        self.event_name_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.event_name_entry = tk.Entry(self.root)
        self.event_name_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.event_date_label = tk.Label(self.root, text="Event Date:")
        self.event_date_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.event_date_entry = tk.Entry(self.root)
        self.event_date_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.event_location_label = tk.Label(self.root, text="Event Location:")
        self.event_location_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.event_location_entry = tk.Entry(self.root)
        self.event_location_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.event_description_label = tk.Label(self.root, text="Event Description:")
        self.event_description_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.event_description_entry = tk.Entry(self.root)
        self.event_description_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=5, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.event_id_entry.delete(0, tk.END)
        self.event_name_entry.delete(0, tk.END)
        self.event_date_entry.delete(0, tk.END)
        self.event_location_entry.delete(0, tk.END)
        self.event_description_entry.delete(0, tk.END)

    def submit(self):
        event_id = self.event_id_entry.get()
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_location = self.event_location_entry.get()
        event_description = self.event_description_entry.get()
        event = Event(event_id, event_name, event_date, event_location, event_description)
        if event_id not in allevents:
            allevents[event_id] = event
            with open("events.pkl", "ab") as file:
                pickle.dump(event, file)
            self.clearBoxes()
            print("Event added successfully. Event ID: " + event_id)
        else:
            print("Event with Event ID {} already exists.".format(event_id))

class ListEventForm:
    """Class to represent a GUI form to display all events"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Event Details")

        self.table = ttk.Treeview(self.root, columns=('Event ID', 'Event Name', 'Event Date', 'Event Location', 'Event Description'), show='headings')
        self.table.heading('Event ID', text='Event ID')
        self.table.heading('Event Name', text='Event Name')
        self.table.heading('Event Date', text='Event Date')
        self.table.heading('Event Location', text='Event Location')
        self.table.heading('Event Description', text='Event Description')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Event ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_event)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_event)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_event)
        self.delete_button.pack(pady=10)

        try:
            with open('events.pkl', 'rb') as file:
                while True:
                    event = pickle.load(file)
                    if isinstance(event, Event):
                        self.table.insert('', 'end', values=(event.event_id, event.event_name, event.event_date, event.event_location, event.event_description))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_event(self):
        event_id = self.search_entry.get()
        if event_id in allevents:
            event = allevents[event_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(event.event_id, event.event_name, event.event_date, event.event_location, event.event_description))
        else:
            print("Event with Event ID {} not found.".format(event_id))

    def edit_event(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        event_id = self.table.item(selected_item)['values'][0]

        with open("events.pkl", "rb") as file:
            events = []
            while True:
                try:
                    event = pickle.load(file)
                    if isinstance(event, Event):
                        if event.event_id == event_id:
                            events.append(event)
                        else:
                            events.append(event)
                except EOFError:
                    break

        # Open a new window or dialog box for editing event details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Event Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Event ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Event Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Event Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Event Location:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Event Description:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

        event_id_var = tk.StringVar(value=events[0].event_id)
        tk.Entry(edit_window, textvariable=event_id_var, state='disabled').grid(row=0, column=1, padx=5, pady=5)
        event_name_var = tk.StringVar(value=events[0].event_name)
        tk.Entry(edit_window, textvariable=event_name_var).grid(row=1, column=1, padx=5, pady=5)
        event_date_var = tk.StringVar(value=events[0].event_date)
        tk.Entry(edit_window, textvariable=event_date_var).grid(row=2, column=1, padx=5, pady=5)
        event_location_var = tk.StringVar(value=events[0].event_location)
        tk.Entry(edit_window, textvariable=event_location_var).grid(row=3, column=1, padx=5, pady=5)
        event_description_var = tk.StringVar(value=events[0].event_description)
        tk.Entry(edit_window, textvariable=event_description_var).grid(row=4, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the event object with the edited details
            events[0].event_name = event_name_var.get()
            events[0].event_date = event_date_var.get()
            events[0].event_location = event_location_var.get()
            events[0].event_description = event_description_var.get()

            # Rewrite the entire events list to the file with the updated event details
            with open("events.pkl", "wb") as file:
                for evt in events:
                    pickle.dump(evt, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(events[0].event_id, events[0].event_name, events[0].event_date, events[0].event_location, events[0].event_description))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=5, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_event(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        event_id = self.table.item(selected_item)['values'][0]

        with open("events.pkl", "rb") as file:
            events = []
            while True:
                try:
                    event = pickle.load(file)
                    if isinstance(event, Event) and event.event_id != event_id:
                        events.append(event)
                except EOFError:
                    break

        with open("events.pkl", "wb") as file:
            for event in events:
                pickle.dump(event, file)

        self.table.delete(selected_item)

# List to save employee details
allemployees = {}

# List to save event details
allevents = {}

# Create Object of the Employee Form
form = EmployeeForm()

# Create Object of the List Employee Form
showemployee = ListEmployeeForm()

# Create Object of the Event Form
form = EventForm()

# Create Object of the List Event Form
showevent = ListEventForm()
