import tkinter as tk
from tkinter import messagebox
from data_manager import save_data, load_data

# Define classes for different entities
class Employee:
    def __init__(self, emp_id, name, department, job_title, basic_salary, age, dob, passport_details):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.dob = dob
        self.passport_details = passport_details

class Event:
    def __init__(self, event_id, type, theme, date, time, duration, venue_address, client_id, guest_list, suppliers):
        self.event_id = event_id
        self.type = type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_address = venue_address
        self.client_id = client_id
        self.guest_list = guest_list
        self.suppliers = suppliers

class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

class Guest:
    def __init__(self, guest_id, name, address, contact_details):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details

class Supplier:
    def __init__(self, supplier_id, name, address, contact_details, services):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.services = services

class Venue:
    def __init__(self, venue_id, name, address, contact, min_guests, max_guests):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact = contact
        self.min_guests = min_guests
        self.max_guests = max_guests

class EventManagementSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Management System")
        self.root.geometry("400x300")

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.add_btn = tk.Button(self.menu_frame, text="Add", command=self.add_details)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.delete_btn = tk.Button(self.menu_frame, text="Delete", command=self.delete_details)
        self.delete_btn.grid(row=0, column=1, padx=5)

        self.modify_btn = tk.Button(self.menu_frame, text="Modify", command=self.modify_details)
        self.modify_btn.grid(row=0, column=2, padx=5)

        self.display_btn = tk.Button(self.menu_frame, text="Display", command=self.display_details)
        self.display_btn.grid(row=0, column=3, padx=5)

        # Load data from pickle files
        self.load_data()

    def add_details(self):
        # Add details logic here
        pass

    def delete_details(self):
        # Delete details logic here
        pass

    def modify_details(self):
        # Modify details logic here
        pass

    def display_details(self):
        # Display details logic here
        pass

    def load_data(self):
        # Load data using data_manager.load_data function
        self.employees = data_manager.load_data("employees.pkl")
        self.events = data_manager.load_data("events.pkl")
        self.clients = data_manager.load_data("clients.pkl")
        self.guests = data_manager.load_data("guests.pkl")
        self.suppliers = data_manager.load_data("suppliers.pkl")
        self.venues = data_manager.load_data("venues.pkl")

    def save_data(self):
        # Save data using data_manager.save_data function
        data_manager.save_data(self.employees, "employees.pkl")
        data_manager.save_data(self.events, "events.pkl")
        data_manager.save_data(self.clients, "clients.pkl")
        data_manager.save_data(self.guests, "guests.pkl")
        data_manager.save_data(self.suppliers, "suppliers.pkl")
        data_manager.save_data(self.venues, "venues.pkl")

def main():
    root = tk.Tk()
    app = EventManagementSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
