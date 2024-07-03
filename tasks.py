#Added update task function
from dataclasses import dataclass
import tkinter
from tkinter import messagebox
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from turtle import st
from typing import List

from Geoloction import Geoloction
from hasher import Hasher  # Import the Hasher class from the hasher module

# Create an instance of the Hasher class
hasher = Hasher()

# create window
window = tkinter.Tk()
# creating window title
window.title("Todoapp form")
# sizing the window
window.geometry('420x520')
window.configure(bg="#333333")

# setting the server
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'ggbemou95@gmail.com'
sender_password = 'sibtihdiuanrgopy'
recipient_email = 'ggbemou95@gmail.com'
geoclass = Geoloction()
@dataclass
class Task:
    id: int
    task:str
    location:str
    timestamp:str
    status:str
    user_id:str

@dataclass
class UserSettings:
    id: int
    user_id: int
    recipient_email: str

class UserSession(object):
     _usersession = None
     _recipient_email = ""
     task:List = []
     def __init__(self):
        pass
     
     def get_usersession(self):
        return self._usersession
     def set_usersession(self,user): 
        self._usersession = user
     def add_task(self, tasks:List[str]| tuple):
        if isinstance(tasks,tuple):
            self.task.append(Task(*tasks))
        if isinstance(tasks,list):
            for t in tasks:
                 task_obj = Task(*t)
                 if task_obj not in self.task:
                    self.task.append(task_obj)
     def refresh(self,user_id): 
         self.add_task(hasher.db.fetch_tasks_for_user(user_id))

     def find_task(self, task:str,user_id):
         return list(filter(lambda x: x.task.find(task) != -1 and x.user_id == user_id, self.task))[0]
     def set_recipient_email(self, user_id,recipient_email):
         self._recipient_email = hasher.db.upsert_user_settings(user_id,recipient_email)
     def get_recipient_email(self,user_id) -> str:
        db_email_value =  hasher.db.get_user_settings(user_id)
        if db_email_value:
            self._recipient_email = db_email_value[2]
            return self._recipient_email
        else:
            return None
    
usersesions = UserSession()
def send_email(subject, body):
    try:
        if usersesions.get_recipient_email() == "": 
            messagebox.showerror("Error", f"Please enter a recipient email")
            raise("Error")
        recipient_email = usersesions.get_recipient_email()
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")
def show_signup():
    signup_window = tkinter.Toplevel(window)
    signup_window.title("Sign Up")
    signup_window.geometry('300x250')
    signup_window.configure(bg="#333333")

    def signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        if username and password:
            hasher.store_user(username, password)
            messagebox.showinfo("Success", "User created successfully")
            signup_window.destroy()
        else:
            messagebox.showerror("Error", "Username and Password cannot be empty")

    tkinter.Label(signup_window, text='Sign Up', bg="#333333", fg="#c97c5d", font="Arial, 20").pack(pady=10)
    tkinter.Label(signup_window, text='Username', bg="#333333", fg="#FFFFFF", font="Arial, 14").pack(pady=5)
    signup_username_entry = tkinter.Entry(signup_window, font="Arial, 14", bg="#FFFFFF")
    signup_username_entry.pack(pady=5)
    tkinter.Label(signup_window, text='Password', bg="#333333", fg="#FFFFFF", font="Arial, 14").pack(pady=5)
    signup_password_entry = tkinter.Entry(signup_window, show="*", font="Arial, 14", bg="#FFFFFF")
    signup_password_entry.pack(pady=5)
    tkinter.Button(signup_window, text="Sign Up", bg="#333333", fg="#c97c5d", font="Arial, 14", command=signup).pack(pady=10)


def login():
    if hasher.check_user(username_entry.get(),password_entry.get()):
        messagebox.showinfo(title="Welcome to todo tasks", message="Welcome to todo list application")
        usersesions.set_usersession(username_entry.get())
        global recipient_email
        recipient_email = usersesions.get_recipient_email(hasher.db.get_user(usersesions.get_usersession())[0])
        show_todo_app()
    else:
        messagebox.showerror(title="Error", message="Invalid login")

