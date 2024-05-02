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