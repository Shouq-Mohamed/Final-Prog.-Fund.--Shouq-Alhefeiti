import tkinter as tk
from tkinter import ttk
import pickle

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