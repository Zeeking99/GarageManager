from tkinter import *
from mysql.connector import connection
from tkinter import messagebox

def init_connection():
	return connection.MySQLConnection(user='zeeking99', password='uzmasadia',
								host='127.0.0.1',
								database='garagedb')

class Main(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry("500x300")
        self.title("Garage Manager - Mechanic Portal")

        # Vehicles List
        self.list = Button(self, text="List of Vehicles", command=self.show_table)
        self.list.place(relx=0.5,rely=0.35, anchor=CENTER)

        # Change Status Button
        self.change = Button(self, text="Change Status", command=self.change_status)
        self.change.place(relx=0.5, rely=0.47, anchor=CENTER)

        # Exit Button
        self.exit = Button(self, text="Exit", command=exit)
        self.exit.place(relx=0.5, rely=0.59, anchor=CENTER)
        
    def show_table(self):
        n = Child1(self)

        n.mainloop()
        
    def change_status(self):
        n = Child2(self)

        n.mainloop()

class Child1(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)

        self.geometry("900x700")
        self.title("Vehicles Not Repaired")
        self.grab_set()
        
        self.canvas = Canvas(self)

        # Frame to grid the widgets in
        self.frame = Frame(self.canvas)

        # Horizontal Scrollbar to scroll the canvas
        self.h_wheel = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)

        # Vertical Scrollbar to scroll the canvas
        self.v_wheel = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        
        # Configuring Scrollbar
        self.canvas.configure(xscrollcommand=self.h_wheel.set, yscrollcommand=self.v_wheel.set)
        self.canvas.create_window( 0, 0, window=self.frame, anchor="center")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        cnx = init_connection()
        cursor = cnx.cursor()

        query = ("select * from customer_details")
        cursor.execute(query)

        row = cursor.fetchall()
        
        i, j = 0, 0
        sequence = cursor.column_names

        # Adding Column names
        for x in sequence:
            z = Entry(self.frame, bg="yellow")
            z.grid(row=i, column=j, sticky=NSEW)
            z.insert(0, x.title().replace('_', ' '))
            j+=1
        i=0

        # Inserting the data as rows and columns
        for x in row:
            j = 0
            for y in x:
                z = Entry(self.frame)
                z.grid(row=i+1, column=j, sticky=NSEW)
                if j == 9:
                    if row[i][j] == 0:
                        z["bg"] = "red"
                        z.insert(0, "Not Repaired")
                    else:
                        z["bg"] = "green"
                        z.insert(0, "Repaired")
                    break
                z.insert(0, row[i][j])

                j+=1
            i+=1

        self.h_wheel.pack(side=BOTTOM, fill=X)
        self.v_wheel.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=TOP, fill=X)

        cursor.close()
        cnx.close()
        
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class Child2(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.geometry("500x300")
        self.title("Change Status")
        self.grab_set()

        # Customer ID Label
        self.ID = Label(self, text="Customer ID: ")
        self.ID.place(relx=0.4, rely=0.4, anchor=CENTER)

        # Customer ID Entry
        self.ID_E = Entry(self, width=5)
        self.ID_E.place(relx=0.54, rely=0.4, anchor=CENTER)

        # Customer ID Button
        self.ID_B = Button(self, text="Enter", command=self.check)
        self.ID_B.place(relx=0.7, rely=0.4, anchor=CENTER)

    def check(self):
        cnx = init_connection()
        cursor = cnx.cursor()

        self.data = (self.ID_E.get(), )
        query = ("select status from customer_details where customer_id = %s")

        cursor.execute(query, self.data)
        self.row = cursor.fetchone()

        # Entry to Put status
        self.Status = Entry(self, width=15)
        self.Status.place(relx=0.45, rely=0.55, anchor=CENTER)

        if self.row == None:
            messagebox.showerror("Status", "Invalid ID")
        elif self.row[0]:
            self.Status.insert(0, "Repaired")
        else:
            self.Status.insert(0, "Not Repaired")

        # Button to change status
        self.Status_C = Button(self, text="Change", command=self.confirm_change)
        self.Status_C.place(relx=0.68, rely=0.55, anchor=CENTER)

    def confirm_change(self):
        cnx = init_connection()
        cursor = cnx.cursor()

        data1 = (not(self.row[0]), self.data[0])
        query = ("update customer_details set status = %s where customer_id = %s")

        cursor.execute(query, data1)
        cnx.commit()

        cursor.close()
        cnx.close()

m = Main()
m.mainloop()