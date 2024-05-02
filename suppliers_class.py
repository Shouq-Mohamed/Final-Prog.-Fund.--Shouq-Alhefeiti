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
