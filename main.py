from tkinter import ttk
import tkinter as tk
from tkinter import *
from db import *
from tkinter import messagebox
from datetime import datetime

global count
count=0

conn=makeConnection()
createTable(conn)

root = tk.Tk()
root.title("\t\tRepository Management System")
root.geometry("1000x670")
root.configure(bg='#666666')


w=tk.Label(root, text="\tRepository Management System",font=("Roboto Bold", 40 * -1),bg='#666666')
w.grid(row = 0, column = 1, pady=10,padx=100)

style = ttk.Style()

style.theme_use("default")
style.configure("Treeview", 
	background="#777777",
	foreground="black",
	rowheight=25,
	fieldbackground="#777777")

style.map('Treeview', 
	background=[('selected', '#222222')])


# Create Treeview Frame
tree_frame =  LabelFrame(root, text="Data",bg='#666666')
tree_frame.grid(row = 1, column = 0, padx=50, pady=10, rowspan=3 ,columnspan = 7)

# Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create Treeview
my_tree = ttk.Treeview(tree_frame,height = 20, yscrollcommand=tree_scroll.set, selectmode="extended")
# Pack to the screen

my_tree.pack()

#Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("ID","Name", "Colour","Year","Qty","Last Added","Last Removed")

style = ttk.Style()
style.configure("Treeview.Heading", font=('Calibri', 17,'bold'))
style.configure("Treeview", font=('Calibri',15 ))

# Formate Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=110)
my_tree.column("Name", anchor=W, width=150)
my_tree.column("Colour", anchor=W, width=130)
my_tree.column("Year", anchor=W, width=130)
my_tree.column("Qty", anchor=W, width=110)
my_tree.column("Last Added", anchor=W, width=165)
my_tree.column("Last Removed", anchor=W, width=165)

# Create Headings 
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Colour", text="Colour", anchor=W)
my_tree.heading("Year", text="Year", anchor=W)
my_tree.heading("Qty", text="Qty", anchor=W)
my_tree.heading("Last Added", text="Last Added", anchor=W)
my_tree.heading("Last Removed", text="Last Removed", anchor=W)


my_tree.tag_configure('empty', background="#A81916")
my_tree.tag_configure('even', background="#555555")
my_tree.tag_configure('odd', background="#666666")
# Create striped row tags

def show():
    my_tree.delete(*my_tree.get_children())
    my_tree.config()
    global count
    count=0
    for  record in showStock(conn):
            if (count%2==0):
                if(record[4]==0):
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2] ,record[3], record[4],record[5],record[6]), tags=('empty','even'))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2] ,record[3], record[4],record[5],record[6]),tags=('even'))
            else:
                if(record[4]==0):
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2] ,record[3], record[4],record[5],record[6]), tags=('empty','odd'))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2] ,record[3], record[4],record[5],record[6]),tags=('odd'))
            count +=1


 
def clear_entries():
            n_entry.delete(0, END)
            c_entry.delete(0, END)
            y_entry.delete(0, END)
            q_entry.delete(0, END)
            I_entry.delete(0, END)
            
def update():
    selected = my_tree.focus()
    old_val = my_tree.item(selected, 'values')
    my_tree.tag_configure('empty', background="#A81916")
    my_tree.tag_configure('even', background="#555555")
    my_tree.tag_configure('odd', background="#666666")

    if(n_entry.get()=='' or c_entry.get()=='' or y_entry.get()==''):
        messagebox.showerror("Error", "Kindly fill in the entry boxes!")
    else:

        if(int(selected)%2==0):
            if(int(old_val[4])==0):
                my_tree.item(selected, text="",  values=(old_val[0],n_entry.get(),c_entry.get(), y_entry.get(),old_val[4],old_val[5],old_val[6]), tags=('empty'))
            else:
                my_tree.item(selected, text="",  values=(old_val[0],n_entry.get(),c_entry.get(), y_entry.get(),old_val[4],old_val[5],old_val[6]), tags=('even'))
        else:
             if(int(old_val[4])==0):
                my_tree.item(selected, text="",  values=(old_val[0],n_entry.get(),c_entry.get(), y_entry.get(),old_val[4],old_val[5],old_val[6]), tags=('empty'))
             else:
                my_tree.item(selected, text="",  values=(old_val[0],n_entry.get(),c_entry.get(), y_entry.get(),old_val[4],old_val[5],old_val[6]), tags=('odd'))

        updateAllStock(conn,n_entry.get(),c_entry.get(),y_entry.get(),old_val[0])
    clear_entries()

def delete():
            x = my_tree.selection()[0]

            selected = my_tree.focus()
            val = my_tree.item(selected, 'values')
        
            my_tree.delete(x)
            deleteStock(conn,val[0])

def edit(Id,q,t):
    for j in range(len(my_tree.get_children())):
        if(my_tree.item(j, 'values')[0]==Id):
            i=j
        else:
            pass

    my_tree.tag_configure('empty', background="#A81916")
    my_tree.tag_configure('even', background="#555555")
    my_tree.tag_configure('odd', background="#666666")
    old_val = my_tree.item(i, 'values')
    
    if(q>=0):
        if(int(old_val[4])+q==0):
            my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,t,old_val[6]), tags=('empty'))
        else:
            if(i%2==0):
                my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,t,old_val[6]), tags=('even'))
            else:
                my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,t,old_val[6]), tags=('odd'))
        clear_entries()

    else:
        if(int(old_val[4])+q==0):
            my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,old_val[5],t), tags=('empty'))
        else:
            if(i%2==0):
                my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,old_val[5],t), tags=('even'))
            else:
                my_tree.item(i, text="",  values=(old_val[0],old_val[1],old_val[2],old_val[3],int(old_val[4])+q,old_val[5],t), tags=('odd'))
        clear_entries()
        