def reset():
    username_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)

def load_users_task(usersesions_name,tasks_listbox,completed_tasks_listbox): 
    if usersesions_name:
        user_id = hasher.db.get_user(usersesions_name)[0]
        tasks = hasher.db.fetch_tasks_for_user(user_id)
        for task in tasks:
            if task[4] == "UNCOMPLETE":
                usersesions.add_task(task)
                tasks_listbox.insert(tkinter.END, task[1])
            if task[4] == "COMPLETE":
                completed_task = f"Task: {task[1]} (Completed at {task[3]} in location {task[2]})"
                completed_tasks_listbox.insert(tkinter.END, completed_task)
def show_todo_app():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Todo List App")

    def add_task():
       task = task_entry.get()
       if task:
            user_id = hasher.db.get_user(usersesions.get_usersession())[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            location = "Unknown"  # Replace with geoclass.get_location().city if Geoloction class is available
            status = "UNCOMPLETE"
            hasher.db.add_task(task, location, timestamp,status, user_id)
            usersesions.refresh(user_id)
            tasks_listbox.insert(tkinter.END, task)
            task_entry.delete(0, tkinter.END)
       else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def update_task():
        try:
            task_index = tasks_listbox.curselection()[0]
            new_task = task_entry.get()
            task = tasks_listbox.get(task_index)
            if new_task:
                tasks_listbox.delete(task_index)
                tasks_listbox.insert(task_index, new_task)
                user_id = hasher.db.get_user(usersesions.get_usersession())[0]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                location = "Unknown"  # Replace with geoclass.get_location().city if Geoloction class is available
                status = "UNCOMPLETE"
                found_task = usersesions.find_task(task,user_id)
                hasher.db.update_task(
                    task_id = found_task.id,
                    new_task = new_task ,
                    new_location = location,
                    new_timestamp = timestamp,
                    new_status= status
                    )
                usersesions.refresh(user_id)
                task_entry.delete(0, tkinter.END)
            else:
                messagebox.showerror("Error", "Please enter a new task description")
        except:
            messagebox.showerror("Error", "Please select a task to update")

    def delete_task():
        try:
            selected_task_index = tasks_listbox.curselection()[0]
            task = tasks_listbox.get(selected_task_index)
            tasks_listbox.delete(selected_task_index)
            user_id = hasher.db.get_user(usersesions.get_usersession())[0]
            found_task = usersesions.find_task(task,user_id)
            hasher.db.delete_task(found_task.id,user_id)
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def complete_task():
        try:
            selected_task_index = tasks_listbox.curselection()[0]
            task = tasks_listbox.get(selected_task_index)
            completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tasks_listbox.delete(selected_task_index)
            geoloaction = geoclass.get_location()
            city_and_region = f"{geoloaction.city},{geoloaction.region}"
            completed_task = f"Task:{task} (Completed at {completion_time} in location {city_and_region})"
            completed_tasks_listbox.insert(tkinter.END, completed_task)
            user_id = hasher.db.get_user(usersesions.get_usersession())[0]
            found_task = usersesions.find_task(task,user_id)
            hasher.db.update_task(
                task_id = found_task.id,
                new_task = task ,
                new_location = f"{city_and_region}",
                new_timestamp = completion_time,
                new_status= "COMPLETE"
                )
            # Compose the email message
            subject = "Task Completed Notification"
            body = f"""
            The following task has been completed:
            Task: {task}
            Completion time:{completion_time}
            at location {geoloaction.city}
            Best regards,
            Your To-Do App
            """

            # Send the email
            send_email(subject, body)
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to mark as complete.")
    
    task_frame = tkinter.Frame(window, bg="#333333")
    task_frame.pack(pady=10)

    task_label = tkinter.Label(task_frame, text="Enter a task:", bg="#333333", fg="#FFFFFF", font="Arial, 14")
    task_label.pack(pady=5)

    task_entry = tkinter.Entry(task_frame, width=30, font="Arial, 14")
    task_entry.pack(pady=5)

    add_task_button = tkinter.Button(task_frame, text="Add Task", width=15, command=add_task, font="Arial, 14")
    add_task_button.pack(pady=5)

    update_task_button = tkinter.Button(task_frame, text="Update Task", width=15, command=update_task, font="Arial, 14")
    update_task_button.pack(pady=5)

    tasks_listbox = tkinter.Listbox(task_frame, width=50, height=10, font="Arial, 14")
    tasks_listbox.pack(pady=10)

    complete_task_button = tkinter.Button(task_frame, text="Complete Task", width=15, command=complete_task, font="Arial, 14")
    complete_task_button.pack(pady=5)

    completed_tasks_listbox = tkinter.Listbox(task_frame, width=50, height=10, font="Arial, 14")
    completed_tasks_listbox.pack(pady=10)

    delete_task_button = tkinter.Button(task_frame, text="Delete Task", width=15, command=delete_task, font="Arial, 14")
    delete_task_button.pack(pady=5)
    settings_button = tkinter.Button(task_frame,text="Setting",width=15, command=show_setting, font="Arial, 14")
    settings_button.pack(pady=6)
    load_users_task(usersesions.get_usersession(),tasks_listbox,completed_tasks_listbox)
def show_setting():
    setting_window = tkinter.Toplevel(window)
    setting_window.title("Settings")
    setting_window.geometry('300x250')
    setting_window.configure(bg="#333333")

    def setEmail():
        email = email_entry.get()
        if email:
            usersesions.set_recipient_email(hasher.db.get_user(usersesions.get_usersession())[0],email)
            messagebox.showinfo("Success", "Email uodated successfully")
            setting_window.destroy()
        else:
            messagebox.showerror("Error", "Email cannot be empty")

    tkinter.Label(setting_window, text='Settings', bg="#333333", fg="#c97c5d", font="Arial, 20").pack(pady=10)
    tkinter.Label(setting_window, text='Set Recipient Email', bg="#333333", fg="#FFFFFF", font="Arial, 14").pack(pady=5)
    email_entry = tkinter.Entry(setting_window, font="Arial, 14", bg="#FFFFFF")
    db_email = usersesions.get_recipient_email(hasher.db.get_user(usersesions.get_usersession())[0])
    if db_email:
        email_entry.insert(0,db_email)
    email_entry.pack(pady=5)
    tkinter.Button(setting_window, text="Save", bg="#333333", fg="#c97c5d", font="Arial, 14", command=setEmail).pack(pady=10)  

# responsive layout
frame = tkinter.Frame(bg="#333333")

# creating widgets for the login screen
login_label = tkinter.Label(frame, text='TaskLogin', bg="#333333", fg="#c97c5d", font="Arial, 30")
username_label = tkinter.Label(frame, text='Username', bg="#333333", fg="#FFFFFF", font="Arial, 22")
username_entry = tkinter.Entry(frame, font="Arial, 22", bg="#FFFFFF")
password_label = tkinter.Label(frame, text='Password', bg="#333333", fg="#FFFFFF", font="Arial, 22")
password_entry = tkinter.Entry(frame, show="*", font="Arial, 22", bg="#FFFFFF")
login_button = tkinter.Button(frame, text="Login", bg="#333333", fg="#c97c5d", font="Arial, 30", command=login)
reset_button = tkinter.Button(frame, text="Reset", bg="#333333", fg="#c97c5d", font="Arial, 30", command=reset)
signup_button = tkinter.Button(frame, text="Sign Up", bg="#333333", fg="#c97c5d", font="Arial, 30", command=show_signup)

frame.pack()

# inserting widgets on the screen for the login screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=30)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=15)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=15)
login_button.grid(row=3, column=0, pady=20, padx=5)
reset_button.grid(row=3, column=1, pady=20, padx=5)
signup_button.grid(row=4, column=0, columnspan=2, pady=20, padx=5)

window.mainloop()
