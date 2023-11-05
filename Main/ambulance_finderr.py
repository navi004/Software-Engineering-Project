import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg , simpledialog
import mysql.connector
from geolocator import get_lat_long_for_address
from distance_finder import latlon_distance_finder

DB_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Naveen@55533",
    database = "ambulance_database"
)

cursor = DB_connection.cursor()

def Menu():
    global L0,B1,B2,B3,B4
    window.geometry('400x400')

    L0 = Label(window,text = "MENU",font = ("Times New Roman",60),bg = "white",fg = "Red")
    B0 = Button(window,text = "Enter Your Details",command = TakeUserDetails,width = 30, bg ="lightgreen", fg = "brown")
    B1 = Button(window,text = "My Profile",command = MyProfile,width = 30,bg = "lightgreen",fg="brown")
    B2 = Button(window,text = "Search Nearest Ambulance",command = Search_Nearest_Ambulance,width = 30,bg = "lightgreen",fg="brown")
    B3 = Button(window,text = "Help",command = help,width = 30,bg = "lightgreen",fg="brown")
    B4 = Button(window,text = "Exit",command = window.destroy,width = 30,bg = "lightgreen",fg="brown")

    L0.pack()
    B0.pack()
    B1.pack()
    B2.pack()
    B3.pack()
    B4.pack()

def help():
        help_txt = """
        How to find the nearest ambulance:
        1. Click the 'My Profile' button and enter your name and mobile number
        2.Click the 'insert data' button. 
        3.Click the 'Search Nearest Ambulance' button.
        4.Enter your current location address when prompted.
        5.It is necessary to enter the pincode of the location.
        6.In case of emergency, call 100.
        """
        msg.showinfo("Help",help_txt)

def Insert_Data():
    name = name_entry.get()
    mobile = mobile_entry.get()

    insert_query = "INSERT INTO user_profiles(name, mobile) VALUES (%s, %s)"
    cursor.execute(insert_query, (name, mobile))
    DB_connection.commit()

    name_label.destroy()
    name_entry.destroy()
    mobile_label.destroy()
    mobile_entry.destroy()
    insert_button.destroy()

def TakeUserDetails():
        global name_label,mobile_label,name_entry,mobile_entry,insert_button

        name_label = tk.Label(window, text = "Name:")
        name_label.pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        mobile_label = tk.Label(window,text = "Mobile:")
        mobile_label.pack()
        mobile_entry = tk.Entry(window)
        mobile_entry.pack()

        insert_button = tk.Button(window, text = "Insert Data", command = Insert_Data)
        insert_button.pack()

def MyProfile():
    cursor.execute("SELECT name, mobile FROM user_profiles ORDER BY id DESC LIMIT 1")
    user_data = cursor.fetchone()

    if user_data:
        name, mobile = user_data
        profile_info = f"Name: {name}\nMobile: {mobile}"
        msg.showinfo("My Profile", profile_info)
    else:
        msg.showinfo("My Profile", "No user profile found. Please enter your details first.")

def Search_Nearest_Ambulance():
    location_address = simpledialog.askstring("Enter Location", "Enter your current location address:")
    if location_address:
        try:
            # Get latitude and longitude for the user's address
            latitude, longitude = get_lat_long_for_address(location_address)

            if latitude is not None and longitude is not None:
    
                cursor.execute("SELECT driver_id, name, location_lat, location_lon, phone_number,hospital_id FROM ambulance_drivers")
                ambulance_drivers = cursor.fetchall()

                cursor.execute("SELECT hospital_id, h_name, location_lat, location_lon FROM hospitals")
                hospitals = cursor.fetchall()

                # Initialize variables to track the nearest ambulance and hospital
                nearest_ambulance = None
                nearest_ambulance_distance = float('inf')
                nearest_hospital = None
                nearest_hospital_distance = float('inf')

                for driver in ambulance_drivers:
                    driver_id, name, location_lat, location_lon, phone_number,hospital_id = driver
                    distance = latlon_distance_finder(latitude, longitude, location_lat, location_lon)
                    if distance < nearest_ambulance_distance:
                        nearest_ambulance_distance = distance
                        nearest_ambulance = driver_id, name, phone_number

                for hospital in hospitals:
                    hospital_id, h_name, location_lat, location_lon = hospital
                    distance = latlon_distance_finder(latitude, longitude, location_lat, location_lon)
                    if distance < nearest_hospital_distance:
                        nearest_hospital_distance = distance
                        nearest_hospital = hospital_id, h_name

                if nearest_ambulance and nearest_hospital:
                    result_text = f"Nearest Ambulance:\nDriver ID: {nearest_ambulance[0]}\nName: {nearest_ambulance[1]}\nPhone: {nearest_ambulance[2]}\n\n"
                    result_text += f"Nearest Hospital:\nHospital ID: {nearest_hospital[0]}\nName: {nearest_hospital[1]}"
                    msg.showinfo("Nearest Ambulance and Hospital", result_text)
                else:
                    msg.showinfo("Error", "No ambulance or hospital found.")
            else:
                msg.showinfo("Error", "Location not found. Please check the address.")
        except Exception as e:
            msg.showinfo("Error", f"An error occurred: {str(e)}")
    else:
        msg.showinfo("Error", "Please enter a location address.")

window = tk.Tk()
window.title("Nearest Ambulance Finder")

window.configure(bg = "LightBlue")
Menu()
window.mainloop()