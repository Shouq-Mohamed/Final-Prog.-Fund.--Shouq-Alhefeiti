#example code
import tkinter as tk
from tkinter import ttk
import pickle

class BankCustomer:
    """Class to represent details of a bank customer"""
    def __init__(self, custNumber="", custName="", custPIN="", custBalance=""):
        self.custNumber = custNumber
        self.custName = custName
        self.custPIN = custPIN
        self.custBalance = custBalance

class CustomerForm():
    '''Class to represent a GUI form to enter customer detail.'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x200")
        self.root.title("Bank Customer Form")

        self.custNumber_label = tk.Label(self.root, text="Customer Number:")
        self.custNumber_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.custNumber_entry = tk.Entry(self.root)
        self.custNumber_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.custName_label = tk.Label(self.root, text="Name:")
        self.custName_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.custName_entry = tk.Entry(self.root)
        self.custName_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.custPIN_label = tk.Label(self.root, text="PIN:")
        self.custPIN_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.custPIN_entry = tk.Entry(self.root)
        self.custPIN_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.custBalance_label = tk.Label(self.root, text="Balance:")
        self.custBalance_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.custBalance_entry = tk.Entry(self.root)
        self.custBalance_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=4, sticky=tk.E, padx=5)

        self.root.mainloop()

    def clearBoxes(self):
        self.custNumber_entry.delete(0, tk.END)
        self.custName_entry.delete(0, tk.END)
        self.custPIN_entry.delete(0, tk.END)
        self.custBalance_entry.delete(0, tk.END)

    def submit(self):
        custNumber = self.custNumber_entry.get()
        custName = self.custName_entry.get()
        custPIN = self.custPIN_entry.get()
        custBalance = self.custBalance_entry.get()
        customer = BankCustomer(custNumber, custName, custPIN, custBalance)
        if custNumber not in allcustomers:
            allcustomers[custNumber] = customer
            with open("zzbank.pick", "ab") as file:
                pickle.dump(customer, file)
            self.clearBoxes()
            print("Customer added successfully. Customer Number: " + custNumber)
        else:
            print("Customer with Customer Number {} already exists.".format(custNumber))

class ListCustomerForm:
    """Class to represent a GUI form to display all customers"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Customer Details")

        self.table = ttk.Treeview(self.root, columns=('CustNumber', 'Name', 'PIN', 'Balance'), show='headings')
        self.table.heading('CustNumber', text='Customer Number')
        self.table.heading('Name', text='Name')
        self.table.heading('PIN', text='PIN')
        self.table.heading('Balance', text='Balance')
        self.table.pack(pady=20)

        with open('zzbank.pick', 'rb') as file:
            while True:
                try:
                    customer = pickle.load(file)
                    self.table.insert('', 'end', values=(customer.custNumber, customer.custName, customer.custPIN, customer.custBalance))
                except EOFError:
                    break

        self.root.mainloop()

# Dictionary to save customer details
allcustomers = {}

# Create Object of the Customer Form
form = CustomerForm()

# Create Object of the List Customer Form
showcustomer = ListCustomerForm()
