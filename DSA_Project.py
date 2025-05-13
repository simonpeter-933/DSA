#importing the needed modules
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

#global data storage
subjects, lectures, tasks, notes = [], {}, [], []

#functions
def add_subject():
    sub = subject_entry.get().strip()
    if not sub:
        messagebox.showwarning("Input Error", "Enter a subject.")
    elif sub in subjects:
        messagebox.showwarning("Duplicate", "Subject already exists.")
    else:
        subjects.append(sub)
        subject_listbox.insert(tk.END, sub)
        update_comboboxes()
        subject_entry.delete(0, tk.END)

def update_comboboxes():
    sub_values = subjects
    note_sub_cb['values'] = task_sub_cb['values'] = sub_values

def save_notes():
    s, l, c = note_sub_cb.get(), lecture_entry.get().strip(), notes_text.get("1.0", "end-1c").strip()
    if not all([s, l, c]):
        messagebox.showwarning("Missing Info", "Complete all fields.")
        return
    notes.append({'subject': s, 'lecture': l, 'content': c, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")})
    lectures.setdefault(s, []).append(l)
    lecture_entry.delete(0, tk.END)
    notes_text.delete("1.0", tk.END)

def add_task():
    desc, sub, typ, freq, dur, dl = (task_desc.get().strip(), task_sub_cb.get(), task_type_cb.get(),
                                     freq_sb.get(), dur_sb.get(), deadline_entry.get().strip())
    if not all([desc, sub, typ, freq, dur, dl]):
        messagebox.showwarning("Missing Info", "Complete all fields.")
        return
    try:
        datetime.strptime(dl, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Format Error", "Deadline format: YYYY-MM-DD")
        return
    tasks.append({'desc': desc, 'sub': sub, 'type': typ, 'freq': freq, 'dur': dur, 'dl': dl})
    task_desc.delete(0, tk.END)

def flip_cards():
    if not notes:
        messagebox.showinfo("Empty", "No notes to review.")
        return
    flip_win = tk.Toplevel(app)
    flip_win.title("Flip Cards")
    idx, show_back = [0], [False]
    front, back = tk.StringVar(), tk.StringVar()

    def update_card():
        n = notes[idx[0]]
        front.set(f"{n['subject']} - {n['lecture']}")
        back.set(n['content'])

    def flip():
        show_back[0] = not show_back[0]
        front_lbl.pack_forget() if show_back[0] else back_lbl.pack_forget()
        (back_lbl if show_back[0] else front_lbl).pack(pady=10)

    def next_card():
        idx[0] = (idx[0] + 1) % len(notes)
        update_card()
        if show_back[0]: flip()

    update_card()
    front_lbl = ttk.Label(flip_win, textvariable=front, wraplength=350)
    back_lbl = ttk.Label(flip_win, textvariable=back, wraplength=350)
    front_lbl.pack(pady=10)
    ttk.Button(flip_win, text="Flip", command=flip).pack()
    ttk.Button(flip_win, text="Next", command=next_card).pack()

def view_notes():
    if not notes:
        messagebox.showinfo("Empty", "No notes to show.")
        return
    note_win = tk.Toplevel(app)
    note_win.title("Notes List")
    tree = ttk.Treeview(note_win, columns=('Sub', 'Lect', 'Date'), show='headings')
    for col in ('Sub', 'Lect', 'Date'):
        tree.heading(col, text=col)
    for n in notes:
        tree.insert('', 'end', values=(n['subject'], n['lecture'], n['timestamp']))
    tree.pack(expand=True, fill='both')
    def show_content():
        sel = tree.focus()
        if not sel: return
        val = tree.item(sel, 'values')
        for n in notes:
            if n['subject'] == val[0] and n['lecture'] == val[1]:
                cont_win = tk.Toplevel(note_win)
                cont_win.title(f"{val[0]} - {val[1]}")
                tk.Text(cont_win, height=10, wrap='word').insert('1.0', n['content']).pack(expand=True, fill='both')
                break
    ttk.Button(note_win, text="View Content", command=show_content).pack(pady=5)

#GUI layout
app = tk.Tk()
app.title("Study Organizer")
app.geometry("500x600")
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True)

#Subjects tab
sub_frame = ttk.Frame(notebook); notebook.add(sub_frame, text="Subjects")
tk.Label(sub_frame, text="Subject:").pack(pady=5)
subject_entry = tk.Entry(sub_frame); subject_entry.pack()
ttk.Button(sub_frame, text="Add", command=add_subject).pack(pady=5)
subject_listbox = tk.Listbox(sub_frame); subject_listbox.pack(expand=True, fill='both')

#Notes tab
note_frame = ttk.Frame(notebook); notebook.add(note_frame, text="Notes")
note_sub_cb = ttk.Combobox(note_frame, state="readonly"); note_sub_cb.pack(pady=5)
lecture_entry = tk.Entry(note_frame); lecture_entry.pack(pady=5)
notes_text = tk.Text(note_frame, height=10); notes_text.pack(pady=5)
ttk.Button(note_frame, text="Save Notes", command=save_notes).pack(pady=5)

#Tasks tab
task_frame = ttk.Frame(notebook); notebook.add(task_frame, text="Tasks")
task_desc = tk.Entry(task_frame); task_desc.pack(pady=5)
task_sub_cb = ttk.Combobox(task_frame, state="readonly"); task_sub_cb.pack(pady=5)
task_type_cb = ttk.Combobox(task_frame, values=["Activity", "Quiz"], state="readonly"); task_type_cb.pack(pady=5)
freq_sb = tk.Spinbox(task_frame, from_=1, to=7); freq_sb.pack(pady=5)
dur_sb = tk.Spinbox(task_frame, from_=15, to=240, increment=15); dur_sb.pack(pady=5)
deadline_entry = tk.Entry(task_frame); deadline_entry.insert(0, "YYYY-MM-DD"); deadline_entry.pack(pady=5)
ttk.Button(task_frame, text="Add Task", command=add_task).pack(pady=5)

#Review tab
review_frame = ttk.Frame(notebook); notebook.add(review_frame, text="Review")
ttk.Button(review_frame, text="Flip Cards", command=flip_cards).pack(pady=10)
ttk.Button(review_frame, text="View Notes", command=view_notes).pack(pady=5)

app.mainloop()
