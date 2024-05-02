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

            # Insert the new event into the table
            self.table.insert('', 'end', values=(
            event.event_id, event.event_name, event.event_date, event.event_location, event.event_description))

            self.clearBoxes()
            print("Event added successfully. Event ID: " + event_id)
        else:
            print("Event with Event ID {} already exists.".format(event_id))

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


class Client:
    """Class to represent details of a client"""
    def __init__(self, name="", client_id="", email="", phone="", company="", address=""):
        self.name = name
        self.client_id = client_id
        self.email = email
        self.phone = phone
        self.company = company
        self.address = address

class ClientForm():
    '''Class to represent a GUI form to enter client details.'''
    def __init__(self, table):
        self.table = table  # Pass the table from ListClientForm
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Client Form")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.client_id_label = tk.Label(self.root, text="Client ID:")
        self.client_id_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.client_id_entry = tk.Entry(self.root)
        self.client_id_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.company_label = tk.Label(self.root, text="Company:")
        self.company_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.company_entry = tk.Entry(self.root)
        self.company_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=6, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.name_entry.delete(0, tk.END)
        self.client_id_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def submit(self):
        client_id = self.client_id_entry.get()
        client_name = self.name_entry.get()
        client_email = self.email_entry.get()
        client_phone = self.phone_entry.get()
        client_company = self.company_entry.get()
        client_address = self.address_entry.get()
        client = Client(client_name, client_id, client_email, client_phone, client_company, client_address)
        if client_id not in all_clients:
            all_clients[client_id] = client
            with open("clients.pkl", "ab") as file:
                pickle.dump(client, file)

            # Insert the new client into the table (accessed via self.table)
            self.table.insert('', 'end', values=(
            client.client_id, client.name, client.email, client.phone, client.company, client.address))

            self.clearBoxes()
            print("Client added successfully. Client ID: " + client_id)
        else:
            print("Client with Client ID {} already exists.".format(client_id))

