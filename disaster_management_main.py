import tkinter as tk
from tkinter import messagebox
import mysql.connector
import time
import matplotlib.pyplot as plt

inventory = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="varshin",
    database="inventory"
)
mycur = inventory.cursor()

def main():
    global mainroot
    mainroot = tk.Tk()
    mainroot.title("Disaster Management System")
    mainroot.geometry("400x300")
    
    admin_btn = tk.Button(mainroot, text="Admin", fg="black", width=30, command=admin)
    user_btn = tk.Button(mainroot, text="User", fg="black", width=30, command=userp)
    
    admin_btn.pack(pady=20)
    user_btn.pack(pady=20)
    
    mainroot.mainloop()

def admin():
    global mainroot
    mainroot.withdraw()
    adminw = tk.Toplevel(mainroot)
    adminw.geometry("400x400")
    adminw.title("Admin Verification")
    
    tk.Label(adminw, text="Enter Name:").pack(pady=5)
    name = tk.Entry(adminw)
    name.pack(pady=5)
    
    tk.Label(adminw, text="Enter ID:").pack(pady=5)
    id_admin = tk.Entry(adminw)
    id_admin.pack(pady=5)
    
    tk.Label(adminw, text="Enter Password:").pack(pady=5)
    passwd = tk.Entry(adminw, show="*")
    passwd.pack(pady=5)
    
    submit = tk.Button(adminw, text="Submit", width=30, command=lambda: check_admin(name, id_admin, passwd, adminw))
    submit.pack(pady=10)

def check_admin(name, id_admin, passwd, adminw):
    query = "SELECT * FROM admin WHERE id=%s AND passwd=%s"
    mycur.execute(query, (id_admin.get(), passwd.get()))
    data = mycur.fetchone()
    
    if data:
        messagebox.showinfo("Success", "Login Successful!")
        admin_portal(adminw)
    else:
        messagebox.showerror("Error", "Invalid Credentials")
        adminw.destroy()
        mainroot.deiconify()

def admin_portal(adminw):
    adminw.withdraw()
    adminpw = tk.Toplevel(adminw)
    adminpw.geometry("400x400")
    adminpw.title("Admin Panel")
    
    tk.Button(adminpw, text="Update Data", width=30, command=lambda: update_database(adminpw)).pack(pady=5)
    tk.Button(adminpw, text="Show Inventory", width=30, command=show_inventory).pack(pady=5)
    tk.Button(adminpw, text="Show Requests", width=30, command=show_requests).pack(pady=5)
    tk.Button(adminpw, text="Process Requests", width=30, command=process_requests).pack(pady=5)
    tk.Button(adminpw, text="Logout", width=30, command=lambda: logout(adminpw, adminw)).pack(pady=5)

def update_database(adminpw):
    updatepw = tk.Toplevel(adminpw)
    updatepw.geometry("400x300")
    
    tk.Label(updatepw, text="Enter Item:").pack(pady=5)
    item = tk.Entry(updatepw)
    item.pack(pady=5)
    
    tk.Label(updatepw, text="Enter Quantity:").pack(pady=5)
    quantity = tk.Entry(updatepw)
    quantity.pack(pady=5)
    
    tk.Button(updatepw, text="Update", command=lambda: update_inventory(item, quantity, updatepw)).pack(pady=10)

def update_inventory(item, quant, updatepw):
    try:
        t=item.get()
        q=int(quant.get())
        mycur.execute("update main_inventory set quantity=quantity+ %s where item=%s",(q,t))
        inventory.commit()
        messagebox.showinfo("Success", "Inventory Updated")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        updatepw.destroy()

def show_inventory():
    mycur.execute("SELECT * FROM main_inventory")
    data = mycur.fetchall()
    
    inv_window = tk.Toplevel()
    inv_window.geometry("400x300")
    inv_window.title("Inventory")
    
    for row in data:
        tk.Label(inv_window, text=str(row)).pack()

def show_requests():
    mycur.execute("SELECT * FROM request")
    data = mycur.fetchall()
    
    req_window = tk.Toplevel()
    req_window.geometry("400x300")
    req_window.title("Requests")
    
    for row in data:
        tk.Label(req_window, text=str(row)).pack()

def process_requests():
    mycur.execute("SELECT * FROM request ORDER BY time")
    requests = mycur.fetchall()
    
    fifo_times = []
    priority_times = []
    location_times = []
    
    for request in requests:
        sent_time = request[6]
        finish_time = time.time()
        process_time = finish_time - sent_time
        
        fifo_times.append(process_time)
        
        if request[5] == "urgent":
            priority_times.append(process_time)
        
        if request[3] == "high_priority_location":
            location_times.append(process_time)
    
    avg_fifo = sum(fifo_times) / len(fifo_times) if fifo_times else 0
    avg_priority = sum(priority_times) / len(priority_times) if priority_times else 0
    avg_location = sum(location_times) / len(location_times) if location_times else 0
    
    strategies = ['FIFO', 'Priority-based', 'Location-based']
    avg_times = [avg_fifo, avg_priority, avg_location]
    
    plt.bar(strategies, avg_times)
    plt.xlabel('Strategy')
    plt.ylabel('Average Processing Time')
    plt.title('Comparison of Distribution Strategies')
    plt.show()

def logout(adminpw, adminw):
    adminpw.destroy()
    adminw.destroy()
    mainroot.deiconify()

def userp():
    global mainroot
    mainroot.withdraw()
    userw = tk.Toplevel(mainroot)
    userw.geometry("400x400")
    userw.title("User Request")
    
    tk.Label(userw, text="Enter Name:").pack(pady=5)
    name = tk.Entry(userw)
    name.pack(pady=5)
    
    tk.Label(userw, text="Enter Phone Number:").pack(pady=5)
    phone = tk.Entry(userw)
    phone.pack(pady=5)
    
    tk.Label(userw, text="Enter Location:").pack(pady=5)
    location = tk.Entry(userw)
    location.pack(pady=5)
    
    tk.Label(userw, text="Enter Item:").pack(pady=5)
    item = tk.Entry(userw)
    item.pack(pady=5)
    
    tk.Label(userw, text="Enter Quantity:").pack(pady=5)
    quantity = tk.Entry(userw)
    quantity.pack(pady=5)
    
    tk.Label(userw, text="Enter Situation:").pack(pady=5)
    situation = tk.Entry(userw)
    situation.pack(pady=5)
    
    submit = tk.Button(userw, text="Submit Request", command=lambda: submit_request(name, phone, location, item, quantity, situation, userw))
    submit.pack(pady=10)

def submit_request(name, phone, location, item, quantity, situation, userw):
    try:
        sent_time = time.time()
        query = "INSERT INTO request VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycur.execute(query, (name.get(), phone.get(), location.get(), item.get(), int(quantity.get()), situation.get(), sent_time))
        inventory.commit()
        messagebox.showinfo("Success", "Request Submitted")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        userw.destroy()
        mainroot.deiconify()

if __name__ == "__main__":
    main()
