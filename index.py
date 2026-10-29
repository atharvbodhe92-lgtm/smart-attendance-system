import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# 1. Main Window Setup (Sarvat aadhi window banavne)
root = tk.Tk()
root.title("Smart Attendance System - Practical No. 22")
root.geometry("820x580")
root.config(bg="#f3f0f7")

# Data Structure: Vidyarthyanchi hajeri sathavnyasathi List
attendance_list = []

# 2. UI Elements (Boxes ani Table aadhi tayar karne mhanje error yenar nahi)
header = tk.Frame(root, bg="#4a148c", height=70)
header.pack(fill=tk.X)
tk.Label(header, text="SMART ATTENDANCE PORTAL", font=("Segoe UI", 20, "bold"), bg="#4a148c", fg="white").pack(pady=(8, 0))
tk.Label(header, text=f"SY AIML - Daily Attendance Logger  |  Date: {datetime.now().strftime('%d-%m-%Y')}", font=("Segoe UI", 10), bg="#4a148c", fg="#e1bee7").pack(pady=(0, 8))

input_frame = tk.LabelFrame(root, text="Mark Student Attendance", font=("Segoe UI", 10, "bold"), bg="#f3f0f7", fg="#4a148c", padx=15, pady=10)
input_frame.pack(fill=tk.X, padx=20, pady=10)

tk.Label(input_frame, text="Roll No:", bg="#f3f0f7", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, sticky="w")
entry_roll = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_roll.grid(row=0, column=1, padx=8, pady=5)

tk.Label(input_frame, text="Student Name:", bg="#f3f0f7", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, sticky="w")
entry_name = tk.Entry(input_frame, width=24, font=("Segoe UI", 10))
entry_name.grid(row=0, column=3, padx=8, pady=5)

tk.Label(input_frame, text="Subject:", bg="#f3f0f7", font=("Segoe UI", 10)).grid(row=0, column=4, padx=5, sticky="w")
combo_sub = ttk.Combobox(input_frame, values=["Python", "AIML", "Data Structures", "DBMS"], width=14, state="readonly", font=("Segoe UI", 10))
combo_sub.current(0)
combo_sub.grid(row=0, column=5, padx=8, pady=5)

stats_frame = tk.Frame(root, bg="#e1bee7", bd=1, relief=tk.SOLID, pady=8)
stats_frame.pack(fill=tk.X, padx=20, pady=5)

lbl_total = tk.Label(stats_frame, text="Total Students: 0", font=("Segoe UI", 11, "bold"), bg="#e1bee7", fg="#333333")
lbl_total.pack(side=tk.LEFT, expand=True)

lbl_present = tk.Label(stats_frame, text="Present: 0", font=("Segoe UI", 11, "bold"), bg="#e1bee7", fg="#1b5e20")
lbl_present.pack(side=tk.LEFT, expand=True)

lbl_absent = tk.Label(stats_frame, text="Absent: 0", font=("Segoe UI", 11, "bold"), bg="#e1bee7", fg="#b71c1c")
lbl_absent.pack(side=tk.LEFT, expand=True)

lbl_percent = tk.Label(stats_frame, text="Attendance: 0.0%", font=("Segoe UI", 11, "bold"), bg="#e1bee7", fg="#4a148c")
lbl_percent.pack(side=tk.LEFT, expand=True)

table_frame = tk.Frame(root, bg="#f3f0f7")
table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

cols = ("Roll No", "Student Name", "Subject", "Attendance Status", "Time Marked")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
for c in cols:
    tree.heading(c, text=c)

