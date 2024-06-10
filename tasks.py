import tkinter
from tkinter import messagebox
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from Geoloction import Geoloction

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

def send_email(subject, body):
    try:
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

def login():
    username = "Group"
    password = 'group1234'
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Welcome to todo tasks", message="Welcome to todo list application")
        show_todo_app()
    else:
        messagebox.showerror(title="Error", message="Invalid login")

def reset():
    username_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)

def show_todo_app():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Todo List App")

    def add_task():
        task = task_entry.get()
        if task:
            tasks_listbox.insert(tkinter.END, task)
            task_entry.delete(0, tkinter.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task():
        try:
            selected_task_index = tasks_listbox.curselection()[0]
            tasks_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def complete_task():
        try:
            selected_task_index = tasks_listbox.curselection()[0]
            task = tasks_listbox.get(selected_task_index)
            completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            completed_task = f"{task} (Completed at {completion_time})"
            tasks_listbox.delete(selected_task_index)
            completed_tasks_listbox.insert(tkinter.END, completed_task)
            geoloaction = geoclass.get_location()
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
            print(body)

            # Send the email
            # send_email(subject, body)
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

    tasks_listbox = tkinter.Listbox(task_frame, width=50, height=10, font="Arial, 14")
    tasks_listbox.pack(pady=10)

    complete_task_button = tkinter.Button(task_frame, text="Complete Task", width=15, command=complete_task, font="Arial, 14")
    complete_task_button.pack(pady=5)

    completed_tasks_listbox = tkinter.Listbox(task_frame, width=50, height=10, font="Arial, 14")
    completed_tasks_listbox.pack(pady=10)

    delete_task_button = tkinter.Button(task_frame, text="Delete Task", width=15, command=delete_task, font="Arial, 14")
    delete_task_button.pack(pady=5)

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

frame.pack()

# inserting widgets on the screen for the login screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=30)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=15)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=15)
login_button.grid(row=3, column=0, pady=20, padx=5)
reset_button.grid(row=3, column=1, pady=20, padx=5)

window.mainloop()
