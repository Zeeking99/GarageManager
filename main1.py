from tkinter import *
from tkinter import messagebox
from mysql.connector import (connection, cursor)

def init_connection():
	return connection.MySQLConnection(user='zeeking99', password='uzmasadia',
								host='127.0.0.1',
								database='garagedb')

class Child(Toplevel):		# Enter Details Window
	
	def __init__(self, master, status=0):	# status parameter to determine to show info or receive it. 0 for input.
		Toplevel.__init__(self, master)

		self.geometry("700x400")
		self.title("Enter Car Details")
		self.grab_set()

		self.details = dict()

		# Customer Name 
		self.customer = Label(self, text="Customer Name: ").place(relx=0.2, rely=0.05, anchor=NE)
		self.details["customer_name"] = Entry(self)
		self.details["customer_name"].place(relx=0.45, rely=0.05, anchor=NE)

		# Car Number
		self.car_no = Label(self, text="Car Number: ").place(relx=0.61, rely=0.05, anchor=NE)
		self.details["car_state"] = Entry(self, width=2)
		self.details["car_state"].place(relx=0.65, rely=0.05, anchor=NE)

		self.details["car_dsnumber"] = Entry(self, width=2)
		self.details["car_dsnumber"].place(relx=0.69, rely=0.05, anchor=NE)

		self.details["car_number"] = Entry(self, width=4)
		self.details["car_number"].place(relx=0.754, rely=0.05, anchor=NE)	

		# Car Color
		self.colour = Label(self, text="Car Color: ").place(relx=0.2, rely=0.2, anchor=NE)
		self.details["car_color"] = Entry(self)
		self.details["car_color"].place(relx=0.45, rely=0.2, anchor=NE)	

		# Car Brand
		self.brand = Label(self, text="Car Brand: ").place(relx=0.61, rely=0.2, anchor=NE)
		self.details["car_brand"] = Entry(self)
		self.details["car_brand"] .place(relx=0.855, rely=0.2, anchor=NE)	

		# Car Model
		self.model = Label(self, text="Car Model: ").place(relx=0.2, rely=0.35, anchor=NE)
		self.details["car_model"] = Entry(self)
		self.details["car_model"] .place(relx=0.45, rely=0.35, anchor=NE)	

		# Customer Phone Number
		self.phone = Label(self, text="Phone: ").place(relx=0.61, rely=0.35, anchor=NE)
		self.details["phone"] = Entry(self)
		self.details["phone"].place(relx=0.855, rely=0.35, anchor=NE)

		# Problem Description
		self.problem = Label(self, text="Problem Description (500 Characters) ").place(relx=0.67, rely=0.45, anchor=NE)
		self.details["problem_description"] = Text(self, height=8, width=70)
		self.details["problem_description"].place(relx=0.9, rely=0.52, anchor=NE)	

		# Enter Button
		self.enter = Button(self, text="Enter", command=self.save_car_details)
		self.enter.place(relx=0.5, rely=0.95, anchor=CENTER)

		# Status Button
		if status:
			self.status_b = Button(self, text="Not Repaired", command=None, fg='red')
			self.status_b.place(relx=0.5, rely=0.95, anchor=CENTER)

			self.ID = Label(self, text="ID: ").place(relx=0.82, rely=0.05, anchor=NE)
			self.details["ID"] = Entry(self, width=4)
			self.details["ID"].place(relx=0.87, rely=0.05, anchor=NE)

			self.enter.destroy()

	def save_car_details(self):

		cnx = init_connection()
		cursor = cnx.cursor()
		
		data = (  (self.details["customer_name"].get()).split()[0], 	# first_name
			  (self.details["customer_name"].get()).split()[1], 	# second_name 
			   self.details["car_state"].get()+self.details["car_dsnumber"].get()+self.details["car_number"].get(),	# car_number
			   self.details["car_color"].get(),	# car_color
			   self.details["car_brand"].get(),	# car_brand
			   self.details["car_model"].get(),	# car_model
			   self.details["phone"].get(),	# phone
			   self.details["problem_description"].get(1.0, 1.0+500)	# description
			)

		insert_stmt = ("INSERT INTO customer_details " "(first_name, last_name, car_num, car_color, car_brand, car_model, phone, prb_desc) " "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" )

		cursor.execute(insert_stmt, data)	# Executing the command

		customer_id = str(cursor.lastrowid)
		messagebox.showinfo("Customer ID", "Your Customer ID is: "+customer_id)
		cnx.commit()	# committing data to the db

		self.clear_input()	# clearing the input from the text boxes
		
		cursor.close()	
		cnx.close()
 
	def clear_input(self):
		self.real_details = dict()

		for x in self.details:
			if x != "problem_description":
			#	self.real_details[x] = self.details[x].get()
			#	print(self.real_details[x])
				self.details[x].delete(0, END)	
			else:
			#	self.real_details[x] = self.details[x].get(1.0, 1.0+500)		
			#	print(self.real_details[x])
				self.details[x].delete(1.0, 1.0+500)	
	
	def put_data(self, data):
		self.details["ID"].insert(0, data[0])
		self.details["customer_name"].insert(0, data[1]+" "+data[2])
		self.details["car_state"].insert(0, data[3][0:2])
		self.details["car_dsnumber"].insert(0, data[3][2:4])
		self.details["car_number"].insert(0, data[3][4:])
		self.details["car_color"].insert(0, data[4])
		self.details["car_brand"].insert(0, data[5])
		self.details["car_model"].insert(0, data[6])
		self.details["phone"].insert(0, data[7])
		self.details["problem_description"].insert(1.0, data[8])
		
		if data[-1:][0]:	# Checking the status of a vehicle
			self.status_b["text"] = "Repaired"
			self.status_b["fg"] = "green"