tree.column("Roll No", width=80, anchor="center")
tree.column("Student Name", width=220, anchor="w")
tree.column("Subject", width=130, anchor="center")
tree.column("Attendance Status", width=130, anchor="center")
tree.column("Time Marked", width=120, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

# 3. Functions (Sagle kam karnare functions)
def update_counters():
    total_cnt = len(attendance_list)
    present_cnt = sum(1 for r in attendance_list if r["status"] == "Present")
    absent_cnt = total_cnt - present_cnt
    percent_val = (present_cnt / total_cnt * 100) if total_cnt > 0 else 0.0

    lbl_total.config(text=f"Total Students: {total_cnt}")
    lbl_present.config(text=f"Present: {present_cnt}")
    lbl_absent.config(text=f"Absent: {absent_cnt}")
    lbl_percent.config(text=f"Attendance: {percent_val:.1f}%")

def mark_attendance(status):
    roll_str = entry_roll.get().strip()
    name = entry_name.get().strip()
    subject = combo_sub.get()

    if not roll_str or not name:
        messagebox.showwarning("Input Error", "Please enter both Roll No and Student Name!")
        return

    try:
        roll = int(roll_str)
    except ValueError:
        messagebox.showerror("Invalid Roll No", "Roll Number must be a valid integer number!")
        return

    for rec in attendance_list:
        if rec["roll"] == roll:
            messagebox.showwarning("Duplicate", f"Roll No {roll} is already marked!")
            return

    time_now = datetime.now().strftime("%I:%M %p")
    record = {"roll": roll, "name": name.title(), "subject": subject, "status": status, "time": time_now}
    attendance_list.append(record)

    tree.insert("", tk.END, values=(roll, name.title(), subject, status, time_now))
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    update_counters()

def toggle_status():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student from the table to change status!")
        return

    for item in selected:
        idx = tree.index(item)
        current = attendance_list[idx]["status"]
        new_status = "Absent" if current == "Present" else "Present"
        attendance_list[idx]["status"] = new_status
        rec = attendance_list[idx]
        tree.item(item, values=(rec["roll"], rec["name"], rec["subject"], rec["status"], rec["time"]))

    update_counters()

def delete_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a record from the table to delete!")
        return

    for item in selected:
        idx = tree.index(item)
        tree.delete(item)
        del attendance_list[idx]

    update_counters()

def clear_all():
    attendance_list.clear()
    for row in tree.get_children():
        tree.delete(row)
    update_counters()

def save_to_file():
    if not attendance_list:
        messagebox.showwarning("Empty Record", "Please mark attendance for at least one student before saving!")
        return

    date_str = datetime.now().strftime("%d-%m-%Y")
    filename = "Attendance_Sheet.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("========================================================\n")
            f.write(f"         STUDENT ATTENDANCE SHEET ({date_str})\n")
            f.write("========================================================\n")
            f.write(f"{'Roll No':<10}{'Student Name':<20}{'Subject':<12}{'Status':<10}\n")
            f.write("--------------------------------------------------------\n")
            for r in attendance_list:
                f.write(f"{r['roll']:<10}{r['name']:<20}{r['subject']:<12}{r['status']:<10}\n")
            f.write("--------------------------------------------------------\n")
            t_cnt = len(attendance_list)
            p_cnt = sum(1 for r in attendance_list if r["status"] == "Present")
            a_cnt = t_cnt - p_cnt
            f.write(f"Total: {t_cnt}  |  Present: {p_cnt}  |  Absent: {a_cnt}\n")
            f.write("========================================================\n")

        messagebox.showinfo("Saved Successfully", f"Attendance saved permanently in '{filename}'!")
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving file: {e}")

# 4. Connecting Buttons
btn_frame = tk.Frame(input_frame, bg="#f3f0f7")
btn_frame.grid(row=1, column=0, columnspan=6, pady=(8, 2))

tk.Button(btn_frame, text="✔ Mark PRESENT", bg="#2e7d32", fg="white", font=("Segoe UI", 10, "bold"), width=18, command=lambda: mark_attendance("Present")).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="✖ Mark ABSENT", bg="#c62828", fg="white", font=("Segoe UI", 10, "bold"), width=18, command=lambda: mark_attendance("Absent")).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="⇄ Change P / A", bg="#6a1b9a", fg="white", font=("Segoe UI", 10, "bold"), width=16, command=toggle_status).pack(side=tk.LEFT, padx=10)

bot_frame = tk.Frame(root, bg="#f3f0f7")
bot_frame.pack(fill=tk.X, padx=20, pady=12)

tk.Button(bot_frame, text="Delete Selected", bg="#d32f2f", fg="white", font=("Segoe UI", 9, "bold"), width=15, command=delete_record).pack(side=tk.LEFT, padx=5)
tk.Button(bot_frame, text="Clear Sheet", bg="#f57c00", fg="white", font=("Segoe UI", 9, "bold"), width=15, command=clear_all).pack(side=tk.LEFT, padx=5)
tk.Button(bot_frame, text="💾 Save Attendance Sheet (.txt)", bg="#1565c0", fg="white", font=("Segoe UI", 10, "bold"), width=26, command=save_to_file).pack(side=tk.RIGHT, padx=5)

root.mainloop()