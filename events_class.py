import tkinter as tk
from tkinter import messagebox
import pickle
import os

# Define the main application class
class EventManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Manager")

        # Event details entry fields
        self.event_id_label = tk.Label(root, text="Event ID")
        self.event_id_label.grid(row=0, column=0)
        self.event_id_entry = tk.Entry(root)
        self.event_id_entry.grid(row=0, column=1)

        self.title_label = tk.Label(root, text="Title")
        self.title_label.grid(row=1, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=1, column=1)

        self.date_label = tk.Label(root, text="Date")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        self.location_label = tk.Label(root, text="Location")
        self.location_label.grid(row=3, column=0)
        self.location_entry = tk.Entry(root)
        self.location_entry.grid(row=3, column=1)

        # Buttons for operations
        self.add_button = tk.Button(root, text="Add Event", command=self.add_event)
        self.add_button.grid(row=4, column=0)

        self.delete_button = tk.Button(root, text="Delete Event", command=self.delete_event)
        self.delete_button.grid(row=4, column=1)

        self.edit_button = tk.Button(root, text="Edit Event", command=self.edit_event)
        self.edit_button.grid(row=4, column=2)

        self.display_button = tk.Button(root, text="Display Event", command=self.display_event)
        self.display_button.grid(row=4, column=3)

        self.display_all_button = tk.Button(root, text="Display All Events", command=self.display_all_events)
        self.display_all_button.grid(row=5, column=0, columnspan=4)

        self.search_button = tk.Button(root, text="Search Event", command=self.search_event_by_id)
        self.search_button.grid(row=6, column=0, columnspan=4)

    # Method to add a new event
    def add_event(self):
        event_id = self.event_id_entry.get()
        title = self.title_entry.get()
        date = self.date_entry.get()
        location = self.location_entry.get()

        try:
            if not os.path.exists('events'):
                os.makedirs('events')

            event_data = {
                'event_id': event_id,
                'title': title,
                'date': date,
                'location': location
            }

            with open(f'events/{event_id}.pickle', 'wb') as f:
                pickle.dump(event_data, f)

            messagebox.showinfo("Success", "Event added successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Method to delete an event
    def delete_event(self):
        event_id = self.event_id_entry.get()

        try:
            os.remove(f'events/{event_id}.pickle')
            messagebox.showinfo("Success", "Event deleted successfully.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Event not found.")

    # Method to edit an event
    def edit_event(self):
        event_id = self.event_id_entry.get()
        title = self.title_entry.get()
        date = self.date_entry.get()
        location = self.location_entry.get()

        try:
            with open(f'events/{event_id}.pickle', 'rb') as f:
                event_data = pickle.load(f)

            event_data['title'] = title
            event_data['date'] = date
            event_data['location'] = location

            with open(f'events/{event_id}.pickle', 'wb') as f:
                pickle.dump(event_data, f)

            messagebox.showinfo("Success", "Event updated successfully.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Event not found.")

    # Method to display an event
    def display_event(self):
        event_id = self.event_id_entry.get()

        try:
            with open(f'events/{event_id}.pickle', 'rb') as f:
                event_data = pickle.load(f)

            messagebox.showinfo("Event Details", f"Event ID: {event_data['event_id']}\nTitle: {event_data['title']}\nDate: {event_data['date']}\nLocation: {event_data['location']}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Event not found.")

    # Method to display all events
    def display_all_events(self):
        try:
            event_files = os.listdir('events')

            if not event_files:
                messagebox.showinfo("All Events", "No events found.")
                return

            events_data = []

            for event_file in event_files:
                with open(f'events/{event_file}', 'rb') as f:
                    event_data = pickle.load(f)

                events_data.append(event_data)

            events_str = ""

            for event_data in events_data:
                events_str += f"Event ID: {event_data['event_id']}\nTitle: {event_data['title']}\nDate: {event_data['date']}\nLocation: {event_data['location']}\n\n"

            messagebox.showinfo("All Events", events_str)

        except FileNotFoundError:
            messagebox.showerror("Error", "No events found.")

    # Method to search for an event by ID
    def search_event_by_id(self):
        event_id = self.event_id_entry.get()
        if event_id:
            try:
                with open(f'events/{event_id}.pickle', 'rb') as f:
                    event_data = pickle.load(f)

                messagebox.showinfo("Event Details", f"Event ID: {event_data['event_id']}\nTitle: {event_data['title']}\nDate: {event_data['date']}\nLocation: {event_data['location']}")

            except FileNotFoundError:
                messagebox.showerror("Error", "Event not found.")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = EventManager(root)
    root.mainloop()

