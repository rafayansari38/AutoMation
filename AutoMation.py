# Import necessary modules
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import *
import os
from PIL import ImageTk, Image

# Connect to the SQLite database or create one if it doesn't exist
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create a table 'cars' if it doesn't exist in the database
c.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT,
        model TEXT,
        year INTEGER,
        price REAL,
        status TEXT
    )
''')
conn.commit()

# Define the main class for the GUI application
class AutoMation:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoMation")
        current_dir = os.path.dirname(__file__)

        # Set the application icon
        icon_path = os.path.join(current_dir, 'Car Icon.ico')
        self.root.iconbitmap(icon_path)

        # Load and display an image on the GUI
        image_one = os.path.join(current_dir, 'images.jpg')
        self.car_image = Image.open(image_one)
        self.car_image = self.car_image.resize((200, 200))
        self.car_image = ImageTk.PhotoImage(self.car_image)
        self.lbl_image = tk.Label(self.root, image=self.car_image)
        self.lbl_image.grid(row=0, column=6, rowspan=6, padx=10)

        # Create labels and entry widgets for car details
        self.lbl_make = tk.Label(root, text='Make:')
        self.lbl_make.grid(row=0, column=0)

        self.lbl_model = tk.Label(root, text='Model:')
        self.lbl_model.grid(row=1, column=0)

        self.lbl_year = tk.Label(root, text='Year:')
        self.lbl_year.grid(row=2, column=0)

        self.lbl_price = tk.Label(root, text='Price:')
        self.lbl_price.grid(row=3, column=0)

        self.lbl_status = tk.Label(root, text='Status:')
        self.lbl_status.grid(row=4, column=0)

        self.entry_make = tk.Entry(root)
        self.entry_make.grid(row=0, column=1)

        self.entry_model = tk.Entry(root)
        self.entry_model.grid(row=1, column=1)

        self.entry_year = tk.Entry(root)
        self.entry_year.grid(row=2, column=1)

        self.entry_price = tk.Entry(root)
        self.entry_price.grid(row=3, column=1)

        self.entry_status = tk.Entry(root)
        self.entry_status.grid(row=4, column=1)

        # Create buttons for CRUD operations and loaner vehicles
        self.btn_add = tk.Button(root, text='Add Car', command=self.add_car)
        self.btn_add.grid(row=5, column=0, pady=10)

        self.btn_remove = tk.Button(root, text='Remove Car', command=self.remove_car)
        self.btn_remove.grid(row=5, column=1, pady=10)

        self.btn_edit = tk.Button(root, text='Edit Car', command=self.edit_car)
        self.btn_edit.grid(row=5, column=2, pady=10)

        self.btn_loaners = tk.Button(root, text='Loaner Vehicles', command=self.show_loaner_vehicles)
        self.btn_loaners.grid(row=5, column=3, pady=10)

        # Create a listbox to display car inventory
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.grid(row=6, columnspan=3)

        # Populate the listbox with car data from the database
        self.refresh_listbox()

    # Method to add a new car to the inventory
    def add_car(self):
        make = self.entry_make.get()
        model = self.entry_model.get()
        year = self.entry_year.get()
        price = self.entry_price.get()
        status = self.entry_status.get()

        if make and model and year and price and status:
            c.execute("INSERT INTO cars (make, model, year, price, status) VALUES (?, ?, ?, ?, ?)",
                      (make, model, year, price, status))
            conn.commit()
            self.refresh_listbox()
            messagebox.showinfo("Success", "Car added successfully.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Method to remove a car from the inventory
    def remove_car(self):
        selected_car = self.listbox.curselection()
        if selected_car:
            car_id = self.listbox.get(selected_car)[0]
            c.execute("DELETE FROM cars WHERE id=?", (car_id,))
            conn.commit()
            self.refresh_listbox()
            messagebox.showinfo("Success", "Car removed successfully.")
        else:
            messagebox.showerror("Error", "Please select a car.")

    # Method to edit details of an existing car in the inventory
    def edit_car(self):
        selected_car = self.listbox.curselection()
        if selected_car:
            car_id = self.listbox.get(selected_car)[0]
            make = self.entry_make.get()
            model = self.entry_model.get()
            year = self.entry_year.get()
            price = self.entry_price.get()
            status = self.entry_status.get()

            if make and model and year and price and status:
                c.execute("UPDATE cars SET make=?, model=?, year=?, price=?, status=? WHERE id=?",
                          (make, model, year, price, status, car_id))
                conn.commit()
                self.refresh_listbox()
                messagebox.showinfo("Success", "Car updated successfully.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
        else:
            messagebox.showerror("Error", "Please select a car.")

    # Method to refresh the listbox with the latest car inventory
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        c.execute("SELECT * FROM cars")
        cars = c.fetchall()

        for car in cars:
            self.listbox.insert(tk.END, car)

    # Method to show the loaner vehicles in a new window
    def show_loaner_vehicles(self):
        Loaners(self.root)

    # Method to close the application
    def exit_auto(self):
        root.destroy()

# Class to display loaner vehicles in a separate window
class Loaners:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Loaner Vehicles")
        self.label = tk.Label(self.top, text="Available Loaner Vehicles:\n2019 Jeep Compass Latitude\n2021 Honda Civic EX\n2023 Hyundai Elantra Hybrid Limited\n2016 Mercedes-Benz C300\n2020 Honda CR-V LX\n2022 Mercedes-Benz GLB250\n2023 Honda Civic Sport\n2019 BMW 530e Plug-in Hybrid iPerformance\n2022 Honda CR-V Hybrid EX\n2021 Hyundai Ioniq Hybrid Blue")
        self.label.pack(padx=10, pady=10)

# Create the main Tkinter window and start the application
root = tk.Tk()
app = AutoMation(root)
root.mainloop()

# Close the database connection when the application is closed
conn.close()
