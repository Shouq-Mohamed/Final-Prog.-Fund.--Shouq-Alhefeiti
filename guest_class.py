import tkinter as tk
from tkinter import ttk
import pickle

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