class Child1(Toplevel):

	def __init__(self, master):
		Toplevel.__init__(self, master)

		self.title("Get Status")
		self.geometry('400x200')
		self.grab_set()

		self.details = {}

		# Customer ID
		self.ID = Label(self, text="Enter Customer ID: ")
		self.ID.place(relx=0.4, rely=0.5, anchor=CENTER)
		self.details["ID"] = Entry(self, width=10)
		self.details["ID"].place(relx=0.68, rely=0.5, anchor=CENTER)

		# Enter Button
		self.enter = Button(self, text="Enter", command=self.get_status)
		self.enter.place(relx=0.5, rely=0.7, anchor=CENTER)

	def get_status(self):
		cnx = init_connection()
		cursor = cnx.cursor()

		data = tuple(self.details["ID"].get())

		retr_stmt = ( "SELECT * FROM customer_details WHERE customer_id = %s" )

		cursor.execute(retr_stmt, (self.details["ID"].get(), ))
		row = cursor.fetchone()

		cursor.close()
		cnx.close()

		if row == None:
			messagebox.showerror("Status", "Invalid ID")
		else:
			print(row[-1:][0])
			self.show_details(row)

	def show_details(self, row):
		info = Child(self, 1)		# Initiating a Child object to display information
		info.put_data(row)

		info.mainloop()

class Main(Tk):		# Class of Main Window

	def __init__(self):
		Tk.__init__(self)
		self.title("Garage Manager 2021")
		self.geometry('500x300')

		# Enter Details Button
		self.enter = Button(self, text="Enter Car Details", command=self.give_details)
		self.enter.place(relx=0.5, rely=0.35, anchor=CENTER)

		# Get Details Button
		self.get = Button(self, text="Get Status", command=self.get_status)
		self.get.place(relx=0.5, rely=0.5, anchor=CENTER)

		# Quit Button
		self.quit = Button(self, text="Exit", command=exit).place(relx=0.5, rely=0.65, anchor=CENTER)

	def give_details(self):		# Function for initiating Enter Details Window
		n = Child(self)

		n.mainloop()

	def get_status(self):
		n = Child1(self)

		n.mainloop()

m = Main()

m.mainloop()