def remove():
    Id = I_entry.get().strip()
    if(Id!=""):
        now = datetime.now()
        resp=stockPresent(conn, Id)
        if resp:
            Last_Removed=now.strftime("%m/%d/%Y, %H:%M")
            if(q_entry.get().isnumeric() or q_entry.get()==""):
                try:
                   removeStock(conn, Id, -1*int(float(q_entry.get())),Last_Removed)
                   edit(Id,-int(float(q_entry.get())),Last_Removed)
                except:
                   removeStock(conn, Id, -1,Last_Removed)
                   edit(Id,-1,Last_Removed)
            else:
                messagebox.showerror("Error", "Kindly Enter a Integer!")
            
        else:
            messagebox.showerror("Error", "This Bottle does not Exist!")

    else:
            messagebox.showerror("Error", "Kindly fill in the ID box!")
    clear_entries()

def add(): 
    Id = I_entry.get().strip()
    if(Id!=""):
        resp=stockPresent(conn, Id)
        if resp:
            now = datetime.now()
            Last_Added=now.strftime("%m/%d/%Y, %H:%M")
            if(q_entry.get().isnumeric() or q_entry.get()==""):
                try:
                    addStock(conn, Id, q_entry.get(),Last_Added)
                    edit(Id,int(float(q_entry.get())),Last_Added)
                except:
                    addStock(conn, Id, 1,Last_Added)
                    edit(Id,1,Last_Added)
            else:
                messagebox.showerror("Error", "Kindly Enter a Integer!")
                
                    
        else:
            if(n_entry.get()=='' or c_entry.get()=='' or y_entry.get()==''):
                messagebox.showerror("Error", "New Bottle! Kindly fill in the entry boxes!")
            else:
                now = datetime.now()
                if(q_entry.get()!=""):
                    name, colour, year, qty,Last_Added, Last_Removed = n_entry.get(), c_entry.get(), y_entry.get(), int(q_entry.get()), now.strftime("%m/%d/%Y, %H:%M"),""
                else:
                    name, colour, year, qty,Last_Added, Last_Removed = n_entry.get(), c_entry.get(), y_entry.get(), 1, now.strftime("%m/%d/%Y, %H:%M"),""

                insertNewStock(conn, Id, name, colour, year, qty,Last_Added,Last_Removed)

            global count      
            my_tree.tag_configure('oddrow', background="#666666")
            my_tree.tag_configure('evenrow', background="#555555")
            if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(Id ,name, colour, year, qty, Last_Added, Last_Removed), tags=('evenrow',))
            else:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=(Id ,name, colour, year, qty,Last_Added,Last_Removed), tags=('oddrow',))

            count += 1
    else:
         messagebox.showerror("Error", "Kindly fill in the ID box!")
    clear_entries()
    
def select_record():
    clear_entries() 
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
 
    n_entry.insert(0, values[1])
    c_entry.insert(0, values[2])
    y_entry.insert(0, values[3])
    I_entry.insert(0, values[0])
    
show()

data_frame =  LabelFrame(root, text="Entry",bg='#666666')
data_frame.grid(row = 4, column = 1, padx=60)

n_label =Label(data_frame, text="Name:",font=("Roboto Bold", 17 * -1),bg='#666666')
n_label.grid(row=0, column=0, padx=10, pady=10)
n_entry = Entry(data_frame)
n_entry.grid(row=0, column=1, padx=10, pady=10)

c_label = Label(data_frame, text="Colour:",font=("Roboto Bold", 17 * -1),bg='#666666')
c_label.grid(row=0, column=2, padx=10, pady=10)
c_entry = Entry(data_frame)
c_entry.grid(row=0, column=3, padx=10, pady=10)

y_label =Label(data_frame, text="Year:",font=("Roboto Bold", 17 * -1),bg='#666666')
y_label.grid(row=0, column=4, padx=10, pady=10)
y_entry = Entry(data_frame)
y_entry.grid(row=0, column=5, padx=10, pady=10)

up = Button(data_frame, text="Update", command=update,height = 1, width = 10)
up.grid(row = 0, column = 7,padx=10)

sel = Button(data_frame, text="Select", command=select_record,height = 1, width = 10)
sel.grid(row = 0, column = 6,padx=10)

Button_frame =  LabelFrame(root, text="Add/Remove",bg='#666666',)
Button_frame.grid(row = 1, column = 8, padx=0 ,pady=10)

add = Button(Button_frame, text="Add", command=add,height = 2, width = 20)
add.grid(row = 1, column = 0,padx=20,pady=15,columnspan=2)

remove = Button(Button_frame, text="Remove", command=remove ,height = 2,width = 20)
remove.grid(row = 2, column = 0,padx=20,pady=15,columnspan=2)

delete = Button(Button_frame, text="Delete`", command=delete ,height = 2,width = 20)
delete.grid(row = 3, column = 0,padx=20,pady=15,columnspan=2)

q_label =Label(Button_frame, text="Qty:",font=("Roboto Bold", 17 * -1),bg='#666666')
q_label.grid(row=5, column=0, padx=10, pady=10)
q_entry = Entry(Button_frame)
q_entry.grid(row=5, column=1, padx=10, pady=10)

I_label =Label(Button_frame, text="ID:",font=("Roboto Bold", 17 * -1),bg='#666666')
I_label.grid(row=4, column=0, padx=10, pady=10)
I_entry = Entry(Button_frame)
I_entry.grid(row=4, column=1, padx=10, pady=10)


root.mainloop()