class ListClientForm:
    """Class to represent a GUI form to display all clients"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Client Details")

        self.table = ttk.Treeview(self.root, columns=('Client ID', 'Name', 'Email', 'Phone', 'Company', 'Address'), show='headings')
        self.table.heading('Client ID', text='Client ID')
        self.table.heading('Name', text='Name')
        self.table.heading('Email', text='Email')
        self.table.heading('Phone', text='Phone')
        self.table.heading('Company', text='Company')
        self.table.heading('Address', text='Address')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Client ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_client)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_client)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_client)
        self.delete_button.pack(pady=10)

        try:
            with open('clients.pkl', 'rb') as file:
                while True:
                    client = pickle.load(file)
                    if isinstance(client, Client):
                        self.table.insert('', 'end', values=(client.client_id, client.name, client.email, client.phone, client.company, client.address))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_client(self):
        client_id = self.search_entry.get()
        if client_id in all_clients:
            client = all_clients[client_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(client.client_id, client.name, client.email, client.phone, client.company, client.address))
        else:
            print("Client with Client ID {} not found.".format(client_id))

    def edit_client(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        client_id = self.table.item(selected_item)['values'][0]

        with open("clients.pkl", "rb") as file:
            clients = []
            while True:
                try:
                    client = pickle.load(file)
                    if isinstance(client, Client):
                        if client.client_id == client_id:
                            clients.append(client)
                        else:
                            clients.append(client)
                except EOFError:
                    break

        # Open a new window or dialog box for editing client details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Client Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Client ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Company:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        name_var = tk.StringVar(value=clients[0].name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        client_id_var = tk.StringVar(value=clients[0].client_id)
        tk.Entry(edit_window, textvariable=client_id_var, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        email_var = tk.StringVar(value=clients[0].email)
        tk.Entry(edit_window, textvariable=email_var).grid(row=2, column=1, padx=5, pady=5)
        phone_var = tk.StringVar(value=clients[0].phone)
        tk.Entry(edit_window, textvariable=phone_var).grid(row=3, column=1, padx=5, pady=5)
        company_var = tk.StringVar(value=clients[0].company)
        tk.Entry(edit_window, textvariable=company_var).grid(row=4, column=1, padx=5, pady=5)
        address_var = tk.StringVar(value=clients[0].address)
        tk.Entry(edit_window, textvariable=address_var).grid(row=5, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the client object with the edited details
            clients[0].name = name_var.get()
            clients[0].email = email_var.get()
            clients[0].phone = phone_var.get()
            clients[0].company = company_var.get()
            clients[0].address = address_var.get()

            # Rewrite the entire clients list to the file with the updated client details
            with open("clients.pkl", "wb") as file:
                for cli in clients:
                    pickle.dump(cli, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(clients[0].client_id, clients[0].name, clients[0].email, clients[0].phone, clients[0].company, clients[0].address))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_client(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        client_id = self.table.item(selected_item)['values'][0]

        with open("clients.pkl", "rb") as file:
            clients = []
            while True:
                try:
                    client = pickle.load(file)
                    if isinstance(client, Client) and client.client_id != client_id:
                        clients.append(client)
                except EOFError:
                    break

        with open("clients.pkl", "wb") as file:
            for client in clients:
                pickle.dump(client, file)

        self.table.delete(selected_item)

# List to save client details
all_clients = {}

# Create Object of the Client Form first
form = ClientForm(None)

# Create Object of the List Client Form after, passing the table from ClientForm
show_clients = ListClientForm()

class Guest:
    """Class to represent details of a guest"""
    def __init__(self, name="", guest_id="", email="", phone="", company="", address=""):
        self.name = name
        self.guest_id = guest_id
        self.email = email
        self.phone = phone
        self.company = company
        self.address = address

class GuestForm():
    '''Class to represent a GUI form to enter guest details.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Guest Form")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.guest_id_label = tk.Label(self.root, text="Guest ID:")
        self.guest_id_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.guest_id_entry = tk.Entry(self.root)
        self.guest_id_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.company_label = tk.Label(self.root, text="Company:")
        self.company_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.company_entry = tk.Entry(self.root)
        self.company_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=6, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.name_entry.delete(0, tk.END)
        self.guest_id_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def submit(self):
        guest_id = self.guest_id_entry.get()
        guest_name = self.name_entry.get()
        guest_email = self.email_entry.get()
        guest_phone = self.phone_entry.get()
        guest_company = self.company_entry.get()
        guest_address = self.address_entry.get()
        guest = Guest(guest_name, guest_id, guest_email, guest_phone, guest_company, guest_address)
        if guest_id not in all_guests:
            all_guests[guest_id] = guest
            with open("guests.pkl", "ab") as file:
                pickle.dump(guest, file)

            # Insert the new guest into the table
            self.table.insert('', 'end', values=(
            guest.guest_id, guest.name, guest.email, guest.phone, guest.company, guest.address))

            self.clearBoxes()
            print("Guest added successfully. Guest ID: " + guest_id)
        else:
            print("Guest with Guest ID {} already exists.".format(guest_id))

class ListGuestForm:
    """Class to represent a GUI form to display all guests"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Guest Details")

        self.table = ttk.Treeview(self.root, columns=('Guest ID', 'Name', 'Email', 'Phone', 'Company', 'Address'), show='headings')
        self.table.heading('Guest ID', text='Guest ID')
        self.table.heading('Name', text='Name')
        self.table.heading('Email', text='Email')
        self.table.heading('Phone', text='Phone')
        self.table.heading('Company', text='Company')
        self.table.heading('Address', text='Address')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Guest ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_guest)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_guest)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_guest)
        self.delete_button.pack(pady=10)

        try:
            with open('guests.pkl', 'rb') as file:
                while True:
                    guest = pickle.load(file)
                    if isinstance(guest, Guest):
                        self.table.insert('', 'end', values=(guest.guest_id, guest.name, guest.email, guest.phone, guest.company, guest.address))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_guest(self):
        guest_id = self.search_entry.get()
        if guest_id in all_guests:
            guest = all_guests[guest_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(guest.guest_id, guest.name, guest.email, guest.phone, guest.company, guest.address))
        else:
            print("Guest with Guest ID {} not found.".format(guest_id))

    def edit_guest(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        guest_id = self.table.item(selected_item)['values'][0]

        with open("guests.pkl", "rb") as file:
            guests = []
            while True:
                try:
                    guest = pickle.load(file)
                    if isinstance(guest, Guest):
                        if guest.guest_id == guest_id:
                            guests.append(guest)
                        else:
                            guests.append(guest)
                except EOFError:
                    break

        # Open a new window or dialog box for editing guest details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Guest Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Guest ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Company:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        name_var = tk.StringVar(value=guests[0].name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        guest_id_var = tk.StringVar(value=guests[0].guest_id)
        tk.Entry(edit_window, textvariable=guest_id_var, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        email_var = tk.StringVar(value=guests[0].email)
        tk.Entry(edit_window, textvariable=email_var).grid(row=2, column=1, padx=5, pady=5)
        phone_var = tk.StringVar(value=guests[0].phone)
        tk.Entry(edit_window, textvariable=phone_var).grid(row=3, column=1, padx=5, pady=5)
        company_var = tk.StringVar(value=guests[0].company)
        tk.Entry(edit_window, textvariable=company_var).grid(row=4, column=1, padx=5, pady=5)
        address_var = tk.StringVar(value=guests[0].address)
        tk.Entry(edit_window, textvariable=address_var).grid(row=5, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the guest object with the edited details
            guests[0].name = name_var.get()
            guests[0].email = email_var.get()
            guests[0].phone = phone_var.get()
            guests[0].company = company_var.get()
            guests[0].address = address_var.get()

            # Rewrite the entire guests list to the file with the updated guest details
            with open("guests.pkl", "wb") as file:
                for gue in guests:
                    pickle.dump(gue, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(guests[0].guest_id, guests[0].name, guests[0].email, guests[0].phone, guests[0].company, guests[0].address))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_guest(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        guest_id = self.table.item(selected_item)['values'][0]

        with open("guests.pkl", "rb") as file:
            guests = []
            while True:
                try:
                    guest = pickle.load(file)
                    if isinstance(guest, Guest) and guest.guest_id != guest_id:
                        guests.append(guest)
                except EOFError:
                    break

        with open("guests.pkl", "wb") as file:
            for guest in guests:
                pickle.dump(guest, file)

        self.table.delete(selected_item)

# List to save guest details
all_guests = {}

# Create Object of the Guest Form
form = GuestForm()

# Create Object of the List Guest Form
show_guests = ListGuestForm()


import tkinter as tk
from tkinter import ttk
import pickle

class Supplier:
    """Class to represent details of a supplier"""
    def __init__(self, name="", supplier_id="", email="", phone="", company="", address=""):
        self.name = name
        self.supplier_id = supplier_id
        self.email = email
        self.phone = phone
        self.company = company
        self.address = address

class SupplierForm():
    '''Class to represent a GUI form to enter supplier details.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Supplier Form")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.supplier_id_label = tk.Label(self.root, text="Supplier ID:")
        self.supplier_id_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.supplier_id_entry = tk.Entry(self.root)
        self.supplier_id_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.company_label = tk.Label(self.root, text="Company:")
        self.company_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.company_entry = tk.Entry(self.root)
        self.company_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=6, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.name_entry.delete(0, tk.END)
        self.supplier_id_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def submit(self):
        supplier_id = self.supplier_id_entry.get()
        supplier_name = self.name_entry.get()
        supplier_email = self.email_entry.get()
        supplier_phone = self.phone_entry.get()
        supplier_company = self.company_entry.get()
        supplier_address = self.address_entry.get()
        supplier = Supplier(supplier_name, supplier_id, supplier_email, supplier_phone, supplier_company, supplier_address)
        if supplier_id not in all_suppliers:
            all_suppliers[supplier_id] = supplier
            with open("suppliers.pkl", "ab") as file:
                pickle.dump(supplier, file)

            # Insert the new supplier into the table
            self.table.insert('', 'end', values=(
            supplier.supplier_id, supplier.name, supplier.email, supplier.phone, supplier.company, supplier.address))

            self.clearBoxes()
            print("Supplier added successfully. Supplier ID: " + supplier_id)
        else:
            print("Supplier with Supplier ID {} already exists.".format(supplier_id))

class ListSupplierForm:
    """Class to represent a GUI form to display all suppliers"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Supplier Details")

        self.table = ttk.Treeview(self.root, columns=('Supplier ID', 'Name', 'Email', 'Phone', 'Company', 'Address'), show='headings')
        self.table.heading('Supplier ID', text='Supplier ID')
        self.table.heading('Name', text='Name')
        self.table.heading('Email', text='Email')
        self.table.heading('Phone', text='Phone')
        self.table.heading('Company', text='Company')
        self.table.heading('Address', text='Address')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Supplier ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_supplier)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_supplier)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_supplier)
        self.delete_button.pack(pady=10)

        try:
            with open('suppliers.pkl', 'rb') as file:
                while True:
                    supplier = pickle.load(file)
                    if isinstance(supplier, Supplier):
                        self.table.insert('', 'end', values=(supplier.supplier_id, supplier.name, supplier.email, supplier.phone, supplier.company, supplier.address))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_supplier(self):
        supplier_id = self.search_entry.get()
        if supplier_id in all_suppliers:
            supplier = all_suppliers[supplier_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(supplier.supplier_id, supplier.name, supplier.email, supplier.phone, supplier.company, supplier.address))
        else:
            print("Supplier with Supplier ID {} not found.".format(supplier_id))

    def edit_supplier(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        supplier_id = self.table.item(selected_item)['values'][0]

        with open("suppliers.pkl", "rb") as file:
            suppliers = []
            while True:
                try:
                    supplier = pickle.load(file)
                    if isinstance(supplier, Supplier):
                        if supplier.supplier_id == supplier_id:
                            suppliers.append(supplier)
                        else:
                            suppliers.append(supplier)
                except EOFError:
                    break

        # Open a new window or dialog box for editing supplier details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Supplier Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Supplier ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Company:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        name_var = tk.StringVar(value=suppliers[0].name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        supplier_id_var = tk.StringVar(value=suppliers[0].supplier_id)
        tk.Entry(edit_window, textvariable=supplier_id_var, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        email_var = tk.StringVar(value=suppliers[0].email)
        tk.Entry(edit_window, textvariable=email_var).grid(row=2, column=1, padx=5, pady=5)
        phone_var = tk.StringVar(value=suppliers[0].phone)
        tk.Entry(edit_window, textvariable=phone_var).grid(row=3, column=1, padx=5, pady=5)
        company_var = tk.StringVar(value=suppliers[0].company)
        tk.Entry(edit_window, textvariable=company_var).grid(row=4, column=1, padx=5, pady=5)
        address_var = tk.StringVar(value=suppliers[0].address)
        tk.Entry(edit_window, textvariable=address_var).grid(row=5, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the supplier object with the edited details
            suppliers[0].name = name_var.get()
            suppliers[0].email = email_var.get()
            suppliers[0].phone = phone_var.get()
            suppliers[0].company = company_var.get()
            suppliers[0].address = address_var.get()

            # Rewrite the entire suppliers list to the file with the updated supplier details
            with open("suppliers.pkl", "wb") as file:
                for sup in suppliers:
                    pickle.dump(sup, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(suppliers[0].supplier_id, suppliers[0].name, suppliers[0].email, suppliers[0].phone, suppliers[0].company, suppliers[0].address))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_supplier(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        supplier_id = self.table.item(selected_item)['values'][0]

        with open("suppliers.pkl", "rb") as file:
            suppliers = []
            while True:
                try:
                    supplier = pickle.load(file)
                    if isinstance(supplier, Supplier) and supplier.supplier_id != supplier_id:
                        suppliers.append(supplier)
                except EOFError:
                    break

        with open("suppliers.pkl", "wb") as file:
            for supplier in suppliers:
                pickle.dump(supplier, file)

        self.table.delete(selected_item)

# List to save supplier details
all_suppliers = {}

# Create Object of the Supplier Form
form = SupplierForm()

# Create Object of the List Supplier Form
show_suppliers = ListSupplierForm()

import tkinter as tk
from tkinter import ttk
import pickle

class Venue:
    """Class to represent details of a venue"""
    def __init__(self, name="", venue_id="", location="", capacity=0, facilities=""):
        self.name = name
        self.venue_id = venue_id
        self.location = location
        self.capacity = capacity
        self.facilities = facilities

class VenueForm():
    '''Class to represent a GUI form to enter venue details.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("Venue Form")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.venue_id_label = tk.Label(self.root, text="Venue ID:")
        self.venue_id_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.venue_id_entry = tk.Entry(self.root)
        self.venue_id_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.location_label = tk.Label(self.root, text="Location:")
        self.location_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.location_entry = tk.Entry(self.root)
        self.location_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.capacity_label = tk.Label(self.root, text="Capacity:")
        self.capacity_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.capacity_entry = tk.Entry(self.root)
        self.capacity_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.facilities_label = tk.Label(self.root, text="Facilities:")
        self.facilities_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.facilities_entry = tk.Entry(self.root)
        self.facilities_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=5, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.name_entry.delete(0, tk.END)
        self.venue_id_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.facilities_entry.delete(0, tk.END)

    def submit(self):
        venue_id = self.venue_id_entry.get()
        venue_name = self.name_entry.get()
        venue_location = self.location_entry.get()
        venue_capacity = int(self.capacity_entry.get())
        venue_facilities = self.facilities_entry.get()
        venue = Venue(venue_name, venue_id, venue_location, venue_capacity, venue_facilities)
        if venue_id not in all_venues:
            all_venues[venue_id] = venue
            with open("venues.pkl", "ab") as file:
                pickle.dump(venue, file)

            # Insert the new venue into the table
            self.table.insert('', 'end', values=(
            venue.venue_id, venue.name, venue.location, venue.capacity, venue.facilities))

            self.clearBoxes()
            print("Venue added successfully. Venue ID: " + venue_id)
        else:
            print("Venue with Venue ID {} already exists.".format(venue_id))

class ListVenueForm:
    """Class to represent a GUI form to display all venues"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Venue Details")

        self.table = ttk.Treeview(self.root, columns=('Venue ID', 'Name', 'Location', 'Capacity', 'Facilities'), show='headings')
        self.table.heading('Venue ID', text='Venue ID')
        self.table.heading('Name', text='Name')
        self.table.heading('Location', text='Location')
        self.table.heading('Capacity', text='Capacity')
        self.table.heading('Facilities', text='Facilities')
        self.table.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Search by Venue ID:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_venue)
        self.search_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_venue)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_venue)
        self.delete_button.pack(pady=10)

        try:
            with open('venues.pkl', 'rb') as file:
                while True:
                    venue = pickle.load(file)
                    if isinstance(venue, Venue):
                        self.table.insert('', 'end', values=(venue.venue_id, venue.name, venue.location, venue.capacity, venue.facilities))
        except FileNotFoundError:
            pass
        except EOFError:
            pass

        self.root.mainloop()

    def search_venue(self):
        venue_id = self.search_entry.get()
        if venue_id in all_venues:
            venue = all_venues[venue_id]
            self.table.delete(*self.table.get_children())  # Clear table
            self.table.insert('', 'end', values=(venue.venue_id, venue.name, venue.location, venue.capacity, venue.facilities))
        else:
            print("Venue with Venue ID {} not found.".format(venue_id))

    def edit_venue(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        venue_id = self.table.item(selected_item)['values'][0]

        with open("venues.pkl", "rb") as file:
            venues = []
            while True:
                try:
                    venue = pickle.load(file)
                    if isinstance(venue, Venue):
                        if venue.venue_id == venue_id:
                            venues.append(venue)
                        else:
                            venues.append(venue)
                except EOFError:
                    break

        # Open a new window or dialog box for editing venue details
        edit_window = tk.Toplevel()
        edit_window.title("Edit Venue Details")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Venue ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Location:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Capacity:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(edit_window, text="Facilities:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

        name_var = tk.StringVar(value=venues[0].name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        venue_id_var = tk.StringVar(value=venues[0].venue_id)
        tk.Entry(edit_window, textvariable=venue_id_var, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        location_var = tk.StringVar(value=venues[0].location)
        tk.Entry(edit_window, textvariable=location_var).grid(row=2, column=1, padx=5, pady=5)
        capacity_var = tk.IntVar(value=venues[0].capacity)
        tk.Entry(edit_window, textvariable=capacity_var).grid(row=3, column=1, padx=5, pady=5)
        facilities_var = tk.StringVar(value=venues[0].facilities)
        tk.Entry(edit_window, textvariable=facilities_var).grid(row=4, column=1, padx=5, pady=5)

        # Function to save the edited details
        def save_edits():
            # Update the venue object with the edited details
            venues[0].name = name_var.get()
            venues[0].location = location_var.get()
            venues[0].capacity = capacity_var.get()
            venues[0].facilities = facilities_var.get()

            # Rewrite the entire venues list to the file with the updated venue details
            with open("venues.pkl", "wb") as file:
                for ven in venues:
                    pickle.dump(ven, file)

            # Update the table with the edited details
            self.table.item(selected_item, values=(venues[0].venue_id, venues[0].name, venues[0].location, venues[0].capacity, venues[0].facilities))

            edit_window.destroy()  # Close the edit window

        # Button to save the edited details
        tk.Button(edit_window, text="Save", command=save_edits).grid(row=5, column=1, padx=5, pady=10, sticky=tk.E)

    def delete_venue(self):
        selected_item = self.table.selection()
        if len(selected_item) == 0:
            return
        venue_id = self.table.item(selected_item)['values'][0]

        with open("venues.pkl", "rb") as file:
            venues = []
            while True:
                try:
                    venue = pickle.load(file)
                    if isinstance(venue, Venue) and venue.venue_id != venue_id:
                        venues.append(venue)
                except EOFError:
                    break

        with open("venues.pkl", "wb") as file:
            for venue in venues:
                pickle.dump(venue, file)

        self.table.delete(selected_item)

# List to save venue details
all_venues = {}

# Create Object of the Venue Form
form = VenueForm()

# Create Object of the List Venue Form
show_venues = ListVenueForm()
