import tkinter as tk
from tkinter import messagebox, scrolledtext, Listbox, simpledialog
import os
import base64

# File paths
CREDENTIALS_FILE = "credentials.txt"
NOTES_FOLDER = "notes"  # Folder to store notes

# Create notes directory if not exists
if not os.path.exists(NOTES_FOLDER):
    os.makedirs(NOTES_FOLDER)

# Encrypt & Decrypt functions
def encrypt(data):
    return base64.b64encode(data.encode()).decode()

def decrypt(data):
    return base64.b64decode(data.encode()).decode()

# Check if user exists
def is_registered():
    return os.path.exists(CREDENTIALS_FILE)

# Save user credentials
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "w") as file:
        file.write(encrypt(username) + "\n")
        file.write(encrypt(password))

# Verify login details
def verify_login(username, password):
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            stored_username = decrypt(file.readline().strip())
            stored_password = decrypt(file.readline().strip())
            return username == stored_username and password == stored_password
    except:
        return False

# Save notes with custom name
def save_notes():
    note_name = simpledialog.askstring("Note Name", "Enter a name for your note:")
    if not note_name:
        messagebox.showwarning("Warning", "Note name cannot be empty!")
        return

    note_content = notes_text.get("1.0", tk.END).strip()
    if not note_content:
        messagebox.showwarning("Warning", "Note cannot be empty!")
        return

    file_path = os.path.join(NOTES_FOLDER, note_name + ".txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(note_content)

    messagebox.showinfo("Success", f"Note '{note_name}' saved successfully!")
    notes_text.delete("1.0", tk.END)
    load_notes()

# Load previous notes into listbox
def load_notes():
    notes_listbox.delete(0, tk.END)
    note_files = os.listdir(NOTES_FOLDER)
    for note_file in note_files:
        notes_listbox.insert(tk.END, note_file.replace(".txt", ""))  # Display name without ".txt"

# Show full content of a selected note
def show_note(event):
    selected_index = notes_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        note_name = notes_listbox.get(index)
        file_path = os.path.join(NOTES_FOLDER, note_name + ".txt")

        with open(file_path, "r", encoding="utf-8") as file:
            note_content = file.read()

        messagebox.showinfo(f"Note - {note_name}", note_content)

# Open Notes Window
def open_notes_window():
    login_window.destroy()

    notes_window = tk.Tk()
    notes_window.title("Personal Diary")
    notes_window.geometry("600x450")
    notes_window.config(bg="#f3eacb")

    tk.Label(notes_window, text="Write Your Notes 📝", font=("Arial", 14, "bold"), bg="#f3eacb").pack(pady=5)

    global notes_text
    notes_text = scrolledtext.ScrolledText(notes_window, font=("Arial", 12), width=50, height=5)
    notes_text.pack(pady=5)

    save_button = tk.Button(notes_window, text="Save Note", command=save_notes, font=("Arial", 12), bg="#4CAF50", fg="white")
    save_button.pack(pady=5)

    # Notes History Section
    tk.Label(notes_window, text="Previous Notes 📜", font=("Arial", 12, "bold"), bg="#f3eacb").pack(pady=5)

    global notes_listbox
    notes_listbox = Listbox(notes_window, font=("Arial", 12), width=50, height=7)
    notes_listbox.pack(pady=5)
    notes_listbox.bind("<<ListboxSelect>>", show_note)  # Click to view full note

    load_notes()  # Load existing notes

    notes_window.mainloop()

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if verify_login(username, password):
        open_notes_window()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Register Function
def register():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        if is_registered():
            messagebox.showerror("Error", "User already registered! Please log in.")
        else:
            save_credentials(username, password)
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
    else:
        messagebox.showwarning("Warning", "Username and Password cannot be empty!")

# Create Login Window
login_window = tk.Tk()
login_window.title("Personal Diary - Login")
login_window.geometry("400x300")
login_window.config(bg="#d4a373")

tk.Label(login_window, text="Personal Diary 🔒", font=("Arial", 16, "bold"), bg="#d4a373").pack(pady=10)
tk.Label(login_window, text="Username:", font=("Arial", 12), bg="#d4a373").pack()

username_entry = tk.Entry(login_window, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#d4a373").pack()
password_entry = tk.Entry(login_window, font=("Arial", 12), width=30, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white")
login_button.pack(pady=10)

register_button = tk.Button(login_window, text="Register", command=register, font=("Arial", 12), bg="#008CBA", fg="white")
register_button.pack(pady=5)

login_window.mainloop()
